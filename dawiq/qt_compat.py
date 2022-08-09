"""
Qt API for PyQt5/6 and PySide2/6.

Based on from https://github.com/hmeine/qimage2ndarray and
https://github.com/pytest-dev/pytest-qt.
"""

from collections import namedtuple


class QtAPIError(Exception):
    pass


VersionTuple = namedtuple("VersionTuple", "qt_api, qt_api_version, runtime, compiled")


class _QtAPI:

    supported_apis = [
        "PySide6",
        "PySide2",
        "PyQt6",
        "PyQt5",
    ]

    def __init__(self):
        self._import_errors = {}

        def _can_import(name):
            try:
                __import__(name)
                return True
            except ModuleNotFoundError as e:
                self._import_errors[name] = str(e)
                return False

        # Not importing only the root namespace because when uninstalling from conda,
        # the namespace can still be there.
        if _can_import("PySide6.QtCore"):
            self.qt_module = "PySide6"
        elif _can_import("PySide2.QtCore"):
            self.qt_module = "PySide2"
        elif _can_import("PyQt6.QtCore"):
            self.qt_module = "PyQt6"
        elif _can_import("PyQt5.QtCore"):
            self.qt_module = "PyQt5"
        else:
            errors = "\n".join(
                f"  {module}: {reason}"
                for module, reason in sorted(self._import_errors.items())
            )
            msg = "Supported Qt not installed.\n" + errors
            raise QtAPIError(msg)

        def _import_module(module_name):
            m = __import__(self.qt_module, globals(), locals(), [module_name], 0)
            return getattr(m, module_name)

        self.QtCore = QtCore = _import_module("QtCore")
        self.QtWidgets = _import_module("QtWidgets")

        if self.qt_module in ("PyQt5", "PyQt6"):
            self.QtCore.Signal = QtCore.pyqtSignal
            self.QtCore.Slot = QtCore.pyqtSlot


qt_api = _QtAPI()

QtCore = qt_api.QtCore
QtWidgets = qt_api.QtWidgets
