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
]


class DataWidgetStack(QtWidgets.QStackedWidget):
    """
    Stacked widget containing multiple :class:`DataWidget`.

    When the data value of current :class:`DataWidget` changes, this widget
    emits :attr:`currentDataValueChanged` signal.

    """

    currentDataValueChanged = QtCore.Signal(dict)

    def addWidget(self, widget: QtWidgets.QWidget):
        # force size policy to ignore the size of hidden widget
        widget.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored
        )
        super().addWidget(widget)
        if self.currentWidget() == widget:
            widget.dataValueChanged.connect(self.currentDataValueChanged)

    def setCurrentIndex(self, index: int):
        old = self.currentWidget()
        if old is not None:
            old.setSizePolicy(
                QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored
            )
        if isinstance(old, DataWidget):
            old.dataValueChanged.disconnect(self.currentDataValueChanged)
        new = self.widget(index)
        if new is not None:
            new.setSizePolicy(
                QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
            )
            new.adjustSize()
        if isinstance(new, DataWidget):
            new.dataValueChanged.connect(self.currentDataValueChanged)
        super().setCurrentIndex(index)
        self.adjustSize()

    def setCurrentWidget(self, widget: QtWidgets.QWidget):
        old = self.currentWidget()
        if old is not None:
            old.setSizePolicy(
                QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored
            )
        if isinstance(old, DataWidget):
            old.dataValueChanged.disconnect(self.currentDataValueChanged)
        new = widget
        if new is not None:
            new.setSizePolicy(
                QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
            )
            new.adjustSize()
        if isinstance(new, DataWidget):
            new.dataValueChanged.connect(self.currentDataValueChanged)
        super().setCurrentWidget(widget)
        self.adjustSize()
