#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import date
from typing import Dict, Callable, Set

from zepben.opendss import NetworkModel
from zepben.opendss.model.load.generator import Generator
from zepben.opendss.model.load.growth_shape import GrowthShape
from zepben.opendss.model.load.load import LoadShapeInfoProvider, Load
from zepben.opendss.model.load.load_shape import LoadShape
from zepben.opendss.model.load.power_conversion_element import PowerConversionElement

__all__ = ["LoadModel", "single_point_load_model", "load_model_from_load_shape_info_provider", "update_loads_in_model"]


class LoadModel:

    def __init__(
            self,
            network: NetworkModel,
            loads: Dict[str, Load] = None,
            generators: Dict[str, Generator] = None,
            load_shapes: Dict[str, LoadShape] = None,
            growth_shapes: Dict[str, GrowthShape] = None
    ):
        self.network = network
        self.loads = {} if loads is None else loads
        self.generators = {} if generators is None else generators
        self.load_shapes = {} if load_shapes is None else load_shapes
        self.growth_shapes = {} if growth_shapes is None else growth_shapes
        self._loads_by_conn_point_uid: Dict[str, Set[Load]] = {load.connection_point_uid: load for load in self.loads.values()}
        self._generators_by_conn_point_uid: Dict[str, Set[Generator]] = {generator.connection_point_uid: generator for generator in self.generators.values()}

    def get_loads_by_conn_point_uid(self, conn_point_uid: str) -> Set[Load]:
        return self._loads_by_conn_point_uid.get(conn_point_uid, set())

    def add_load(self, load: Load):
        self._verify_power_conversion_element_refs(load)
        LoadModel._add_refs_for_pce(self._loads_by_conn_point_uid, load)
        self.loads[load.uid] = load

    def remove_load(self, uid: str):
        if uid in self.loads:
            LoadModel._remove_refs_for_pce(self._loads_by_conn_point_uid, self.loads[uid])
            del self.loads[uid]

    def get_generators_by_cnn_point_uid(self, conn_point_uid: str) -> Set[Generator]:
        return self._generators_by_conn_point_uid.get(conn_point_uid, set())

    def add_generator(self, generator: Generator):
        self._verify_power_conversion_element_refs(generator)
        LoadModel._add_refs_for_pce(self._generators_by_conn_point_uid, generator)
        self.generators[generator.uid] = generator

    def remove_generator(self, uid: str):
        if uid in self.generators:
            LoadModel._remove_refs_for_pce(self._generators_by_conn_point_uid, self.generators[uid])
            del self.generators[uid]

    def _verify_power_conversion_element_refs(self, pce: PowerConversionElement):
        if pce.connection_point_uid not in self.network.connection_points:
            raise ReferenceError(f"No connection point found with uid {pce.connection_point_uid}.")
        if pce.load_shape is not None and pce.load_shape.uid not in self.load_shapes.keys():
            raise ReferenceError(f"No load shape found with uid {pce.load_shape.uid}.")
        if pce.growth_shape is not None and pce.growth_shape.uid not in self.growth_shapes.keys():
            raise ReferenceError(f"No growth shape found with uid {pce.growth_shape.uid}.")

    @staticmethod
    def _add_refs_for_pce(ref_dictionary: Dict[str, Set[PowerConversionElement]], element: PowerConversionElement):
        if element.connection_point_uid not in ref_dictionary:
            ref_dictionary[element.connection_point_uid] = set()
        ref_dictionary[element.connection_point_uid].add(element)

    @staticmethod
    def _remove_refs_for_pce(ref_dictionary: Dict[str, Set[PowerConversionElement]], element: PowerConversionElement):
        if element.connection_point_uid not in ref_dictionary:
            return

        elements = ref_dictionary[element.connection_point_uid]
        elements.remove(element)

        if len(elements) == 0:
            del ref_dictionary[element.connection_point_uid]

    def add_load_shape(self, load_shape: LoadShape):
        self.load_shapes[load_shape.uid] = load_shape

    def remove_load_shape(self, uid: str):
        del self.load_shapes[uid]

    def add_growth_shape(self, growth_shape: GrowthShape):
        self.growth_shapes[growth_shape.uid] = growth_shape

    def remove_growth_shape(self, uid: str):
        del self.growth_shapes[uid]

    def copy(self):
        raise NotImplementedError("Copy method is not implemented")


def single_point_load_model(network_model: NetworkModel, kw: float, pf: float) -> LoadModel:
    load_model = LoadModel(network_model)
    for conn in network_model.connection_points.values():
        load_model.add_load(Load(uid=f"{conn.uid}_LOAD", connection_point_uid=conn.uid, kw=kw, pf=pf))
    return load_model


async def load_model_from_load_shape_info_provider(load_shape_info_provider: LoadShapeInfoProvider, from_date: date, to_date: date,
                                                   network_model: NetworkModel) -> LoadModel:
    load_model = LoadModel(network_model)
    for conn_point in network_model.connection_points.values():
        await _add_to_load_model(load_model, load_shape_info_provider, conn_point.uid, from_date, to_date)
    return load_model


async def _add_to_load_model(load_model: LoadModel, load_shape_info_provider: LoadShapeInfoProvider, conn_point_uid: str, from_date: date, to_date: date):
    load_shape_info = await load_shape_info_provider.get_load_shape_info(conn_point_uid, from_date, to_date)

    load_shape = None
    if len(load_shape_info.shape) != 0:
        load_shape = LoadShape(
            uid=f"{conn_point_uid}_SHAPE",
            shape=load_shape_info.shape,
            interval=load_shape_info.interval
        )
        load_model.add_load_shape(load_shape)

    load_model.add_load(
        Load(
            uid=f"{conn_point_uid}_LOAD",
            connection_point_uid=conn_point_uid,
            kw=load_shape_info.kw,
            pf=load_shape_info.pf,
            load_shape=load_shape
        )
    )


def update_loads_in_model(load_model: LoadModel, load_updater: Callable[[Load], None], load_filter: Callable[[Load], bool] = lambda _: True):
    for load in load_model.loads.values():
        if load_filter(load):
            load_updater(load)
