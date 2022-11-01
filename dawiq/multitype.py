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
    Stacked widget containing multiple :class:`DataWidget` and their dataclasses.

    To add :class:`DataWidget`, pass the widget and its dataclass to
    :meth:`addDataWidget` or to :meth:`insertDataWidget`.

    When the data value of current data widget changes, this widget emits
    :attr:`currentDataValueChanged` signal. When the current data widget is
    edited by user, :attr:`currentDataEdited` signal is emitted.

    """

    currentDataValueChanged = QtCore.Signal(dict)
    currentDataEdited = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dataWidgets = {}
        self._previousIndex = -1
        self.currentChanged.connect(self._onCurrentChange)

    def _onCurrentChange(self, index: int):
        """Handle the signals of old widget and current widget."""
        old = self.widget(self._previousIndex)
        if isinstance(old, DataWidget):
            old.dataValueChanged.disconnect(self.currentDataValueChanged)
            old.dataEdited.disconnect(self.currentDataEdited)
        new = self.widget(index)
        if isinstance(new, DataWidget):
            new.dataValueChanged.connect(self.currentDataValueChanged)
            new.dataEdited.connect(self.currentDataEdited)
        self._previousIndex = index

    def addDataWidget(
        self, widget: DataWidget, dataclass: Type[DataclassProtocol]
    ) -> int:
        """Add *widget* with binding it to *dataclass*."""
        index = self.addWidget(widget)
        self._dataWidgets[widget] = dataclass
        return index

    def insertDataWidget(
        self, index: int, widget: DataWidget, dataclass: Type[DataclassProtocol]
    ) -> int:
        index = self.insertWidget(index, widget)
        self._dataWidgets[widget] = dataclass
        return index

    def removeWidget(self, widget: QtWidgets.QWidget):
        if isinstance(widget, DataWidget):
            self._dataWidgets.pop(widget, None)
            if widget == self.currentWidget():
                widget.dataValueChanged.disconnect(self.currentDataValueChanged)
                widget.dataEdited.disconnect(self.currentDataEdited)
        super().removeWidget(widget)

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


class DataclassTabWidget(QtWidgets.QTabWidget):
    """
    Tab widget containing multiple :class:`DataWidget` and dataclasses.

    To add :class:`DataWidget`, pass the widget and its dataclass to
    :meth:`addDataWidget` or to :meth:`insertDataWidget`.

    When current index is changed by user, :attr:`activated` signal is emitted.
    When the data value of current data widget changes, this widget emits
    :attr:`currentDataValueChanged` signal. When the current data widget is
    edited by user, :attr:`currentDataEdited` signal is emitted.

    """

    activated = QtCore.Signal(int)
    currentDataValueChanged = QtCore.Signal(dict)
    currentDataEdited = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dataWidgets = {}
        self._previousIndex = -1
        self._blockActivated = False
        self.currentChanged.connect(self._onCurrentChange)

    def setCurrentIndex(self, index):
        self._blockActivated = True
        super().setCurrentIndex(index)
        self._blockActivated = False

    def _onCurrentChange(self, index: int):
        """Handle the signals of old widget and current widget."""
        old = self.widget(self._previousIndex)
        if isinstance(old, DataWidget):
            old.dataValueChanged.disconnect(self.currentDataValueChanged)
            old.dataEdited.disconnect(self.currentDataEdited)
        new = self.widget(index)
        if isinstance(new, DataWidget):
            new.dataValueChanged.connect(self.currentDataValueChanged)
            new.dataEdited.connect(self.currentDataEdited)
        self._previousIndex = index
        if not self._blockActivated:
            self.activated.emit(index)

    def addDataWidget(self, widget, dataclass, icon=None, label=None) -> int:
        """Add *widget* with binding it to *dataclass*."""
        args = [arg for arg in [icon, label] if arg is not None]
        index = self.addTab(widget, *args)
        self._dataWidgets[widget] = dataclass
        return index

    def insertDataWidget(self, index, widget, dataclass, icon=None, label=None) -> int:
        """Insert *widget* with binding it to *dataclass*."""
        args = [arg for arg in [icon, label] if arg is not None]
        index = self.insertTab(index, widget, *args)
        self._dataWidgets[widget] = dataclass
        return index

    def removeTab(self, index: int):
        widget = self.widget(index)
        if isinstance(widget, DataWidget):
            self._dataWidgets.pop(widget, None)
            if widget == self.currentWidget():
                widget.dataValueChanged.disconnect(self.currentDataValueChanged)
                widget.dataEdited.disconnect(self.currentDataEdited)
        super().removeTab(index)

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
