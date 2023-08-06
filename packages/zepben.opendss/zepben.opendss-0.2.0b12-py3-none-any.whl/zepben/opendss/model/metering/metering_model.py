#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.


__all__ = ["MeteringModel", "get_basic_metering_model"]

from typing import Dict

from zepben.opendss import EnergyMeter, NetworkModel, TargetElement, Monitor


class MeteringModel:

    def __init__(
            self,
            network: NetworkModel,
            energy_meters: Dict[str, EnergyMeter] = None,
            monitors: Dict[str, Monitor] = None
    ):
        self.network = network
        self.energy_meters = {} if energy_meters is None else energy_meters
        self.monitors = {} if monitors is None else monitors

    def add_energy_meter(self, energy_meter: EnergyMeter):
        self._validate_element_ref(energy_meter.element)
        self.energy_meters[energy_meter.uid] = energy_meter

    def add_monitor(self, monitor: Monitor):
        self._validate_element_ref(monitor.element)
        self.monitors[monitor.uid] = monitor

    def _validate_element_ref(self, element: TargetElement):
        line_uids = self.network.lines.keys()
        transformer_uids = self.network.transformers.keys()
        load_connection_uids = self.network.connection_points.keys()
        if element.uid not in load_connection_uids \
                and element.uid not in line_uids \
                and element.uid not in transformer_uids:
            raise ReferenceError(f"No element found with uid {element.uid}.")

    def remove_energy_meter(self, uid: str):
        del self.energy_meters[uid]

    def remove_monitor(self, uid: str):
        del self.monitors[uid]

    def copy(self):
        raise NotImplementedError("Copy method is not implemented")


def get_basic_metering_model(network_model: NetworkModel, feeder_mrid: str) -> MeteringModel:
    metering_model = MeteringModel(network_model)

    lines_connected_to_feeder_head = [ln for ln in network_model.lines.values()
                                      if ln.bus_conn1.bus == network_model.circuit.bus_conn.bus or ln.bus_conn2.bus == network_model.circuit.bus_conn.bus]

    for ln in lines_connected_to_feeder_head:
        t_element = TargetElement(
            uid=ln.uid,
            element_type="Line"
        )
        if feeder_mrid in ln.bus_conn1.bus.uid:
            line_terminal = 1
        else:
            line_terminal = 2
        metering_model.add_monitor(Monitor(uid=f"{t_element.uid}_monitor", element=t_element, mode=1))
        metering_model.add_energy_meter(EnergyMeter(uid=f"{t_element.uid}_em", element=t_element, term=line_terminal))

    for transformer in network_model.transformers.values():
        if any(w.kv < 1 for w in transformer.windings):
            check = 0
            index = 0
            for w in transformer.windings:
                if w.kv > check:
                    check = w.kv
                    index = transformer.windings.index(w)
            metering_model.add_energy_meter(
                EnergyMeter(
                    uid=f"{transformer.uid}_em",
                    element=TargetElement(
                        uid=transformer.uid,
                        element_type="Transformer"
                    ),
                    term=index + 1
                )
            )
    return metering_model
