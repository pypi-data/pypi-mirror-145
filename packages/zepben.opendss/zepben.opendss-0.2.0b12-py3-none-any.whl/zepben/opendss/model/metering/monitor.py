#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.opendss.model.metering.target_element import TargetElement

__all__ = ["Monitor"]


class Monitor:

    def __init__(
            self,
            uid: str,
            element: TargetElement,
            mode: int
    ):
        self.uid = uid
        self.element = element
        self.mode = mode
