"""
Dynamically import Qt module.

"""
# Code from https://github.com/hmeine/qimage2ndarray

import os
import sys


class QtDriver(object):
    DRIVERS = (
        "PySide2",
        "PySide6",
        "PyQt5",
        "PyQt6",
    )
    DEFAULT = "PyQt5"

    @classmethod
    def detect_qt(cls):
        for drv in cls.DRIVERS:
            if drv in sys.modules:
                return drv
        return None

    def name(self):
        return self._drv

    def __init__(self, drv=os.environ.get("QT_DRIVER")):
        """Supports QT_API (used by ETS and ipython)"""
        if drv is None:
            drv = self.detect_qt()
        if drv is None:
            drv = os.environ.get("QT_API")
        if drv is None:
            drv = self.DEFAULT
        # map ETS syntax
        drv = {
            "pyside2": "PySide2",
            "pyside6": "PySide6",
            "pyqt5": "PyQt5",
            "pyqt6": "PyQt6",
        }.get(drv, drv)
        assert drv in self.DRIVERS
        self._drv = drv

        if self._drv.startswith("PyQt"):
            self.QtCore.Signal = self.QtCore.pyqtSignal
            self.QtCore.Slot = self.QtCore.pyqtSlot

    def importMod(self, mod):
        qt = __import__("%s.%s" % (self._drv, mod))
        return getattr(qt, mod)

    def __getattr__(self, name):
        if name.startswith("Qt"):
            return self.importMod(name)
        return super(QtDriver, self).__getattr__(name)


qt = QtDriver()

QtCore = qt.QtCore
QtWidgets = qt.QtWidgets
