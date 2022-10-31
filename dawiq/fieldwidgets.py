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
    "BoolCheckBox",
    "EmptyIntValidator",
    "IntLineEdit",
    "EmptyFloatValidator",
    "FloatLineEdit",
    "StrLineEdit",
    "EnumComboBox",
    "TupleGroupBox",
]


class BoolCheckBox(QtWidgets.QCheckBox):
    """
    Checkbox for fuzzy boolean value.

    Check state of the box represents the field value. If the box is checked, the
    value is True. If unchecked, the value is False. ``Qt.PartiallyChecked``
    represents ``None``.

    Setting the field value changes the check state. Because of the nature of
    check box, it is impossible to define empty state of the widget which means
    that ``None`` always represent a valid value. If tristate is enabled,
    setting ``None`` sets the state as ``Qt.PartiallyChecked``. If tristate is
    disabled, ``None`` is treated as ``False`` and unchecks the box.

    """

    fieldValueChanged = QtCore.Signal(object)
    fieldEdited = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._block_dataValueChanged = False

        self.stateChanged.connect(self.emitDataValueChanged)
        self.stateChanged.connect(self._onStateChange)
        self.clicked.connect(self.fieldEdited)

    def fieldValue(self) -> Optional[bool]:
        checkstate = self.checkState()
        if checkstate == QtCore.Qt.CheckState.Checked:
            state = True
        elif checkstate == QtCore.Qt.CheckState.Unchecked:
            state = False
        else:
            state = None
        return state

    def setFieldValue(self, value: Optional[bool]):
        if value is None and not self.isTristate():
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
        self.setCheckState(state)

    def _onStateChange(self, checkstate: Union[int, QtCore.Qt.CheckState]):
        checkstate = QtCore.Qt.CheckState(checkstate)
        if checkstate == QtCore.Qt.CheckState.Checked:
            state = True
        elif checkstate == QtCore.Qt.CheckState.Unchecked:
            state = False
        else:
            state = None
        self.fieldValueChanged.emit(state)

    def fieldName(self) -> str:
        return self.text()

    def setFieldName(self, name: str):
        self.setText(name)
        self.setToolTip(name)

    def setRequired(self, required: bool):
        # Check box is always occupied
        pass

    # below will be deleted

    dataValue = fieldValue
    dataValueChanged = QtCore.Signal(object)

    def setDataValue(self, value: Optional[bool]):
        if value is None and not self.isTristate():
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
        # wil be deleted
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

    If the text is not empty, the field value is the integer that the text is
    converted to. If the line edit is empty or the text cannot be converted to
    integer, ``None`` is the field value. Setting ``None`` as field value clears
    the line edit.

    """

    fieldValueChanged = QtCore.Signal(object)
    fieldEdited = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setValidator(EmptyIntValidator(self))

        self.editingFinished.connect(self.emitDataValueChanged)
        self.textChanged.connect(self._onTextChange)
        self.editingFinished.connect(self.fieldEdited)

    def fieldValue(self) -> Optional[int]:
        text = self.text()
        if not text:
            val: Optional[int] = None
        else:
            try:
                val = int(text)
            except ValueError:
                val = None
        return val

    def setFieldValue(self, value: Optional[int]):
        if value is None:
            txt = ""
        elif isinstance(value, int):
            txt = str(int(value))
        else:
            raise TypeError(f"IntLineEdit value must be int, not {type(value)}")
        self.setText(txt)

    def _onTextChange(self, text: str):
        if not text:
            val: Optional[int] = None
        else:
            try:
                val = int(text)
            except ValueError:
                val = None
        self.fieldValueChanged.emit(val)

    def fieldName(self) -> str:
        return self.placeholderText()

    def setFieldName(self, name: str):
        self.setPlaceholderText(name)
        self.setToolTip(name)

    def setRequired(self, required: bool):
        if required and self.dataValue() is None:
            requires = True
        else:
            requires = False
        if self.property("requiresFieldData") != requires:
            self.setProperty("requiresFieldData", requires)
            self.style().unpolish(self)
            self.style().polish(self)

    # below will be deleted

    dataValue = fieldValue
    dataValueChanged = QtCore.Signal(object)

    setDataValue = setFieldValue

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

    If the text is not empty, the field value is the float that the text is
    converted to. If the line edit is empty or the text cannot be converted to
    float, ``None`` is the field value. Setting ``None`` as field value clears
    the line edit.
    """

    fieldValueChanged = QtCore.Signal(object)
    fieldEdited = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setValidator(EmptyFloatValidator(self))

        self.editingFinished.connect(self.emitDataValueChanged)
        self.textChanged.connect(self._onTextChange)
        self.editingFinished.connect(self.fieldEdited)

    def fieldValue(self) -> Optional[float]:
        text = self.text()
        if not text:
            val: Optional[float] = None
        else:
            try:
                val = float(text)
            except ValueError:
                val = None
        return val

    def setFieldValue(self, value: Optional[float]):
        if value is None:
            txt = ""
        elif isinstance(value, float):
            txt = str(float(value))
        else:
            raise TypeError(f"FloatLineEdit value must be float, not {type(value)}")
        self.setText(txt)

    def _onTextChange(self, text: str):
        if not text:
            val: Optional[float] = None
        else:
            try:
                val = float(text)
            except ValueError:
                val = None
        self.fieldValueChanged.emit(val)

    def fieldName(self) -> str:
        return self.placeholderText()

    def setFieldName(self, name: str):
        self.setPlaceholderText(name)
        self.setToolTip(name)

    def setRequired(self, required: bool):
        if required and self.dataValue() is None:
            requires = True
        else:
            requires = False
        if self.property("requiresFieldData") != requires:
            self.setProperty("requiresFieldData", requires)
            self.style().unpolish(self)
            self.style().polish(self)

    # below will be deleted

    dataValue = fieldValue
    dataValueChanged = QtCore.Signal(object)

    setDataValue = setFieldValue

    def emitDataValueChanged(self):
        val = self.dataValue()
        self.dataValueChanged.emit(val)


