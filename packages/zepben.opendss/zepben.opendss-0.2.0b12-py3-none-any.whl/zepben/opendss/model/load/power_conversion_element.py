#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import abc
from typing import Optional

from zepben.opendss import GrowthShape
from zepben.opendss.model.load.load_shape import LoadShape

__all__ = ["PowerConversionElement"]


class PowerConversionElement(metaclass=abc.ABCMeta):
    def __init__(
            self,
            uid: str,
            connection_point_uid: str,
            model: int,
            kw: float,
            pf: float,
            load_shape: Optional[LoadShape] = None,
            growth_shape: Optional[GrowthShape] = None,
            *,
            enabled: bool = True
    ):
        self.uid = uid
        self.connection_point_uid = connection_point_uid
        self.model = model
        self.kw = kw
        self.pf = pf
        self.load_shape = load_shape
        self.growth_shape = growth_shape
        self.enabled = enabled
