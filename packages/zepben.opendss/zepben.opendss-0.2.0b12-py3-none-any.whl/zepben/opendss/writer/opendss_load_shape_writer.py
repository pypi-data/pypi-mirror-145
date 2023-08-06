#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os.path
import sys
from typing import List, Dict
import logging

import aiofiles as aiof
import aiohttp
import ujson
from zepben.auth.client import create_token_fetcher

logger = logging.getLogger(__name__)

__all__ = ["OpenDssLoadShapeWriter"]


class OpenDssLoadShapeWriter:
    def __init__(self, output_dir: str, secure: bool = False, username: str = None, password: str = None,
                 client_id: str = None, host: str = None):
        self.secure = secure
        self.out_dir = output_dir
        if secure:
            authenticator = create_token_fetcher(f"https://{host}/ewb/auth")
            authenticator.token_request_data.update(
                {
                    "grant_type": "password",
                    "username": username,
                    "password": password,
                    "scope": "offline_access openid profile email",
                    "client_id": client_id
                }
            )
            authenticator.refresh_request_data.update({
                "grant_type": "refresh_token",
                "scope": "offline_access openid profile email",
                "client_id": client_id
            })

            self.token = authenticator.fetch_token()
        else:
            self.token = ''

    async def get_load_profile(self, from_asset: str, from_date: str, to_date: str, host: str, port: int) -> List[Dict]:
        async with aiohttp.ClientSession(headers={'Authorization': self.token}, json_serialize=ujson.dumps) as session:
            async with session.get(url=
                                   f'{"https" if self.secure else "http"}://{host}:{port}/ewb/energy/profiles/api/v1/range/{from_asset}'
                                   f'/from-date/{from_date}'
                                   f'/to-date/{to_date}'
                                   ) as response:
                return (await response.json())["results"] if response.status == 200 else []

    @staticmethod
    def create_load_shape(load_profile):
        max_value = sys.float_info.min
        load_shape = []
        zero_count = 0
        days_replaced = 0
        try:
            for s in load_profile[0]["series"][0]:
                for entry in s["energy"]["readings"]:
                    if abs(entry["values"]["kwNet"]) > max_value:
                        max_value = abs(entry["values"]["kwNet"])

            for s in load_profile[0]["series"][0]:
                for entry in s["energy"]["readings"]:
                    load_shape.append(f'{entry["values"]["kwNet"] / max_value}\n')
                    if entry["values"]["kwNet"] == 0:
                        zero_count += 1
                        # Once 48 reading of 0 is accumulated, it is replaced with previous day's readings
                        if zero_count == 48:
                            for c in range(48):
                                load_shape[-(48 - c)] = load_shape[-(96 - c)]
                            days_replaced += 1
                            zero_count = 0
                    else:
                        # This route will patch non full day zero readings just in case
                        # Compensate for leading 2 0.0 readings
                        if zero_count > 0 and len(load_shape) > 3:
                            difference = (float(load_shape[-1]) - float(load_shape[-(zero_count+2)]))/(zero_count+1)
                            for i in range(zero_count):
                                load_shape[-(zero_count+1-i)] = str(float(load_shape[-(zero_count+2-i)]) + difference) + '\n'
                        zero_count = 0
        except IndexError:
            # Empty Feeder
            pass
        # Normalize to 365 days a year
        if len(load_shape) > 17520:
            difference = len(load_shape)-17520
            del load_shape[:difference]
        return load_shape, max_value

    async def write_load_shape_to_txt(self, feeder: str, target: str, load_shape: List[str]):
        if len(load_shape) != 0:
            base_folder = f'{self.out_dir}/{feeder}/base/'
            if not os.path.exists(base_folder):
                os.makedirs(base_folder)

            async with aiof.open(f'{base_folder}{target}.txt', 'w', encoding='ascii') as f:
                await f.writelines(load_shape)
                await f.close()
