#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["transformer_end_connection_mapper", "id_from_identified_objects", "get_bus_nodes", "tx_rating", "vreg_from_nominal_v", "get_voltage_kv",
           "load_loss_percent", "tx_bus_connection", "cmp_end_tn_by_t_direction", "closest_connected_nodes", "is_swer_tx", "is_dist_tx", "create_tx",
           "create_swer_tx"]

import random
from math import sqrt, log
from typing import TypeVar, Collection, Set, Union, Tuple, List

from zepben.evolve import PowerTransformerEnd, SinglePhaseKind, WindingConnection, IdentifiedObject, Terminal, PowerTransformer, FeederDirection

from zepben.opendss import Node, Bus, BusConnection, Transformer, TransformerWinding

T = TypeVar("T")


def transformer_end_connection_mapper(transformer_end: PowerTransformerEnd):
    if transformer_end.connection_kind == WindingConnection.D:
        return "delta"
    elif transformer_end.connection_kind == WindingConnection.Y:
        return "wye"
    else:
        # TODO: There are tons of windings missing here, if we throw for anything other than D and Y then this won't run on anywhere
        return "delta" if transformer_end.end_number == 1 else "wye"
        # raise Exception(f'WindingConnection {transformer_end.connection_kind} is not supported for '
        #                 f'TransformerEnd: {transformer_end.mrid}')


def id_from_identified_objects(ios: Collection[IdentifiedObject], separator: str = "__"):
    return separator.join(sorted(io.mrid for io in ios))


spk_to_node = {
    SinglePhaseKind.A: Node.A,
    SinglePhaseKind.B: Node.B,
    SinglePhaseKind.C: Node.C
}


def get_bus_nodes(t: Terminal) -> Set[Node]:
    if t is None:
        return set()
    return {n for n in {spk_to_node.get(t.traced_phases.normal(sp)) for sp in t.phases.single_phases} if n is not None}


def tx_rating(pt: PowerTransformer, default_rating: float = None):
    rating = None
    for end in pt.ends:
        if end.rated_s is not None and end.rated_s != 0:
            rating = end.rated_s

    if rating is None:
        if pt.power_transformer_info is not None:
            for tank_info in pt.power_transformer_info.transformer_tank_infos:
                for end_info in tank_info.transformer_end_infos:
                    if end_info.rated_s is not None and end_info.rated_s != 0:
                        rating = end_info.rated_s

    if rating is None and default_rating is not None:
        rating = default_rating

    return rating


# NOTE: Input Needs to be nominal voltage in Volts
def vreg_from_nominal_v(nominal_voltage: int):
    m = 0.0059090909
    ltg_ltl = {19100: 33000, 12700: 22000, 6350: 11000}
    return round(ltg_ltl.get(nominal_voltage, nominal_voltage) * m, 1)


def get_voltage_kv(base_voltage: Union[int, None], nodes: Union[Set[Node], None], force_line_to_ground: bool = False):
    if base_voltage is None:
        return 0.0

    if base_voltage == 19100 or base_voltage == 12700 or base_voltage == 6350:
        return round(base_voltage / 1000, 3)

    if force_line_to_ground:
        return round(base_voltage / sqrt(3) / 1000.0, 3)

    return round((base_voltage / sqrt(3) if nodes is not None and len(list(nodes)) == 1 and base_voltage < 1000 else base_voltage) / 1000.0, 3)


def load_loss_percent(rating_kva: float):
    if rating_kva == 0:
        return 0.0
    value = -0.288 * log(rating_kva) + 2.4293
    if value > 2.2:
        return 2.2
    elif value < 0.5:
        return 0.5
    else:
        return value


def tx_bus_connection(
        power_transformer: PowerTransformer,
        end: PowerTransformerEnd,
        num_phases: int,
        bus: Union[Bus, None]
):
    end_to_nodes = {end.mrid: get_bus_nodes(end.terminal) for end in power_transformer.ends}
    nodes = end_to_nodes.get(end.mrid)

    return BusConnection(Bus(f"{power_transformer.mrid}-disconnected-end-{end.end_number}", nodes=set()) if bus is None else bus, nodes)


