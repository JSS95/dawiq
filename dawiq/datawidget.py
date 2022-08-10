"""
Data widget
===========

:mod:`dawiq.datawidget` provides :class:`DataWidget` to represent the data
structure established by the dataclass.
"""

from .qt_compat import QtCore, QtWidgets
from typing import Optional
from .typing import FieldWidgetProtocol


__all__ = [
    "DataWidget",
]


class DataWidget(QtWidgets.QGroupBox):
    """
    Widget to represent the data structure.
    """

    def __init__(
        self,
        orientation: QtCore.Qt.Orientation = QtCore.Qt.Orientation.Vertical,
        parent=None,
    ):
        super().__init__(parent)
        self._orientation = orientation

        if orientation == QtCore.Qt.Orientation.Vertical:
            layout = QtWidgets.QVBoxLayout()
        elif orientation == QtCore.Qt.Orientation.Horizontal:
            layout = QtWidgets.QHBoxLayout()
        else:
            raise TypeError(f"Invalid orientation: {orientation}")
        self.setLayout(layout)

    def dataName(self) -> str:
        return self.title()

    def setDataName(self, name: str):
        self.setTitle(name)

    def orientation(self) -> QtCore.Qt.Orientation:
        return self._orientation

    def count(self) -> int:
        return self.layout().count()

    def widget(self, index: int) -> Optional[FieldWidgetProtocol]:
        item = self.layout().itemAt(index)
        if item is not None:
            item = item.widget()
        return item

    def insertWidget(
        self,
        index: int,
        widget: FieldWidgetProtocol,
        stretch: int = 0,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag(0),
    ):
        for i in range(self.count()):
            w = self.widget(i)
            if w is None:
                break
            elif widget.dataName() == w.dataName():
                raise KeyError(f"Data name '{widget.dataName()}' is duplicate")
        self.layout().insertWidget(index, widget, stretch, alignment)

    def addWidget(
        self,
        widget: FieldWidgetProtocol,
        stretch: int = 0,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag(0),
    ):
        for i in range(self.count()):
            w = self.widget(i)
            if w is None:
                break
            elif widget.dataName() == w.dataName():
                raise KeyError(f"Data name '{widget.dataName()}' is duplicate")
        self.layout().addWidget(widget, stretch, alignment)

    def removeWidget(self, widget: FieldWidgetProtocol):
        self.layout().removeWidget(widget)
