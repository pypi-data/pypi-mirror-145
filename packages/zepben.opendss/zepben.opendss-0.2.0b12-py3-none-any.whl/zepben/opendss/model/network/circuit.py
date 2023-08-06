#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Circuit"]

from zepben.opendss import BusConnection


class Circuit:

    def __init__(
            self,
            uid: str,
            bus_conn: BusConnection,
            pu: float,
            base_kv: float,
            phases: int
    ):
        self.uid = uid
        self.bus_conn = bus_conn
        self.pu = pu
        self.base_kv = base_kv
        self.phases = phases
