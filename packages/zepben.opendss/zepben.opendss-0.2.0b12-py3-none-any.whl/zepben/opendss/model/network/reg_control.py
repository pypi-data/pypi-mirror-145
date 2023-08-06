#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.opendss import Transformer

__all__ = ["RegControl"]


class RegControl:

    def __init__(
            self,
            uid: str,
            transformer: Transformer,
            winding: int,
            vreg: float,
            band: float,
            ptratio: int,
            ctprim: int,
            r: float,
            x: float
    ):
        self.uid = uid
        self.transformer = transformer
        self.winding = winding
        self.vreg = vreg
        self.band = band
        self.ptratio = ptratio
        self.ctprim = ctprim
        self.r = r
        self.x = x
