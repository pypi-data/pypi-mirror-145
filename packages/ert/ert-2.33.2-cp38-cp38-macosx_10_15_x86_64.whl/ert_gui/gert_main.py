#  Copyright (C) 2011  Equinor ASA, Norway.
#
#  The file 'gert_main.py' is part of ERT - Ensemble based Reservoir Tool.
#
#  ERT is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ERT is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.
#
#  See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html>
#  for more details.
import os
import logging
import sys
import time

from qtpy.QtCore import Qt, QLocale
from qtpy.QtWidgets import QApplication, QMessageBox

from ert_gui.ert_splash import ErtSplash
from ert_gui.ertwidgets import SummaryPanel, resourceIcon
import ert_gui.ertwidgets
from ert_gui.ertnotifier import ErtNotifier
from ert_gui.main_window import GertMainWindow
from ert_gui.simulation.simulation_panel import SimulationPanel
from ert_gui.tools.export import ExportTool
from ert_gui.tools.ide import IdeTool
from ert_gui.tools.load_results import LoadResultsTool
from ert_gui.tools.manage_cases import ManageCasesTool
from ert_gui.tools.plot import PlotTool
from ert_gui.tools.plugins import PluginHandler, PluginsTool
from ert_gui.tools.run_analysis import RunAnalysisTool
from ert_gui.tools.workflows import WorkflowsTool
from ert_shared import ERT

from res.enkf import EnKFMain, ResConfig

import ecl


def run_gui(args):
    app = QApplication([])  # Early so that QT is initialized before other imports
    app.setWindowIcon(resourceIcon("application/window_icon_cutout"))
    res_config = ResConfig(args.config)

    # Create logger inside function to make sure all handlers have been added to the root-logger.
    logger = logging.getLogger(__name__)
    logger.info(
        "Logging forward model jobs",
        extra={
            "workflow_jobs": str(res_config.model_config.getForwardModel().joblist())
        },
    )

    os.chdir(res_config.config_path)
    # Changing current working directory means we need to update the config file to
    # be the base name of the original config
    args.config = os.path.basename(args.config)
    ert = EnKFMain(res_config, strict=True, verbose=args.verbose)
    notifier = ErtNotifier(ert, args.config)
    with ERT.adapt(notifier):
        # window reference must be kept until app.exec returns
        window = _start_window(ert, args)
        return app.exec_()


def _start_window(ert, args):

    _check_locale()

    splash = ErtSplash(version_string="Version {}".format(ert_gui.__version__))
    splash.show()
    splash.repaint()
    splash_screen_start_time = time.time()

    window = _setup_main_window(ert, args)

    minimum_splash_screen_time = 2
    sleep_time_left = minimum_splash_screen_time - (
        time.time() - splash_screen_start_time
    )
    if sleep_time_left > 0:
        time.sleep(sleep_time_left)

    window.show()
    splash.finish(window)
    window.activateWindow()
    window.raise_()

    if not ert._real_enkf_main().have_observations():
        QMessageBox.warning(
            window,
            "Warning!",
            "No observations loaded. Model update algorithms disabled!",
        )

    return window


def _check_locale():
    # There seems to be a setlocale() call deep down in the initialization of
    # QApplication, if the user has set the LC_NUMERIC environment variables to
    # a locale with decimalpoint different from "." the application will fail
    # hard quite quickly.
    current_locale = QLocale()
    decimal_point = str(current_locale.decimalPoint())
    if decimal_point != ".":
        msg = """
** WARNING: You are using a locale with decimalpoint: '{}' - the ert application is
            written with the assumption that '.' is used as decimalpoint, and chances
            are that something will break if you continue with this locale. It is highly
            reccomended that you set the decimalpoint to '.' using one of the environment
            variables 'LANG', LC_ALL', or 'LC_NUMERIC' to either the 'C' locale or
            alternatively a locale which uses '.' as decimalpoint.\n""".format(
            decimal_point
        )

        sys.stderr.write(msg)


def _setup_main_window(ert, args):
    config_file = args.config
    window = GertMainWindow(config_file)
    window.setWidget(SimulationPanel(config_file))
    plugin_handler = PluginHandler(ert, ert.getWorkflowList().getPluginJobs(), window)

    window.addDock(
        "Configuration Summary", SummaryPanel(), area=Qt.BottomDockWidgetArea
    )
    window.addTool(IdeTool(config_file))
    window.addTool(PlotTool(config_file))
    window.addTool(ExportTool())
    window.addTool(WorkflowsTool())
    window.addTool(ManageCasesTool())
    window.addTool(PluginsTool(plugin_handler))
    window.addTool(RunAnalysisTool())
    window.addTool(LoadResultsTool())
    window.adjustSize()
    return window
