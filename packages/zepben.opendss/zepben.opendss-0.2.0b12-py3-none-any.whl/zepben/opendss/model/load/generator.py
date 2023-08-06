#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Optional

from zepben.opendss import GrowthShape
from zepben.opendss.model.load.load_shape import LoadShape
from zepben.opendss.model.load.power_conversion_element import PowerConversionElement

__all__ = ["Generator"]


class Generator(PowerConversionElement):

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
        super().__init__(uid, connection_point_uid, 7, kw, pf, load_shape, growth_shape, enabled=enabled)
