#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List, Optional, Dict

from zepben.opendss import NetworkModel
from zepben.opendss.model.load.load_model import LoadModel
from zepben.opendss.model.metering.metering_model import MeteringModel

__all__ = ["Master", "YearConfig", "PceEnableTarget"]


class PceEnableTarget:

    def __init__(
            self,
            uid: str,
            pce_type: str  # valid strings: "Load", "Generator"
    ):
        self.uid = uid
        self.pce_type = pce_type


class YearConfig:

    def __init__(
            self,
            enable_pce_targets: Optional[List[PceEnableTarget]] = None,
            disable_pce_targets: Optional[List[PceEnableTarget]] = None
    ):
        self.enable_pce_targets = [] if enable_pce_targets is None else enable_pce_targets
        self.disable_pce_targets = [] if disable_pce_targets is None else disable_pce_targets


class Master:

    def __init__(
            self,
            network_model: NetworkModel,
            load_model: LoadModel,
            metering_model: MeteringModel,
            yearly_config: Dict[int, YearConfig] = None
    ):
        self.network_model = network_model
        self.load_model = load_model
        self.metering_model = metering_model
        self.yearly_config = {} if yearly_config is None else yearly_config

    def get_year_config(self, year: int) -> Optional[YearConfig]:
        return self.yearly_config.get(year)

    def add_year_config(self, year: int, year_config: YearConfig):
        self.yearly_config[year] = year_config

    def remove_year_config(self, year: int):
        del self.yearly_config[year]
