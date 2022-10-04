"""
Data field widgets
==================

:mod:`dawiq.fieldwidgets` provides widgets to represent the fields of the
dataclass. Widgets are compatible to :class:`dawiq.typing.FieldWidgetProtocol`.
"""

from .qt_compat import QtCore, QtWidgets, QtGui
from enum import Enum
from typing import Optional, Union, Tuple, TypeVar, Type
from .typing import FieldWidgetProtocol


__all__ = [
    "MISSING",
    "BoolCheckBox",
    "EmptyIntValidator",
    "IntLineEdit",
    "EmptyFloatValidator",
    "FloatLineEdit",
    "StrLineEdit",
    "EnumComboBox",
    "TupleGroupBox",
]


class _MISSING:
    """Sentinel object to indicate empty field."""

    pass


MISSING = _MISSING()


class BoolCheckBox(QtWidgets.QCheckBox):
    """
    Checkbox for fuzzy boolean value.

    :meth:`dataValue` returns the current value. When the check state is changed
    by user, :attr:`dataValueChanged` signal is emitted. :meth:`setDataValue`
    changes the check state of the checkbox.

    If the box is checked, the data value is True. If unchecked, the value is
    False. Else, e.g. ``Qt.PartiallyChecked``, the value is None.

    Because of the nature of check box, it is impossible to define empty state of
    the widget. :meth:`dataValue` is always either True, False or None, and never
    :obj:`MISSING`. :meth:`setDataValue` treats :obj:`MISSING` as False.

    """

    dataValueChanged = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._block_dataValueChanged = False

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
        elif value is None:
            state = QtCore.Qt.CheckState.PartiallyChecked
        else:
            raise TypeError(
                f"BoolCheckBox data must be True, False or None, not {type(value)}"
            )

        self._block_dataValueChanged = True
        self.setCheckState(state)
        self._block_dataValueChanged = False

    def emitDataValueChanged(self, checkstate: Union[int, QtCore.Qt.CheckState]):
        if self._block_dataValueChanged:
            return

        checkstate = QtCore.Qt.CheckState(checkstate)
        if checkstate == QtCore.Qt.CheckState.Checked:
            state = True
        elif checkstate == QtCore.Qt.CheckState.Unchecked:
            state = False
        else:
            state = None
        self.dataValueChanged.emit(state)

    def setRequired(self, required: bool):
        pass


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
        elif isinstance(val, int):
            txt = str(int(val))
        else:
            raise TypeError(f"IntLineEdit data must be int, not {type(val)}")
        self.setText(txt)

    def emitDataValueChanged(self):
        val = self.dataValue()
        self.dataValueChanged.emit(val)

    def setRequired(self, required: bool):
        if required and self.dataValue() is MISSING:
            requires = True
        else:
            requires = False
        self.setProperty("requiresFieldData", requires)
        self.style().unpolish(self)
        self.style().polish(self)


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
        elif isinstance(val, float):
            txt = str(float(val))
        else:
            raise TypeError(f"FloatLineEdit data must be float, not {type(val)}")
        self.setText(txt)

    def emitDataValueChanged(self):
        val = self.dataValue()
        self.dataValueChanged.emit(val)

    def setRequired(self, required: bool):
        if required and self.dataValue() is MISSING:
            requires = True
        else:
            requires = False
        self.setProperty("requiresFieldData", requires)
        self.style().unpolish(self)
        self.style().polish(self)


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
        elif isinstance(val, str):
            txt = str(val)  # type: ignore[assignment]
        else:
            raise TypeError(f"StrLineEdit data must be str, not {type(val)}")
        self.setText(txt)

    def emitDataValueChanged(self):
        val = self.dataValue()
        self.dataValueChanged.emit(val)

    def setRequired(self, required: bool):
        if required and self.dataValue() is MISSING:
            requires = True
        else:
            requires = False
        self.setProperty("requiresFieldData", requires)
        self.style().unpolish(self)
        self.style().polish(self)


T = TypeVar("T", bound="EnumComboBox")


