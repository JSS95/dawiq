"""
Data widget container
=====================

:mod:`dawiq.multitype` provides widgets that contain multiple :class:`DataWidget`
to support multiple dataclass types.
"""

from .qt_compat import QtWidgets, QtCore
from .datawidget import DataWidget
from typing import Type, Optional
from .typing import DataclassProtocol


__all__ = [
    "DataclassStackedWidget",
    "DataclassTabWidget",
]


class DataclassStackedWidget(QtWidgets.QStackedWidget):
    """
    Stacked widget containing multiple :class:`DataWidget` and dataclasses.

    To add :class:`DataWidget`, pass the widget and the dataclass from which
    the widget was constructed to :meth:`addDataWidget`.

    When the data value of current :class:`DataWidget` changes, this widget
    emits :attr:`currentDataValueChanged` signal.

    """

    currentDataValueChanged = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dataWidgets = {}
        self._previousIndex = -1
        self.currentChanged.connect(self.onCurrentChange)

    @QtCore.Slot(int)
    def onCurrentChange(self, index: int):
        """Handle the signals of old widget and current widget."""
        old = self.widget(self._previousIndex)
        if isinstance(old, DataWidget):
            old.dataValueChanged.disconnect(self.currentDataValueChanged)
        new = self.widget(index)
        if isinstance(new, DataWidget):
            new.dataValueChanged.connect(self.currentDataValueChanged)
        self._previousIndex = index

    def addDataWidget(
        self, widget: DataWidget, dataclass: Type[DataclassProtocol]
    ) -> int:
        """Add *widget* with binding it to *dataclass*."""
        self._dataWidgets[widget] = dataclass
        index = self.addWidget(widget)
        return index

    def currentDataclass(self) -> Optional[Type[DataclassProtocol]]:
        return self._dataWidgets.get(self.currentWidget())

    def indexOfDataclass(self, dataclass: Type[DataclassProtocol]) -> int:
        """Return the index of the widget bound to *dataclass*."""
        for widget, dcls in self._dataWidgets.items():
            if dcls == dataclass:
                index = self.indexOf(widget)
                break
        else:
            index = -1
        return index

    def removeWidget(self, widget: QtWidgets.QWidget):
        if isinstance(widget, DataWidget):
            self._dataWidgets.pop(widget, None)
            if widget == self.currentWidget():
                widget.dataValueChanged.disconnect(self.currentDataValueChanged)
        super().removeWidget(widget)


class DataclassTabWidget(QtWidgets.QTabWidget):
    """
    Tab widget containing multiple :class:`DataWidget` and dataclasses.

    To add :class:`DataWidget`, pass the widget and the dataclass from which
    the widget was constructed to :meth:`addDataWidget`.

    When the data value of current :class:`DataWidget` changes, this widget
    emits :attr:`currentDataValueChanged` signal.

    """

    currentDataValueChanged = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dataWidgets = {}
        self._previousIndex = -1
        self.currentChanged.connect(self.onCurrentChange)

    @QtCore.Slot(int)
    def onCurrentChange(self, index: int):
        """Handle the signals of old widget and current widget."""
        old = self.widget(self._previousIndex)
        if isinstance(old, DataWidget):
            old.dataValueChanged.disconnect(self.currentDataValueChanged)
        new = self.widget(index)
        if isinstance(new, DataWidget):
            new.dataValueChanged.connect(self.currentDataValueChanged)
        self._previousIndex = index

    def addDataWidget(
        self, widget: DataWidget, label: str, dataclass: Type[DataclassProtocol]
    ) -> int:
        """Add *widget* with binding it to *dataclass*."""
        self._dataWidgets[widget] = dataclass
        index = self.addTab(widget, label)
        return index

    def currentDataclass(self) -> Optional[Type[DataclassProtocol]]:
        return self._dataWidgets.get(self.currentWidget())

    def indexOfDataclass(self, dataclass: Type[DataclassProtocol]) -> int:
        """Return the index of the widget bound to *dataclass*."""
        for widget, dcls in self._dataWidgets.items():
            if dcls == dataclass:
                index = self.indexOf(widget)
                break
        else:
            index = -1
        return index

    def removeTab(self, index: int):
        widget = self.widget(index)
        if isinstance(widget, DataWidget):
            self._dataWidgets.pop(widget, None)
            if widget == self.currentWidget():
                widget.dataValueChanged.disconnect(self.currentDataValueChanged)
        super().removeTab(index)
