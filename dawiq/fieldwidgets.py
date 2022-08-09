"""
Data field widgets
==================

:mod:`dawiq.fieldwidgets` provides widgets to represent the fields of the
dataclass.
"""

from .qt_compat import QtCore, QtWidgets
from typing import Any, Optional, Union
from .typing import FieldWidgetProtocol


__all__ = [
    "type2Widget",
    "BoolCheckBox",
]


def type2Widget(t: Any) -> FieldWidgetProtocol:
    """Construct the widget for given type annotation."""
    if isinstance(t, type) and issubclass(t, bool):
        return BoolCheckBox()
    raise TypeError("Unknown type or annotation: %s" % t)


class BoolCheckBox(QtWidgets.QCheckBox):
    """
    Checkbox for fuzzy boolean value.

    :meth:`dataValue` returns the current value. When the check state is changed,
    :attr:`dataValueChanged` signal is emitted. :meth:`setDataValue` changes the
    check state of the checkbox.

    If the box is checked, the data value is True. If unchecked, the value is
    False. Else, e.g. ``Qt.PartiallyChecked``, the value is None.

    Because of the nature of check box, default value always exists even if
    the original dataclass does not define it.

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
        if checkstate == QtCore.Qt.CheckState.Checked:
            state = True
        elif checkstate == QtCore.Qt.CheckState.Unchecked:
            state = False
        else:
            state = None
        return state

    def setDataValue(self, value: Optional[bool]):
        if value is True:
            state = QtCore.Qt.CheckState.Checked
        elif value is False:
            state = QtCore.Qt.CheckState.Unchecked
        else:
            state = QtCore.Qt.CheckState.PartiallyChecked
        self.setCheckState(state)

    def emitDataValueChanged(self, checkstate: Union[int, QtCore.Qt.CheckState]):
        checkstate = QtCore.Qt.CheckState(checkstate)
        if checkstate == QtCore.Qt.CheckState.Checked:
            state = True
        elif checkstate == QtCore.Qt.CheckState.Unchecked:
            state = False
        else:
            state = None
        self.dataValueChanged.emit(state)
