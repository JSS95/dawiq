"""
Data field widgets
==================

:mod:`dawiq.fieldwidgets` provides widgets to represent the fields of the
dataclass.
"""

from .qt_compat import QtCore, QtWidgets, QtGui
from typing import Any, Optional, Union, Tuple
from .typing import FieldWidgetProtocol


__all__ = [
    "type2Widget",
    "BoolCheckBox",
    "MISSING",
    "EmptyIntValidator",
    "IntLineEdit",
]


def type2Widget(t: Any) -> FieldWidgetProtocol:
    """Construct the widget for given type annotation."""
    if isinstance(t, type) and issubclass(t, bool):
        return BoolCheckBox()
    if isinstance(t, type) and issubclass(t, int):
        return IntLineEdit()

    origin = getattr(t, "__origin__", None)

    if origin is Union:
        args = [a for a in getattr(t, "__args__") if not isinstance(None, a)]
        if len(args) > 1:
            msg = f"Cannot convert Union with multiple types: {t}"
            raise TypeError(msg)
        widget = type2Widget(args[0])
        if isinstance(widget, BoolCheckBox):
            widget.setTristate(True)
            return widget
        if isinstance(widget, IntLineEdit):
            widget.setDefaultDataValue(None)
            return widget

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


class _MISSING:
    """Sentinel object to indicate empty field."""

    pass


MISSING = _MISSING()


class EmptyIntValidator(QtGui.QIntValidator):
    """Validator which accpets integer and empty string"""

    def validate(self, input: str, pos: int) -> Tuple[QtGui.QValidator.State, str, int]:
        state, ret_input, ret_pos = super().validate(input, pos)
        if not input:
            state = QtGui.QValidator.State.Acceptable
        return (state, ret_input, ret_pos)


class IntLineEdit(QtWidgets.QLineEdit):
    """
    Line edit for integer field.

    :meth:`dataValue` returns the current value. When editing is finished,
    :attr:`dataValueChanged` signal is emitted. :meth:`setDataValue` changes the
    text on the line edit.

    When the line edit is empty, :meth:`defaultDataValue` is used as data value.
    Default value can be integer or ``None``, thus supporting the field with
    ``Optional[int]`` type.

    When the default value is :obj:`MISSING`, it indicates that the field has no
    default value. Data value with empty string is :obj:`MISSING` in this case
    and should be specially handled.

    """

    dataValueChanged = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._default_data_value = MISSING
        self.setValidator(EmptyIntValidator(self))

        self.editingFinished.connect(self.emitDataValueChanged)

    def dataName(self) -> str:
        return self.placeholderText()

    def setDataName(self, name: str):
        self.setPlaceholderText(name)
        self.setToolTip(name)

    def defaultDataValue(self) -> Union[int, None, _MISSING]:
        return self._default_data_value

    def hasDefaultDataValue(self) -> bool:
        return self.defaultDataValue() is not MISSING

    def setDefaultDataValue(self, val: Union[int, None, _MISSING]):
        self._default_data_value = val

    def dataValue(self) -> Union[int, None, _MISSING]:
        text = self.text()
        if text:
            val: Union[int, None, _MISSING] = int(text)
        else:
            val = self.defaultDataValue()
        return val

    def setDataValue(self, val: Union[int, None, _MISSING]):
        if val is MISSING:
            self.setText("")
        elif val is None:
            self.setText("")
        else:
            self.setText(str(val))

    def emitDataValueChanged(self):
        val = self.dataValue()
        self.dataValueChanged.emit(val)
