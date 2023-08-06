#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os.path
from pathlib import Path
from typing import Callable, Set, Tuple, Collection
from typing import TypeVar, List

import aiofiles as aiof

from zepben.opendss import Line, LineCode, EnergyMeter, Transformer, TransformerWinding, Load, ConnectionPoint, Monitor, GrowthShape
from zepben.opendss.model.load.generator import Generator
from zepben.opendss.model.load.load_shape import LoadShape
from zepben.opendss.model.load.power_conversion_element import PowerConversionElement
from zepben.opendss.model.master import Master, PceEnableTarget
from zepben.opendss.model.network.bus import Node, BusConnection
from zepben.opendss.model.network.reg_control import RegControl

__all__ = ["OpenDssWriter"]


class OpenDssWriter:

    @staticmethod
    async def write(dir_path_str: str, master: Master):
        model_dir = Path(dir_path_str)

        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        if not model_dir.is_dir():
            raise ValueError(f"The argument '{dir_path_str}' for the dir_path_str parameter was not a directory")

        # -- Network Model --
        if OpenDssWriter.has_lines(master):
            await OpenDssWriter.write_lines_file(model_dir, master)

        if OpenDssWriter.has_line_codes(master):
            await OpenDssWriter.write_line_codes_file(model_dir, master)

        if OpenDssWriter.has_transformers(master):
            await OpenDssWriter.write_transformers_file(model_dir, master)

        if OpenDssWriter.has_reg_controls(master):
            await OpenDssWriter.write_reg_controls_file(model_dir, master)

        # -- Load Model --
        if OpenDssWriter.has_loads(master):
            await OpenDssWriter.write_loads_file(model_dir, master)

        if OpenDssWriter.has_generators(master):
            await OpenDssWriter.write_generators_file(model_dir, master)

        if OpenDssWriter.has_load_shapes(master):
            await OpenDssWriter.write_load_shape_files(model_dir, master)

        if OpenDssWriter.has_growth_shapes(master):
            await OpenDssWriter.write_growth_shape_file(model_dir, master)

        # -- Metering Model --
        if OpenDssWriter.has_energy_meters(master):
            await OpenDssWriter.write_energy_meter_file(model_dir, master)

        if OpenDssWriter.has_monitors(master):
            await OpenDssWriter.write_monitor_file(model_dir, master)

        if OpenDssWriter.has_yearly_config(master):
            await OpenDssWriter.write_yearly_config_files(model_dir, master)

        # -- Master --
        await OpenDssWriter.write_master_file(model_dir=model_dir, master=master)

    @staticmethod
    def has_lines(master: Master) -> bool:
        return OpenDssWriter.has_elements(master.network_model.lines)

    @staticmethod
    def has_line_codes(master: Master) -> bool:
        return OpenDssWriter.has_elements(master.network_model.line_codes)

    @staticmethod
    def has_transformers(master: Master) -> bool:
        return OpenDssWriter.has_elements(master.network_model.transformers)

    @staticmethod
    def has_reg_controls(master: Master) -> bool:
        return OpenDssWriter.has_elements(master.network_model.reg_controls)

    @staticmethod
    def has_loads(master: Master) -> bool:
        return OpenDssWriter.has_elements(master.load_model.loads)

    @staticmethod
    def has_generators(master: Master) -> bool:
        return OpenDssWriter.has_elements(master.load_model.generators)

    @staticmethod
    def has_load_shapes(master: Master) -> bool:
        return OpenDssWriter.has_elements(master.load_model.load_shapes)

    @staticmethod
    def has_growth_shapes(master: Master) -> bool:
        return OpenDssWriter.has_elements(master.load_model.growth_shapes)

    @staticmethod
    def has_energy_meters(master: Master) -> bool:
        return OpenDssWriter.has_elements(master.metering_model.energy_meters)

    @staticmethod
    def has_monitors(master: Master) -> bool:
        return OpenDssWriter.has_elements(master.metering_model.monitors)

    @staticmethod
    def has_yearly_config(master: Master) -> bool:
        return OpenDssWriter.has_elements(master.yearly_config)

    @staticmethod
    def has_elements(collection: Collection) -> bool:
        return collection.__len__() != 0

    @staticmethod
    async def write_lines_file(model_dir: Path, master: Master):
        await OpenDssWriter.write_elements_to_file(
            model_dir / 'Lines.dss',
            lambda: master.network_model.lines.values(),
            OpenDssWriter.line_to_str
        )

    @staticmethod
    async def write_line_codes_file(model_dir: Path, master: Master):
        await OpenDssWriter.write_elements_to_file(
            model_dir / 'LineCodes.dss',
            lambda: master.network_model.line_codes.values(),
            OpenDssWriter.line_code_to_str
        )

    @staticmethod
    async def write_transformers_file(model_dir: Path, master: Master):
        await OpenDssWriter.write_elements_to_file(
            model_dir / 'Transformers.dss',
            lambda: master.network_model.transformers.values(),
            OpenDssWriter.transformer_to_str
        )

    @staticmethod
    async def write_reg_controls_file(model_dir: Path, master: Master):
        await OpenDssWriter.write_elements_to_file(
            model_dir / 'RegControls.dss',
            lambda: master.network_model.reg_controls.values(),
            OpenDssWriter.reg_control_to_str
        )

    @staticmethod
    async def write_loads_file(model_dir: Path, master: Master):
        await OpenDssWriter.write_elements_to_file(
            model_dir / 'Loads.dss',
            lambda: [(conn_point, load)
                     for conn_point in master.network_model.connection_points.values()
                     for load in master.load_model.get_loads_by_conn_point_uid(conn_point.uid)],
            OpenDssWriter.conn_point_load_to_str
        )

    @staticmethod
    async def write_generators_file(model_dir: Path, master: Master):
        await OpenDssWriter.write_elements_to_file(
            model_dir / 'Generators.dss',
            lambda: [(conn_point, generator)
                     for conn_point in master.network_model.connection_points.values()
                     for generator in master.load_model.get_generators_by_cnn_point_uid(conn_point.uid)],
            OpenDssWriter.conn_point_generator_to_str
        )

    @staticmethod
    async def write_load_shape_files(model_dir: Path, master: Master):
        await OpenDssWriter.write_elements_to_file(
            model_dir / 'LoadShapes.dss',
            lambda: master.load_model.load_shapes.values(),
            OpenDssWriter.load_shape_to_str
        )

        for load_shape in master.load_model.load_shapes.values():
            if len(load_shape.shape) != 0:
                await OpenDssWriter.write_mult_file(model_dir, load_shape)

    @staticmethod
    async def write_mult_file(model_dir: Path, load_shape: LoadShape):
        await OpenDssWriter.write_elements_to_file(
            model_dir / f'{load_shape.uid}.txt',
            lambda: load_shape.shape,
            lambda n: str(n)
        )

    @staticmethod
    async def write_growth_shape_file(model_dir: Path, master: Master):
        await OpenDssWriter.write_elements_to_file(
            model_dir / 'GrowthShapes.dss',
            lambda: master.load_model.growth_shapes.values(),
            OpenDssWriter.growth_shape_to_str
        )

    @staticmethod
    async def write_energy_meter_file(model_dir: Path, master: Master):
        await OpenDssWriter.write_elements_to_file(
            model_dir / 'EnergyMeters.dss',
            lambda: master.metering_model.energy_meters.values(),
            OpenDssWriter.energy_meter_to_str
        )

    @staticmethod
    async def write_monitor_file(model_dir: Path, master: Master):
        await OpenDssWriter.write_elements_to_file(
            model_dir / 'Monitors.dss',
            lambda: master.metering_model.monitors.values(),
            OpenDssWriter.monitor_to_str
        )

    @staticmethod
    async def write_yearly_config_files(model_dir: Path, master: Master):
        for index, yc in master.yearly_config.items():
            if len(yc.enable_pce_targets) != 0:
                await OpenDssWriter.write_elements_to_file(
                    model_dir / f'Year{index}Setup.dss',
                    lambda: yc.enable_pce_targets,
                    OpenDssWriter.enable_command_to_str
                )

            if len(yc.disable_pce_targets) != 0:
                await OpenDssWriter.write_elements_to_file(
                    model_dir / f'Year{index}Cleanup.dss',
                    lambda: yc.disable_pce_targets,
                    OpenDssWriter.disable_command_to_str
                )

    @staticmethod
    async def write_master_file(model_dir: Path, master: Master):
        async with aiof.open((model_dir / 'Master.dss'), 'w') as file:
            master_str = OpenDssWriter.master_to_str(master)
            if not master_str:
                raise ValueError("Empty master object for OpenDss model.")

            await file.write(master_str)

    T = TypeVar('T')

    # noinspection PyArgumentList
    @staticmethod
    async def write_elements_to_file(
            file_path: Path,
            elements_provider: Callable[[], List[T]],
            to_str: Callable[[T], str]
    ):
        async with aiof.open(str(file_path), 'w') as file:
            await file.write("\n".join(to_str(element) for element in elements_provider()))

    @staticmethod
    def nodes_to_str(nodes: Set[Node]) -> str:
        nodes_str = '.'.join(sorted(str(n.value) for n in nodes))
        return f".{nodes_str}" if nodes_str else ""

    @staticmethod
    def bus_conn_to_str(bus_conn: BusConnection) -> str:
        return f"{bus_conn.bus.uid}{OpenDssWriter.nodes_to_str(bus_conn.connections)}"

    @staticmethod
    def line_to_str(line: Line) -> str:
        return f"New Line.{line.uid} " \
               f"Units={line.units} " \
               f"Length={line.length} " \
               f"bus1={OpenDssWriter.bus_conn_to_str(line.bus_conn1)} bus2={OpenDssWriter.bus_conn_to_str(line.bus_conn2)} " \
               f"Linecode={line.line_code.uid}"

    @staticmethod
    def line_code_to_str(line_code: LineCode) -> str:
        return f"New Linecode.{line_code.uid} " \
               f"units={line_code.units} " \
               f"nphases={line_code.nphases} " \
               f"Normamps={line_code.norm_amps} Emergamps={line_code.emerg_amps} " \
               f"R1={line_code.r1} R0={line_code.r0 or line_code.r1} " \
               f"X1={line_code.x1} X0={line_code.x0 or line_code.x1} " \
               f"B1={line_code.b1} B0={line_code.b0 or line_code.b1}"

    @staticmethod
    def conn_point_load_to_str(conn_point_to_load: Tuple[ConnectionPoint, Load]):
        cnn_point, load = conn_point_to_load
        return f"New Load.{load.uid} {OpenDssWriter.conn_point_pce_to_str(conn_point_to_load)}"

    @staticmethod
    def conn_point_generator_to_str(conn_point_to_generator: Tuple[ConnectionPoint, Generator]):
        cnn_point, generator = conn_point_to_generator
        return f"New Generator.{generator.uid} {OpenDssWriter.conn_point_pce_to_str(conn_point_to_generator)}"

    @staticmethod
    def conn_point_pce_to_str(conn_point_to_pce: Tuple[ConnectionPoint, PowerConversionElement]) -> str:
        cnn_point, pce = conn_point_to_pce
        pce_str = f"bus1={OpenDssWriter.bus_conn_to_str(cnn_point.bus_conn)} " \
                  f"kV={cnn_point.kv} Vminpu={cnn_point.v_min_pu} Vmaxpu={cnn_point.v_max_pu} " \
                  f"model={pce.model} " \
                  f"Phases={cnn_point.phases} " \
                  f"kW={pce.kw} PF={pce.pf} " \
                  f"enabled={pce.enabled}"

        if pce.load_shape is not None and pce.kw != 0:
            pce_str += f" {pce.load_shape.duration}={pce.load_shape.uid}"

        if pce.growth_shape is not None:
            pce_str += f" Growth={pce.growth_shape.uid}"
        return pce_str

    @staticmethod
    def reg_control_to_str(reg_control: RegControl) -> str:
        return f"New regcontrol.{reg_control.uid} " \
               f"transformer={reg_control.transformer.uid} winding={reg_control.winding} " \
               f"vreg={reg_control.vreg} band={reg_control.band} ptratio={reg_control.ptratio} ctprim={reg_control.ctprim} " \
               f"R={reg_control.r} X={reg_control.x}"

    @staticmethod
    def energy_meter_to_str(energy_meter: EnergyMeter) -> str:
        return f"New energymeter.{energy_meter.uid} " \
               f"element={energy_meter.element.element_type}.{energy_meter.element.uid} " \
               f"term={energy_meter.term} " \
               f"option={energy_meter.option} " \
               f"action={energy_meter.action} " \
               f"PhaseVolt={energy_meter.phasevolt}"

    @staticmethod
    def monitor_to_str(monitor: Monitor) -> str:
        return f"New monitor.{monitor.uid} " \
               f"element={monitor.element.element_type}.{monitor.element.uid} " \
               f"mode={monitor.mode}"

    @staticmethod
    def transformer_to_str(transformer: Transformer) -> str:
        tx_str = f"New Transformer.{transformer.uid} " \
                 f"phases={transformer.phases} " \
                 f"windings={len(transformer.windings)} " \
                 f"%loadloss={transformer.load_loss_percent} " \
                 f"XHL={transformer.xhl} "

        if transformer.xht is not None:
            tx_str += f"XHT={transformer.xht} "

        if transformer.xlt is not None:
            tx_str += f"XLT={transformer.xlt} "

        tx_str += " ".join(OpenDssWriter.t_winding_to_str(tw, index + 1)
                           for index, tw in enumerate(sorted(transformer.windings, key=lambda w: w.kv, reverse=True)))
        return tx_str

    @staticmethod
    def t_winding_to_str(t_winding: TransformerWinding, w_number: int) -> str:
        t_winding_str = f"wdg={w_number} conn={t_winding.conn} " \
                        f"Kv={t_winding.kv} kva={t_winding.kva} " \
                        f"bus={OpenDssWriter.bus_conn_to_str(t_winding.bus_conn)}"

        if t_winding.tap is not None:
            t_winding_str += f" Tap={t_winding.tap}"
        return t_winding_str

    @staticmethod
    def load_shape_to_str(load_shape: LoadShape) -> str:
        return f"New Loadshape.{load_shape.uid} " \
               f"npts={len(load_shape.shape)} " \
               f"{'' if load_shape.interval is None else f'interval={load_shape.interval} '}" \
               f"mult=(file={load_shape.uid}.txt) " \
               f"action=normalize"

    @staticmethod
    def growth_shape_to_str(growth_shape: GrowthShape) -> str:
        years = []
        multi = []
        for index, value in enumerate(growth_shape.shape):
            years.append(str(index))
            multi.append(str(value))

        return f"New GrowthShape.{growth_shape.uid} " \
               f"npts={len(years)} " \
               f"Year=[{', '.join(years)}] " \
               f"Mult=[{', '.join(multi)}]"

    @staticmethod
    def enable_command_to_str(pce_target: PceEnableTarget) -> str:
        return f"Edit {pce_target.pce_type}.{pce_target.uid} enabled=True"

    @staticmethod
    def disable_command_to_str(pce_target: PceEnableTarget) -> str:
        return f"Edit {pce_target.pce_type}.{pce_target.uid} enabled=False"

    @staticmethod
    def master_to_str(master: Master) -> str:
        model_files_str = ""
        if OpenDssWriter.has_line_codes(master):
            model_files_str += "Redirect LineCodes.dss\n"
        if OpenDssWriter.has_lines(master):
            model_files_str += "Redirect Lines.dss\n"
        if OpenDssWriter.has_transformers(master):
            model_files_str += "Redirect Transformers.dss\n"
        if OpenDssWriter.has_reg_controls(master):
            model_files_str += "Redirect RegControls.dss\n"
        if OpenDssWriter.has_load_shapes(master):
            model_files_str += "Redirect LoadShapes.dss\n"
        if OpenDssWriter.has_growth_shapes(master):
            model_files_str += "Redirect GrowthShapes.dss\n"
        if OpenDssWriter.has_loads(master):
            model_files_str += "Redirect Loads.dss\n"
        if OpenDssWriter.has_generators(master):
            model_files_str += "Redirect Generators.dss\n"
        if OpenDssWriter.has_energy_meters(master):
            model_files_str += "Redirect EnergyMeters.dss\n"
        if OpenDssWriter.has_monitors(master):
            model_files_str += "Redirect Monitors.dss\n"

        if not model_files_str:
            return ""

        return (
                "Clear\n" +
                "\n" +
                f"set defaultbasefreq={master.network_model.default_base_frequency}\n" +
                "\n" +
                f"New Circuit.{master.network_model.circuit.uid}  "
                f"bus1={master.network_model.circuit.bus_conn.bus.uid} "
                f"pu={master.network_model.circuit.pu} "
                f"basekV={master.network_model.circuit.base_kv} "
                f"phases={master.network_model.circuit.phases}\n" +
                "\n" +
                "Set normvminpu=0.94\n"
                "Set normvmaxpu=1.10\n" +
                "\n" +
                model_files_str +
                "\n" +
                f"Set Voltagebases=[{','.join(str(vb) for vb in master.network_model.voltage_bases)}]\n"
                "\n" +
                "Calcvoltagebases\n" +
                "\n" +
                "Set overloadreport=true\t! TURN OVERLOAD REPORT ON\n" +
                "Set voltexcept=true\t! voltage exception report\n" +
                "Set demand=true\t! demand interval ON\n" +
                "Set DIVerbose=true\t! verbose mode is ON\n" +
                "Set Maxiter=25\n" +
                "Set Maxcontroliter=20\n" +
                "set mode=yearly\n" +
                "\n" +
                OpenDssWriter.master_solve_str(master)
        )

    @staticmethod
    def master_solve_str(master: Master) -> str:
        if len(master.yearly_config) == 0:
            return "Solve"

        solve_str = ""
        for year, config in sorted(master.yearly_config.items(), key=lambda x: x[0]):
            if len(config.enable_pce_targets) != 0:
                solve_str += f"Redirect Year{year}Setup.dss\n"

            solve_str += f"set year={year}\n" \
                         f"Solve\n" \
                         f"CloseDI\n"

            if len(config.disable_pce_targets) != 0:
                solve_str += f"Redirect Year{year}Cleanup.dss\n"

            solve_str += "\n"

        return solve_str
