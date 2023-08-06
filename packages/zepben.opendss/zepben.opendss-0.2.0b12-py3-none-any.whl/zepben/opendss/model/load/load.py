#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import abc
from datetime import date
from typing import List, Optional

from zepben.opendss import ConnectionPoint, GrowthShape
from zepben.opendss.model.load.load_shape import LoadShape
from zepben.opendss.model.load.power_conversion_element import PowerConversionElement

__all__ = ["Load", "zero_load_point", "LoadShapeInfo", "LoadShapeInfoProvider"]


class Load(PowerConversionElement):

    def __init__(
            self,
            uid: str,
            connection_point_uid: str,
            kw: float,
            pf: float,
            load_shape: Optional[LoadShape] = None,
            growth_shape: Optional[GrowthShape] = None,
            *,
            enabled: bool = True
    ):
        super().__init__(uid, connection_point_uid, 1, kw, pf, load_shape, growth_shape, enabled=enabled)


def zero_load_point(conn_point: ConnectionPoint):
    return Load(uid=f"{conn_point}_LOAD", connection_point_uid=conn_point.uid, kw=0.0, pf=1.0)


class LoadShapeInfo:

    def __init__(self, kw: float, pf: float, shape: List[float], interval: float):
        self.kw = kw
        self.pf = pf
        self.shape = shape
        self.interval = interval


class LoadShapeInfoProvider(metaclass=abc.ABCMeta):

    async def get_load_shape_info(self, conducting_equipment_mrid: str, from_date: date, to_date: date) -> LoadShapeInfo:
        raise NotImplementedError