class EnumComboBox(QtWidgets.QComboBox):
    """
    Combo box for enum type.

    Standard way to construct this widget is by :meth:`fromEnum` class method.
    N-th item contains N-th member of the Enum as its data.

    :meth:`dataValue` returns the current member. When current index is changed
    by user, :attr:`dataValueChanged` signal is emitted. :meth:`setDataValue`
    changes the current index.

    Data value is the Enum member. If the current index is empty, data value is
    :obj:`MISSING`

    :meth:`setDataValue` sets the current index. If :obj:`MISSING` is passed,
    index is set to -1.

    """

    dataValueChanged = QtCore.Signal(object)

    @classmethod
    def fromEnum(cls: Type[T], enum: Type[Enum]) -> T:
        obj = cls()
        for e in enum:
            obj.addItem(e.name, userData=e)
        obj.setCurrentIndex(-1)
        return obj

    def __init__(self, parent=None):
        super().__init__(parent)
        self._block_dataValueChanged = False

        self.currentIndexChanged.connect(self.emitDataValueChanged)

    def fieldName(self) -> str:
        return self.placeholderText()

    def setFieldName(self, name: str):
        self.setPlaceholderText(name)
        self.setToolTip(name)

    def dataValue(self) -> Union[Enum, _MISSING]:
        index = self.currentIndex()
        if index == -1:
            ret = MISSING
        else:
            ret = self.itemData(index)
        return ret

    def setDataValue(self, value: Union[Enum, _MISSING]):
        if value is MISSING:
            index = -1
        elif isinstance(value, Enum):
            index = self.findData(value)
        else:
            raise TypeError(f"EnumComboBox data must be Enum, not {type(value)}")
        self._block_dataValueChanged = True
        self.setCurrentIndex(index)
        self._block_dataValueChanged = False

    def emitDataValueChanged(self):
        if self._block_dataValueChanged:
            return
        val = self.dataValue()
        self.dataValueChanged.emit(val)

    def setRequired(self, required: bool):
        pass


V = TypeVar("V", bound="TupleGroupBox")


class TupleGroupBox(QtWidgets.QGroupBox):
    """
    Group box for tuple data with fixed length.

    This is the group box which contains field widgets as subwidgets. Data value
    is constructed from the data of subwidgets as tuple.

    :meth:`dataValue` returns the current tuple value. When data value of any
    subwidget is changed by user, :attr:`dataValueChanged` signal is emitted.
    :meth:`setDataValue` changes the data of subwidgets.

    Data value is the tuple containing subwidget data, and never :obj:`MISSING`.

    :meth:`setDataValue` sets the subwidget data. If :obj:`MISSING` is passed,
    it is propagated to all subwidget.

    """

    dataValueChanged = QtCore.Signal(tuple)

    def __init__(
        self,
        orientation: QtCore.Qt.Orientation = QtCore.Qt.Orientation.Horizontal,
        parent=None,
    ):
        super().__init__(parent)
        self._orientation = orientation
        self._block_dataValueChanged = False

        if orientation == QtCore.Qt.Orientation.Vertical:
            layout = QtWidgets.QVBoxLayout()
        elif orientation == QtCore.Qt.Orientation.Horizontal:
            layout = QtWidgets.QHBoxLayout()
        else:
            raise TypeError(f"Invalid orientation: {orientation}")
        self.setLayout(layout)

    def fieldName(self) -> str:
        return self.title()

    def setFieldName(self, name: str):
        self.setTitle(name)
        self.setToolTip(name)

    def orientation(self) -> QtCore.Qt.Orientation:
        """Orientation to stack the subwidgets."""
        return self._orientation

    def count(self) -> int:
        """Number of subwidgets."""
        return self.layout().count()

    def widget(self, index: int) -> Optional[FieldWidgetProtocol]:
        """
        Returns the subwidget at the given index, or None for invalid index.
        """
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
        """Insert the widget to layout and connect data value change signal."""
        for i in range(self.count()):
            w = self.widget(i)
            if w is None:
                break
        widget.dataValueChanged.connect(self.emitDataValueChanged)
        self.layout().insertWidget(index, widget, stretch, alignment)

    def addWidget(
        self,
        widget: FieldWidgetProtocol,
        stretch: int = 0,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag(0),
    ):
        """Add the widget to layout and connect data value change signal."""
        for i in range(self.count()):
            w = self.widget(i)
            if w is None:
                break
        widget.dataValueChanged.connect(self.emitDataValueChanged)
        self.layout().addWidget(widget, stretch, alignment)

    def removeWidget(self, widget: FieldWidgetProtocol):
        """
        Remove the widget from layout and disconnect data value change signal.
        """
        for i in range(self.count()):
            w = self.widget(i)
            if w is None:
                break
            if w == widget:
                widget.dataValueChanged.disconnect(self.emitDataValueChanged)
                break
        self.layout().removeWidget(widget)

    def dataValue(self) -> tuple:
        ret = []
        for i in range(self.count()):
            widget = self.widget(i)
            if widget is None:
                break
            ret.append(widget.dataValue())
        return tuple(ret)

    def setDataValue(self, value: Union[tuple, _MISSING]):
        self._block_dataValueChanged = True
        if value is MISSING:
            for i in range(self.count()):
                widget = self.widget(i)
                if widget is None:
                    break
                widget.setDataValue(MISSING)
        elif isinstance(value, tuple):
            for i in range(self.count()):
                widget = self.widget(i)
                if widget is None:
                    break
                widget.setDataValue(value[i])  # type: ignore[index]
        else:
            raise TypeError(f"TupleGroupBox data must be tuple, not {type(value)}")
        self._block_dataValueChanged = False

    def emitDataValueChanged(self):
        if self._block_dataValueChanged:
            return
        val = self.dataValue()
        self.dataValueChanged.emit(val)

    def setRequired(self, required: bool):
        pass
