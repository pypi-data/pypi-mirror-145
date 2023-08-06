#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["LineCode"]


class LineCode:

    def __init__(
            self,
            uid: str,
            units: str,
            nphases: int,
            norm_amps: float,
            emerg_amps: float,
            r1: float,
            r0: float,
            x1: float,
            x0: float,
            b1: float,
            b0: float
    ):
        self.uid = uid
        self.units = units
        self.nphases = nphases
        self.norm_amps = norm_amps
        self.emerg_amps = emerg_amps
        self.r1 = r1
        self.r0 = r0
        self.x1 = x1
        self.x0 = x0
        self.b1 = b1
        self.b0 = b0
