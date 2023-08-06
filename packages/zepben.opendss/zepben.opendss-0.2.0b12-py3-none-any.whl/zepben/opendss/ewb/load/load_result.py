#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
from datetime import date
from typing import List, Dict

import aiohttp

__all__ = ["EwbLoadShapeInfoProvider"]

from aiohttp import ClientSession

from zepben.opendss import LoadShapeInfoProvider, LoadShapeInfo

_load_api_date_format = "%Y-%m-%d"


class EwbLoadShapeInfoProvider(LoadShapeInfoProvider):

    def __init__(self, session: ClientSession = None, base_url=None, json_serialiser=None):
        if not session:
            if not base_url:
                raise ValueError("base_url must be provided if not providing a session - it should be the host and port of EWB only")
            conn = aiohttp.TCPConnector(limit=200, limit_per_host=0)
            timeout = aiohttp.ClientTimeout(total=60)
            self.session = aiohttp.ClientSession(base_url=base_url, json_serialize=json_serialiser if json_serialiser is not None else json.dumps,
                                                 connector=conn, timeout=timeout)
        else:
            self.session = session

    async def get_load_shape_info(self, conducting_equipment_mrid: str, from_date: date, to_date: date) -> LoadShapeInfo:
        load_result = await self._get_load_profile(conducting_equipment_mrid, from_date, to_date)

        max_abs_val = 0
        zero_count = 0
        days_replaced = 0
        values = []
        for result in load_result:
            for series in result["series"]:
                for series_item in series:
                    for reading in series_item['energy']["readings"]:
                        val = reading["values"]["kwNet"]
                        abs_val = abs(val)
                        if abs_val > max_abs_val:
                            max_abs_val = abs_val
                        values.append(val)
                        if val == 0:
                            zero_count += 1
                            # Once 48 reading of 0 is accumulated, it is replaced with previous day's readings
                            if zero_count == 48 and zero_count != len(values):
                                for c in range(48):
                                    values[-(48 - c)] = values[-(96 - c)]
                                days_replaced += 1
                                zero_count = 0
                        else:
                            # This route will patch non full day zero readings just in case
                            # This route replace all 0 at the start of loadshape with first reading
                            if zero_count > 0 and zero_count == (len(values) - 1):
                                for i in range(zero_count):
                                    values[-(i + 1)] = values[-1]
                            elif zero_count > 0:
                                difference = (float(values[-1]) - float(values[-(zero_count + 2)])) / (zero_count + 1)
                                for i in range(zero_count):
                                    values[-(zero_count + 1 - i)] = float(values[-(zero_count + 2 - i)]) + difference
                            zero_count = 0
        return LoadShapeInfo(max_abs_val, 1.0, [1 if max_abs_val == 0 else v / max_abs_val for v in values], 0.5)

    async def _get_load_profile(self, from_asset_mrid: str, from_date: date, to_date: date) -> List[Dict]:
        url = f'/ewb/energy/profiles/api/v1/range/{from_asset_mrid}/from-date/{from_date.isoformat()}/to-date/{to_date.isoformat()}'
        async with self.session.get(url=url) as response:
            return (await response.json())["results"] if response.status == 200 else []
