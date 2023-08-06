#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
from functools import cmp_to_key
from random import choice
from typing import FrozenSet, Tuple, List, Optional, Callable, Dict

from zepben.evolve import Terminal, NetworkService, AcLineSegment, PowerTransformer, EnergyConsumer, \
    PowerTransformerEnd, ConductingEquipment, \
    PowerElectronicsConnection, BusBranchNetworkCreator, EnergySource, Switch, Junction, BusbarSection, PerLengthSequenceImpedance, EquivalentBranch, \
    TransformerFunctionKind, WireInfo

from zepben.opendss import BusConnection, Bus
from zepben.opendss import ConnectionPoint
from zepben.opendss import LineCode, Circuit, Line, Load, NetworkModel, Transformer, TransformerWinding
from zepben.opendss.creators.utils import id_from_identified_objects, get_bus_nodes, cmp_end_tn_by_t_direction, \
    get_voltage_kv, tx_rating, vreg_from_nominal_v, is_swer_tx, is_dist_tx, create_swer_tx, \
    create_tx
from zepben.opendss.creators.validators.validator import OpenDssNetworkValidator
from zepben.opendss.model.network.reg_control import RegControl

__all__ = ["OpenDssNetworkCreator", "id_from_identified_objects"]


class OpenDssNetworkCreator(
    BusBranchNetworkCreator[NetworkModel, Bus, Line, Line, Transformer, Circuit, Load, Load, OpenDssNetworkValidator]
):

    def __init__(
            self, *,
            logger: logging.Logger,
            vm_pu: float = 1.0,
            load_provider: Callable[[ConductingEquipment], Tuple[float, float]] = lambda x: (0, 0),
            pec_load_provider: Callable[[ConductingEquipment], Tuple[float, float]] = lambda x: (0, 0),
            min_line_r_ohm: float = 0.001,
            min_line_x_ohm: float = 0.001
    ):
        # -- input --
        self.vm_pu = vm_pu
        self.logger = logger
        self.load_provider = load_provider
        self.pec_load_provider = pec_load_provider
        self.min_line_r_ohm = min_line_r_ohm
        self.min_line_x_ohm = min_line_x_ohm

    def bus_branch_network_creator(self, node_breaker_network: NetworkService) -> NetworkModel:
        network = NetworkModel(default_base_frequency=50)
        return network

    def topological_node_creator(
            self,
            bus_branch_network: NetworkModel,
            base_voltage: Optional[int],
            collapsed_conducting_equipment: FrozenSet[ConductingEquipment],
            border_terminals: FrozenSet[Terminal],
            inner_terminals: FrozenSet[Terminal],
            node_breaker_network: NetworkService
    ) -> Tuple[str, Bus]:
        uid = id_from_identified_objects(border_terminals)
        max_phases_terminal = max((t for t in border_terminals), key=lambda t: len(t.phases.single_phases))
        bus = Bus(uid=uid, nodes=get_bus_nodes(max_phases_terminal))
        bus_branch_network.add_bus(bus)
        return uid, bus

    def topological_branch_creator(
            self,
            bus_branch_network: NetworkModel,
            connected_topological_nodes: Tuple[Bus, Bus],
            length: Optional[float],
            collapsed_ac_line_segments: FrozenSet[AcLineSegment],
            border_terminals: FrozenSet[Terminal],
            inner_terminals: FrozenSet[Terminal],
            node_breaker_network: NetworkService
    ) -> Tuple[str, Line]:
        ac_line = next(iter(collapsed_ac_line_segments))
        connected_nodes = min(connected_topological_nodes, key=lambda b: len(b.nodes)).nodes
        line_code = self._get_create_line_code(bus_branch_network, ac_line.per_length_sequence_impedance, ac_line.wire_info, len(connected_nodes))

        uid = id_from_identified_objects(collapsed_ac_line_segments)
        line = Line(
            uid=uid,
            units="m",
            length=0.5 if length is None else length,
            bus_conn1=BusConnection(connected_topological_nodes[0], connected_nodes),
            bus_conn2=BusConnection(connected_topological_nodes[1], connected_nodes),
            line_code=line_code
        )
        bus_branch_network.add_line(line)
        return uid, line

    @staticmethod
    def _get_create_line_code(
            bus_branch_network: NetworkModel,
            per_length_sequence_impedance: PerLengthSequenceImpedance,
            wire_info: WireInfo,
            nphases: int
    ) -> LineCode:
        uid = f"{wire_info.mrid}-{per_length_sequence_impedance.mrid}-{nphases}W"
        line_code = bus_branch_network.line_codes.get(uid)
        if line_code is not None:
            return line_code

        line_code = LineCode(
            uid=uid,
            units="m",
            nphases=nphases,
            r1=per_length_sequence_impedance.r,
            r0=per_length_sequence_impedance.r0,
            x1=per_length_sequence_impedance.x,
            x0=per_length_sequence_impedance.x0,
            b1=0.0 if per_length_sequence_impedance.bch is None else per_length_sequence_impedance.bch * 1000000,
            b0=0.0 if per_length_sequence_impedance.b0ch is None else per_length_sequence_impedance.b0ch * 1000000,
            norm_amps=wire_info.rated_current,
            emerg_amps=wire_info.rated_current * 1.5
        )
        bus_branch_network.add_line_code(line_code)
        return line_code

    def equivalent_branch_creator(self, bus_branch_network: NetworkModel, connected_topological_nodes: List[Bus], equivalent_branch: EquivalentBranch,
                                  node_breaker_network: NetworkService) -> Tuple[str, Line]:
        raise RuntimeError(
            f"The creation of EquivalentBranches is not supported by the OpenDssNetworkCreator."
            f" Tried to create EquivalentBranches {equivalent_branch.mrid}.")

    def power_transformer_creator(
            self,
            bus_branch_network: NetworkModel,
            power_transformer: PowerTransformer,
            ends_to_topological_nodes: List[Tuple[PowerTransformerEnd, Optional[Bus]]],
            node_breaker_network: NetworkService
    ) -> Dict[str, Transformer]:
        uid = power_transformer.mrid

        rating_kva = tx_rating(power_transformer, 234000.0) / 1000.0
        if power_transformer.function is TransformerFunctionKind.voltageRegulator:
            # TODO: this is done to figure out the end to use for the reg_controller as the end number is non-deterministic
            #  for regulators with our current data processing, once we make the bus-branch creator functionality sort terminals
            #  from upstream to downstream this should not be needed anymore.
            ends_to_topological_nodes = sorted(ends_to_topological_nodes, key=cmp_to_key(cmp_end_tn_by_t_direction))
            transformers_and_reg_controllers = {}
            nodes = max((bus for end, bus in ends_to_topological_nodes), key=lambda b: len(b.nodes)).nodes
            rating_kva = 1500 if rating_kva < 1000 else rating_kva

            for node in nodes:
                transformer = Transformer(
                    uid=f"{uid}_{str(node)}",
                    phases=1,
                    load_loss_percent=0.002,
                    xhl=0.007,
                    xht=None,
                    xlt=None,
                    windings=[TransformerWinding(
                        conn="wye",
                        kv=get_voltage_kv(end.rated_u, {node}, True),
                        kva=rating_kva,
                        bus_conn=BusConnection(bus, {node})
                    ) for end, bus in ends_to_topological_nodes]
                )
                bus_branch_network.add_transformer(transformer)
                transformers_and_reg_controllers[transformer.uid] = transformer

                reg_control = RegControl(
                    uid=f"{uid}_controller_{str(node)}",
                    transformer=transformer,
                    winding=len(transformer.windings),
                    vreg=vreg_from_nominal_v(list(power_transformer.ends)[0].nominal_voltage),
                    band=2,
                    ptratio=100,
                    ctprim=700,
                    r=2,
                    x=7
                )
                bus_branch_network.add_reg_control(reg_control)
                transformers_and_reg_controllers[reg_control.uid] = reg_control

            return transformers_and_reg_controllers
        else:
            is_swer = is_swer_tx(power_transformer)
            is_dist = is_dist_tx(power_transformer)
            num_phases = min([len(get_bus_nodes(end.terminal)) for end, t in ends_to_topological_nodes if end.terminal is not None])
            num_phases = 1 if num_phases < 3 else 3
            ends_to_topological_nodes = sorted(ends_to_topological_nodes, key=lambda end_tn: end_tn[0].end_number)

            if is_swer and is_dist:
                transformer = create_swer_tx(power_transformer, num_phases, rating_kva, ends_to_topological_nodes)
            else:
                transformer = create_tx(power_transformer, num_phases, rating_kva, ends_to_topological_nodes)

            bus_branch_network.add_transformer(transformer)
            return {transformer.uid: transformer}

    def energy_source_creator(
            self,
            bus_branch_network: NetworkModel,
            energy_source: EnergySource,
            connected_topological_node: Bus,
            node_breaker_network: NetworkService
    ) -> Dict[str, Circuit]:
        if bus_branch_network.circuit is not None:
            raise RuntimeError("Found multiple EnergySources while trying to create OpenDss model. Only one energy source is supported.")

        uid = energy_source.mrid
        circuit = Circuit(
            uid=uid,
            bus_conn=BusConnection(connected_topological_node, connected_topological_node.nodes),
            pu=self.vm_pu,
            base_kv=get_voltage_kv(energy_source.base_voltage.nominal_voltage, connected_topological_node.nodes),
            phases=len(connected_topological_node.nodes)
        )
        bus_branch_network.set_circuit(circuit)
        return {uid: circuit}

    def energy_consumer_creator(
            self, bus_branch_network: NetworkModel,
            energy_consumer: EnergyConsumer,
            connected_topological_node: Bus,
            node_breaker_network: NetworkService
    ) -> Dict[str, Load]:
        uid = energy_consumer.mrid
        nodes = {choice([n for n in connected_topological_node.nodes])} if len(connected_topological_node.nodes) == 2 else connected_topological_node.nodes
        connection_point = ConnectionPoint(
            uid=uid,
            bus_conn=BusConnection(connected_topological_node, nodes),
            kv=get_voltage_kv(energy_consumer.base_voltage.nominal_voltage, nodes),
            phases=len(nodes)
        )
        bus_branch_network.add_connection_point(connection_point)
        return {uid: connection_point}

    def power_electronics_connection_creator(
            self,
            bus_branch_network: NetworkModel,
            power_electronics_connection: PowerElectronicsConnection,
            connected_topological_node: Bus,
            node_breaker_network: NetworkService,
    ) -> Dict[str, Load]:
        uid = power_electronics_connection.mrid
        return {uid: None}

    def has_negligible_impedance(self, ce: ConductingEquipment) -> bool:
        if isinstance(ce, AcLineSegment):
            if ce.length == 0 or ce.per_length_sequence_impedance.r == 0:
                return True

            if ce.length * ce.per_length_sequence_impedance.r < self.min_line_r_ohm \
                    or ce.length * ce.per_length_sequence_impedance.x < self.min_line_x_ohm:
                return True

            return False
        if isinstance(ce, Switch):
            return not ce.is_open()
        if isinstance(ce, Junction) or isinstance(ce, BusbarSection) or isinstance(ce, EquivalentBranch):
            return True
        return False

    def validator_creator(self) -> OpenDssNetworkValidator:
        return OpenDssNetworkValidator(logger=self.logger)
