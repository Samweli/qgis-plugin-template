"""
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os.path

from qgis.core import QgsSettings
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QDockWidget, QMainWindow, QVBoxLayout

# Initialize Qt resources from file resources.py
from .resources import *

from .gui.qgis_plugin_template import QgisPluginTemplate


class QgisPlugin:
    """QGIS Plugin Template Plugin Implementation."""

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        locale = QgsSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(self.plugin_dir, "i18n", "QGISPluginTemplate{}.qm".format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr("&QGIS Plugin Template")
        self.pluginIsActive = False
        self.toolbar = self.iface.addToolBar("Open QGIS Plugin Template")
        self.toolbar.setObjectName("QGIS Plugin Template")

        self.main_widget = QgisPluginTemplate(
            iface=self.iface, parent=self.iface.mainWindow()
        )

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.
        We implement this ourselves since we do not inherit QObject.
        :param message: String for translation.
        :type message: str, QString
        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("QGIS Plugin Template", message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_web_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None,
    ):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_web_menu: Flag indicating whether the action
            should also be added to the web menu. Defaults to True.
        :type add_to_web_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        if add_to_web_menu:
            self.iface.addPluginToWebMenu(self.menu, action)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = ":/plugins/qgis_plugin_template/icon.svg"
        self.add_action(
            icon_path,
            text=self.tr("Open Plugin"),
            callback=self.run,
            parent=self.iface.mainWindow(),
        )

        # Handle debug mode and additional settings
        debug_mode = int(setting(key="debug_mode", default=0))
        if debug_mode:
            debug_icon = QIcon(":/plugins/qgis_plugin_template/debug.svg")
            self.debug_action = QAction(
                debug_icon, "Debug Mode", self.iface.mainWindow()
            )
            self.debug_action.triggered.connect(self.debug)
            self.iface.addToolBarIcon(self.debug_action)

            tests_icon = QIcon(":/plugins/qgis_plugin_template/run-tests.svg")
            self.tests_action = QAction(
                tests_icon, "Run Tests", self.iface.mainWindow()
            )
            self.tests_action.triggered.connect(self.run_tests)
            self.iface.addToolBarIcon(self.tests_action)
        else:
            self.tests_action = None
            self.debug_action = None

        debug_env = int(os.getenv("DEBUG", 0))
        if debug_env:
            self.debug()

    def kill_debug(self):
        # Note that even though this kills the debugpy process I still
        # cannot successfully restart the debugger in vscode without restarting QGIS
        if self.debug_running:
            import psutil
            import signal

            """Find the PID of the process listening on the specified port."""
            for conn in psutil.net_connections(kind="tcp"):
                if conn.laddr.port == 9000 and conn.status == psutil.CONN_LISTEN:
                    os.kill(conn.pid, signal.SIGTERM)

    def debug(self):
        """
        Enters debug mode.
        Shows a message to attach a debugger to the process.
        """
        self.kill_debug()
        self.display_information_message_box(
            title="qgis-plugin-template",
            message="Close this dialog then open VSCode and start your debug client.",
        )
        import multiprocessing  # pylint: disable=import-outside-toplevel

        if multiprocessing.current_process().pid > 1:
            import debugpy  # pylint: disable=import-outside-toplevel

            debugpy.listen(("0.0.0.0", 9000))
            debugpy.wait_for_client()
            self.display_information_message_bar(
                title="qgis-plugin-template",
                message="Visual Studio Code debugger is now attached on port 9000",
            )
            self.debug_action.setEnabled(False)  # prevent user starting it twice
            self.debug_running = True

    def run_tests(self):
        """Run unit tests in the python console."""

        main_window = self.iface.mainWindow()
        action = main_window.findChild(QAction, "mActionShowPythonDialog")
        action.trigger()
        for child in main_window.findChildren(QDockWidget, "PythonConsole"):
            if child.objectName() == "PythonConsole":
                child.show()
                for widget in child.children():

                    widget_class_name = widget.__class__.__name__
                    if widget_class_name == "PythonConsole":
                        shell = widget.console.shell
                        test_dir = "/home/user/dev/python/qgis-plugin-template/test"
                        shell.runCommand("")
                        shell.runCommand("import unittest")
                        shell.runCommand("test_loader = unittest.TestLoader()")
                        shell.runCommand(
                            f'test_suite = test_loader.discover(start_dir="{test_dir}", pattern="test_*.py")'
                        )
                        shell.runCommand(
                            "test_runner = unittest.TextTestRunner(verbosity=2)"
                        )
                        shell.runCommand("test_runner.run(test_suite)")
                        # Unload test modules
                        shell.runCommand(
                            f"""
    for module_name in list(sys.modules.keys()):
        if module_name.startswith("test_") or module_name.startswith("utilities_for_testing"):
            del sys.modules[module_name]

                                """
                        )
                        break

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin widget is closed"""
        self.pluginIsActive = False

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        try:
            for action in self.actions:
                self.iface.removePluginMenu(self.tr("&QGIS Plugin Template"), action)
                self.iface.removePluginWebMenu(self.tr("&QGIS Plugin Template"), action)
                self.iface.removeToolBarIcon(action)

        except Exception as e:
            pass

    def run(self):
        if self.main_widget == None:
            self.main_widget = QgisPluginTemplate(
                iface=self.iface, parent=self.iface.mainWindow()
            )

        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.main_widget)
        self.main_widget.show()

        if not self.pluginIsActive:
            self.pluginIsActive = True