def cmp_end_tn_by_t_direction(end_tn1: Tuple[PowerTransformerEnd, Bus], end_tn2: Tuple[PowerTransformerEnd, Bus]):
    end1, tn1 = end_tn1
    end2, tn2 = end_tn2

    if tn1 is not None and end1 is not None:
        if end1.terminal.normal_feeder_direction.has(FeederDirection.UPSTREAM):
            return -1

    if tn2 is not None and end2 is not None:
        return 1

    return 0


def closest_connected_nodes(terminal: Terminal) -> Set[Node]:
    if terminal is None:
        return set()

    if terminal.connectivity_node is None:
        return get_bus_nodes(terminal)

    o_nodes = None
    for ot in terminal.connectivity_node.terminals:
        if ot != terminal:
            o_nodes = get_bus_nodes(ot)

    if o_nodes is None:
        return get_bus_nodes(terminal)
    else:
        return o_nodes


def is_swer_tx(pt: PowerTransformer) -> bool:
    return any(end.nominal_voltage == 19100 or end.nominal_voltage == 12700 or end.nominal_voltage == 6350 for end in pt.ends)


def is_dist_tx(pt: PowerTransformer) -> bool:
    return any(end.nominal_voltage < 1000 for end in pt.ends)


def create_tx(power_transformer: PowerTransformer, num_phases: int, rating_kva: float,
              ends_to_topological_nodes: List[Tuple[PowerTransformerEnd, Bus]]) -> Transformer:
    return Transformer(
        uid=power_transformer.mrid,
        phases=num_phases,
        load_loss_percent=load_loss_percent(rating_kva),
        xhl=4,
        xht=None,
        xlt=None,
        windings=[TransformerWinding(
            conn=transformer_end_connection_mapper(end),
            kv=get_voltage_kv(end.rated_u, bus.nodes if bus is not None else None),
            kva=rating_kva,
            bus_conn=tx_bus_connection(power_transformer, end, num_phases, bus)
        ) for end, bus in ends_to_topological_nodes]
    )


def create_swer_tx(power_transformer: PowerTransformer, num_phases: int, rating_kva: float,
                   ends_to_topological_nodes: List[Tuple[PowerTransformerEnd, Bus]]) -> Transformer:
    transformer = Transformer(
        uid=power_transformer.mrid,
        phases=num_phases,
        load_loss_percent=0.4,
        xhl=3.54,
        xht=3.54,
        xlt=2.36,
        windings=[TransformerWinding(
            conn=transformer_end_connection_mapper(end),
            kv=get_voltage_kv(end.rated_u, bus.nodes if bus is not None else None),
            kva=rating_kva,
            bus_conn=tx_bus_connection(power_transformer, end, num_phases, bus)
        ) for end, bus in ends_to_topological_nodes]
    )
    secondary = transformer.windings[len(transformer.windings) - 1]
    # TODO: We hard code 0.25kV for second and third winding on swer-dist transformer because essential wants this.
    #  This should be reviewed and removed in the future because hard-coding values this way independently of source data
    #  leads to non-reusable functionality between customers.
    secondary.kv = 0.25
    transformer.windings.append(
        TransformerWinding(
            secondary.conn,
            secondary.kv,
            secondary.kva,
            BusConnection(
                secondary.bus_conn.bus,
                {Node.G, _get_other_node(next(iter(secondary.bus_conn.connections)))} if len(secondary.bus_conn.connections) != 0 else {},
                validate=False
            )
        )
    )
    return transformer


def _get_other_node(node: Node):
    nodes = {Node.A, Node.B, Node.C}
    nodes.remove(node)
    return random.choice([n for n in nodes])
