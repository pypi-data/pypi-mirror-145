#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Union

__all__ = ["TransformerWinding", "Transformer"]

from zepben.opendss import BusConnection


class TransformerWinding:

    def __init__(
            self,
            conn: str,
            kv: float,
            kva: float,
            bus_conn: BusConnection,
            tap: Union[float, None] = None
    ):
        self.conn = conn
        self.kv = kv
        self.kva = kva
        self.bus_conn = bus_conn
        self.tap = tap


class Transformer:

    def __init__(
            self,
            uid: str,
            phases: int,
            load_loss_percent: float,
            xhl: float,
            xht: Union[float, None],
            xlt: Union[float, None],
            windings: List[TransformerWinding],
    ):
        self.uid = uid
        self.phases = phases
        self.load_loss_percent = load_loss_percent
        self.xhl = xhl
        self.xht = xht
        self.xlt = xlt
        self.windings = windings
