"""
Data field widgets
==================

:mod:`dawiq.fieldwidgets` provides widgets to represent the fields of the
dataclass. Widgets are compatible to :class:`dawiq.typing.FieldWidgetProtocol`.
"""

from .qt_compat import QtCore, QtWidgets, QtGui
from typing import Optional, Union, Tuple, Any


__all__ = [
    "BoolCheckBox",
    "MISSING",
    "EmptyIntValidator",
    "IntLineEdit",
]


class BoolCheckBox(QtWidgets.QCheckBox):
    """
    Checkbox for fuzzy boolean value.

    :meth:`dataValue` returns the current value. When the check state is changed,
    :attr:`dataValueChanged` signal is emitted. :meth:`setDataValue` changes the
    check state of the checkbox.

    If the box is checked, the data value is True. If unchecked, the value is
    False. Else, e.g. ``Qt.PartiallyChecked``, the value is None.

    Because of the nature of check box, it is impossible to define empty state of
    the widget. Data value is always either True, False or None, and never
    :obj:`MISSING`.

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
    Line edit for integer value.

    :meth:`dataValue` returns the current value. When editing is finished,
    :attr:`dataValueChanged` signal is emitted. :meth:`setDataValue` changes the
    text on the line edit.

    If the text is not empty, the data value is the integer that the string is
    converted to. If the string is empty, :meth:`defaultValue` is used instead.

    """

    dataValueChanged = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._default_data_value = MISSING
        self.setValidator(EmptyIntValidator(self))

        self.editingFinished.connect(self.emitDataValueChanged)

    def fieldName(self) -> str:
        return self.placeholderText()

    def setFieldName(self, name: str):
        self.setPlaceholderText(name)
        self.setToolTip(name)

    def defaultDataValue(self) -> Any:
        """
        Value which is used as :meth:`dataValue` if the text is empty.

        Default value can be any object. :obj:`MISSING` indicates there is no
        default value and thus the field is null when the text is empty.

        """
        return self._default_data_value

    def hasDefaultDataValue(self) -> bool:
        """Return True if :meth:`defaultDataValue` is not :obj:`MISSING`."""
        return self.defaultDataValue() is not MISSING

    def setDefaultDataValue(self, val: Any):
        """Set :meth:`defaultDataValue`."""
        self._default_data_value = val

    def dataValue(self) -> Any:
        text = self.text()
        if text:
            val: Any = int(text)
        else:
            val = self.defaultDataValue()
        return val

    def setDataValue(self, val: Any):
        if val is MISSING:
            self.setText("")
        elif val is None:
            self.setText("")
        else:
            self.setText(str(val))

    def emitDataValueChanged(self):
        val = self.dataValue()
        self.dataValueChanged.emit(val)
