from .dynqt import QtCore, QtWidgets
from typing import Any, Optional
from .typing import FieldWidgetProtocol


__all__ = [
    "type2Widget",
    "BoolCheckBox",
]


def type2Widget(t: Any) -> FieldWidgetProtocol:
    """Return the widget instance for given type annotation."""
    if isinstance(t, type) and issubclass(t, bool):
        return BoolCheckBox()
    raise TypeError("Unknown type or annotation: %s" % t)


class BoolCheckBox(QtWidgets.QCheckBox):
    """
    Checkbox for fuzzy boolean value.

    If the box is checked, the value is True. If it is unchecked, the value is
    False. Else, e.g. tristate is allowed, the value is None.

    :meth:`dataValue` returns the current value. When the check state is changed,
    :attr:`dataValueChanged` signal is emitted. :meth:`setDataValue` changes the
    check state of the checkbox.

    Examples
    ========

    >>> from PySide6.QtWidgets import QApplication
    >>> import sys
    >>> from dawiq import BoolCheckBox
    >>> def runGUI():
    ...     app = QApplication(sys.argv)
    ...     widget = BoolCheckBox()
    ...     widget.setTristate(True)
    ...     widget.show()
    ...     app.exec()
    ...     app.quit()
    >>> runGUI() # doctest: +SKIP

    """

    dataValueChanged = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.stateChanged.connect(self.emitDataValueChanged)

    def dataName(self) -> str:
        return self.text()

    def setDataName(self, name: str):
        self.setText(name)
        self.setToolTip(name)

    def dataValue(self) -> Optional[bool]:
        checkstate = self.checkState()
        if checkstate == QtCore.Qt.Checked:
            state = True
        elif checkstate == QtCore.Qt.Unchecked:
            state = False
        else:
            state = None
        return state

    def setDataValue(self, value: Optional[bool]):
        if value is True:
            state = QtCore.Qt.Checked
        elif value is False:
            state = QtCore.Qt.Unchecked
        else:
            state = QtCore.Qt.PartiallyChecked
        self.setCheckState(state)

    def emitDataValueChanged(self, checkstate: QtCore.Qt.CheckState):
        if checkstate == QtCore.Qt.Checked:
            state = True
        elif checkstate == QtCore.Qt.Unchecked:
            state = False
        else:
            state = None
        self.dataValueChanged.emit(state)
