"""
Qt API for PyQt5/6 and PySide2/6.

Import the Qt subpackages from this module, as if importing from the Qt binding
package.

Notes
=====

This module is not part of public API, therefore users must not rely on it.

Based on https://github.com/hmeine/qimage2ndarray and
https://github.com/pytest-dev/pytest-qt.

"""


class QtAPIError(Exception):
    pass


class _QtAPI:
    """
    Interface to access the Qt binding package installed in the environment.

    This object can be treated as root namespace of the Qt package.

    """

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
            self.qt_binding = "PySide6"
        elif _can_import("PySide2.QtCore"):
            self.qt_binding = "PySide2"
        elif _can_import("PyQt6.QtCore"):
            self.qt_binding = "PyQt6"
        elif _can_import("PyQt5.QtCore"):
            self.qt_binding = "PyQt5"
        else:
            errors = "\n".join(
                f"  {module}: {reason}"
                for module, reason in sorted(self._import_errors.items())
            )
            msg = "Supported Qt not installed.\n" + errors
            raise QtAPIError(msg)

        if self.qt_binding in ("PyQt5", "PyQt6"):
            self.QtCore.Signal = self.QtCore.pyqtSignal
            self.QtCore.Slot = self.QtCore.pyqtSlot

    def _import_module(self, module_name):
        m = __import__(self.qt_binding, globals(), locals(), [module_name], 0)
        return getattr(m, module_name)

    def __getattr__(self, name):
        if name.startswith("Qt"):
            return self._import_module(name)
        return super().__getattr__(name)


qt_api = _QtAPI()

QtCore = qt_api.QtCore
QtWidgets = qt_api.QtWidgets
