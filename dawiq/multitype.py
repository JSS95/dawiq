"""
Data widget container
=====================

:mod:`dawiq.multitype` provides widgets that contain multiple :class:`DataWidget`
to support multiple dataclass types.
"""

from .qt_compat import QtWidgets, QtCore
from .datawidget import DataWidget


__all__ = [
    "DataWidgetStack",
    "DataWidgetTab",
]


class DataWidgetStack(QtWidgets.QStackedWidget):
    """
    Stacked widget containing multiple :class:`DataWidget`.

    When the data value of current :class:`DataWidget` changes, this widget
    emits :attr:`currentDataValueChanged` signal.

    """

    currentDataValueChanged = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._previousIndex = -1
        self.currentChanged.connect(self.handleDataValueSignal)

    @QtCore.Slot(int)
    def handleDataValueSignal(self, index: int):
        old = self.widget(self._previousIndex)
        if isinstance(old, DataWidget):
            old.dataValueChanged.disconnect(self.currentDataValueChanged)
        new = self.widget(index)
        if isinstance(new, DataWidget):
            new.dataValueChanged.connect(self.currentDataValueChanged)
        self._previousIndex = index


class DataWidgetTab(QtWidgets.QTabWidget):
    """
    Tab widget containing multiple :class:`DataWidget`.

    When the data value of current :class:`DataWidget` changes, this widget
    emits :attr:`currentDataValueChanged` signal.

    """

    currentDataValueChanged = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._previousIndex = -1
        self.currentChanged.connect(self.handleDataValueSignal)

    @QtCore.Slot(int)
    def handleDataValueSignal(self, index: int):
        old = self.widget(self._previousIndex)
        if isinstance(old, DataWidget):
            old.dataValueChanged.disconnect(self.currentDataValueChanged)
        new = self.widget(index)
        if isinstance(new, DataWidget):
            new.dataValueChanged.connect(self.currentDataValueChanged)
        self._previousIndex = index
