"""
Data field widgets
==================

:mod:`dawiq.fieldwidgets` provides widgets to represent the fields of the
dataclass. Widgets are compatible to :class:`dawiq.typing.FieldWidgetProtocol`.
"""

from .qt_compat import QtCore, QtWidgets, QtGui
from typing import Optional, Union, Tuple


__all__ = [
    "MISSING",
    "BoolCheckBox",
    "EmptyIntValidator",
    "IntLineEdit",
    "EmptyFloatValidator",
    "FloatLineEdit",
    "StrLineEdit",
]


class _MISSING:
    """Sentinel object to indicate empty field."""

    pass


MISSING = _MISSING()


class BoolCheckBox(QtWidgets.QCheckBox):
    """
    Checkbox for fuzzy boolean value.

    :meth:`dataValue` returns the current value. When the check state is changed,
    :attr:`dataValueChanged` signal is emitted. :meth:`setDataValue` changes the
    check state of the checkbox.

    If the box is checked, the data value is True. If unchecked, the value is
    False. Else, e.g. ``Qt.PartiallyChecked``, the value is None.

    Because of the nature of check box, it is impossible to define empty state of
    the widget. :meth:`dataValue` is always either True, False or None, and never
    :obj:`MISSING`. :meth:`setDataValue` treats :obj:`MISSING` as False.

    """

    dataValueChanged = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.stateChanged.connect(self.emitDataValueChanged)

    def fieldName(self) -> str:
        return self.text()

    def setFieldName(self, name: str):
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

    def setDataValue(self, value: Union[Optional[bool], _MISSING]):
        if value is MISSING:
            value = False

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


class EmptyIntValidator(QtGui.QIntValidator):
    """Validator which accpets integer and empty string"""

    def validate(self, input: str, pos: int) -> Tuple[QtGui.QValidator.State, str, int]:
        state, ret_input, ret_pos = super().validate(input, pos)
        if not input:
            state = QtGui.QValidator.State.Acceptable
        return (state, ret_input, ret_pos)


class IntLineEdit(QtWidgets.QLineEdit):
    """
    Line edit for integer value.

    :meth:`dataValue` returns the current value. When editing is finished,
    :attr:`dataValueChanged` signal is emitted. :meth:`setDataValue` changes the
    text on the line edit.

    If the text is not empty, the data value is the integer that the string is
    converted to. If the line edit is empty, :obj:`MISSING` is the data value.

    :meth:`setDataValue` sets the line edit text. If :obj:`MISSING` is passed,
    line edit is cleared.

    """

    dataValueChanged = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setValidator(EmptyIntValidator(self))

        self.editingFinished.connect(self.emitDataValueChanged)

    def fieldName(self) -> str:
        return self.placeholderText()

    def setFieldName(self, name: str):
        self.setPlaceholderText(name)
        self.setToolTip(name)

    def dataValue(self) -> Union[int, _MISSING]:
        text = self.text()

        if not text:
            val: Union[int, _MISSING] = MISSING
        else:
            try:
                val = int(text)
            except ValueError:
                val = MISSING
        return val

    def setDataValue(self, val: Union[int, _MISSING]):
        if val is MISSING:
            txt = ""
        else:
            txt = str(val)
        self.setText(txt)
        self.emitDataValueChanged()

    def emitDataValueChanged(self):
        val = self.dataValue()
        self.dataValueChanged.emit(val)


class EmptyFloatValidator(QtGui.QDoubleValidator):
    """Validator which accpets float and empty string"""

    def validate(self, input: str, pos: int) -> Tuple[QtGui.QValidator.State, str, int]:
        state, ret_input, ret_pos = super().validate(input, pos)
        if not input:
            state = QtGui.QValidator.State.Acceptable
        return (state, ret_input, ret_pos)


class FloatLineEdit(QtWidgets.QLineEdit):
    """
    Line edit for float value.

    :meth:`dataValue` returns the current value. When editing is finished,
    :attr:`dataValueChanged` signal is emitted. :meth:`setDataValue` changes the
    text on the line edit.

    If the text is not empty, the data value is the float that the string is
    converted to. If the line edit is empty, :obj:`MISSING` is the data value.

    :meth:`setDataValue` sets the line edit text. If :obj:`MISSING` is passed,
    line edit is cleared.

    """

    dataValueChanged = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setValidator(EmptyFloatValidator(self))

        self.editingFinished.connect(self.emitDataValueChanged)

    def fieldName(self) -> str:
        return self.placeholderText()

    def setFieldName(self, name: str):
        self.setPlaceholderText(name)
        self.setToolTip(name)

    def dataValue(self) -> Union[float, _MISSING]:
        text = self.text()

        if not text:
            val: Union[float, _MISSING] = MISSING
        else:
            try:
                val = float(text)
            except ValueError:
                val = MISSING
        return val

    def setDataValue(self, val: Union[float, _MISSING]):
        if val is MISSING:
            txt = ""
        else:
            txt = str(val)
        self.setText(txt)
        self.emitDataValueChanged()

    def emitDataValueChanged(self):
        val = self.dataValue()
        self.dataValueChanged.emit(val)


class StrLineEdit(QtWidgets.QLineEdit):
    """
    Line edit for string value.

    :meth:`dataValue` returns the current value. When editing is finished,
    :attr:`dataValueChanged` signal is emitted. :meth:`setDataValue` changes the
    text on the line edit.

    Data value is the text of line edit. If the line edit is empty, data value is
    empty string. Thus, the data value is never :obj:`MISSING`.

    :meth:`setDataValue` sets the line edit text. If :obj:`MISSING` is passed,
    line edit is cleared.

    """

    dataValueChanged = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.editingFinished.connect(self.emitDataValueChanged)

    def fieldName(self) -> str:
        return self.placeholderText()

    def setFieldName(self, name: str):
        self.setPlaceholderText(name)
        self.setToolTip(name)

    def dataValue(self) -> str:
        return self.text()

    def setDataValue(self, val: Union[str, _MISSING]):
        if val is MISSING:
            txt = ""
        else:
            txt = val  # type: ignore[assignment]
        self.setText(txt)
        self.emitDataValueChanged()

    def emitDataValueChanged(self):
        val = self.dataValue()
        self.dataValueChanged.emit(val)
