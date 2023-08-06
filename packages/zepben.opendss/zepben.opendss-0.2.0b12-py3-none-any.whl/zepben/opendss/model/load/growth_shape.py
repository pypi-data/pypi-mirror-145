#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

__all__: ["GrowthShape"]


class GrowthShape:
    def __init__(self, uid: str, shape: List[float]):
        self.uid = uid
        self.shape = shape