class StrLineEdit(QtWidgets.QLineEdit):
    """
    Line edit for string value.

    If the line edit is empty, field data is empty string and never ``None``.

    """

    fieldValueChanged = QtCore.Signal(str)
    fieldEdited = QtCore.Signal()

    dataValueChanged = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.editingFinished.connect(self.emitDataValueChanged)
        self.textChanged.connect(self._onTextChange)
        self.editingFinished.connect(self.fieldEdited)

    def fieldValue(self) -> str:
        return self.text()

    def setFieldValue(self, value: Optional[str]):
        if value is None:
            txt = ""
        elif isinstance(value, str):
            txt = str(value)  # type: ignore[assignment]
        else:
            raise TypeError(f"StrLineEdit data must be str, not {type(value)}")
        self.setText(txt)

    def _onTextChange(self, text: str):
        self.fieldValueChanged.emit(text)

    def fieldName(self) -> str:
        return self.placeholderText()

    def setFieldName(self, name: str):
        self.setPlaceholderText(name)
        self.setToolTip(name)

    def setRequired(self, required: bool):
        if required and self.dataValue() is None:
            requires = True
        else:
            requires = False
        if self.property("requiresFieldData") != requires:
            self.setProperty("requiresFieldData", requires)
            self.style().unpolish(self)
            self.style().polish(self)

    # below will be deleted

    dataValue = fieldValue
    dataValueChanged = QtCore.Signal(str)

    setDataValue = setFieldValue

    def emitDataValueChanged(self):
        val = self.dataValue()
        self.dataValueChanged.emit(val)


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
    :obj:`None`

    :meth:`setDataValue` sets the current index. If :obj:`None` is passed,
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

    def dataValue(self) -> Optional[Enum]:
        index = self.currentIndex()
        if index == -1:
            ret = None
        else:
            ret = self.itemData(index)
        return ret

    def setDataValue(self, value: Optional[Enum]):
        if value is None:
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
        if required and self.dataValue() is None:
            requires = True
        else:
            requires = False
        if self.property("requiresFieldData") != requires:
            self.setProperty("requiresFieldData", requires)
            self.style().unpolish(self)
            self.style().polish(self)


V = TypeVar("V", bound="TupleGroupBox")


class TupleGroupBox(QtWidgets.QGroupBox):
    """
    Group box for tuple data with fixed length.

    This is the group box which contains field widgets as subwidgets. Data value
    is constructed from the data of subwidgets as tuple.

    :meth:`dataValue` returns the current tuple value. When data value of any
    subwidget is changed by the user, :attr:`dataValueChanged` signal is emitted.
    :meth:`setDataValue` changes the data of subwidgets.

    Data value is the tuple containing subwidget data, and never :obj:`None`.

    :meth:`setDataValue` sets the subwidget data. If :obj:`None` is passed,
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

    def setDataValue(self, value: Optional[tuple]):
        self._block_dataValueChanged = True
        if value is None:
            for i in range(self.count()):
                widget = self.widget(i)
                if widget is None:
                    break
                widget.setDataValue(None)
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
        """Recursively set *required* to all subwidgets."""
        for i in range(self.count()):
            widget = self.widget(i)
            if widget is None:
                continue
            widget.setRequired(required)
