#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.opendss.model.network.bus import BusConnection
from zepben.opendss.model.network.line_code import LineCode

__all__ = ["Line"]


class Line:

    def __init__(
            self,
            uid: str,
            units: str,
            length: float,
            bus_conn1: BusConnection,
            bus_conn2: BusConnection,
            line_code: LineCode
    ):
        self.uid = uid
        self.units = units
        self.length = length
        self.bus_conn1 = bus_conn1
        self.bus_conn2 = bus_conn2
        self.line_code = line_code
