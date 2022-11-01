"""
Data field widgets
==================

:mod:`dawiq.fieldwidgets` provides widgets to represent the fields of the
dataclass. Widgets are compatible to :class:`dawiq.typing.FieldWidgetProtocol`.
"""

from .qt_compat import QtCore, QtWidgets, QtGui
from enum import Enum
from typing import Optional, Union, Tuple, TypeVar, Type, Any
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
    value is True. If unchecked, the value is False.

    If tristate is enabled, setting ``None`` as the field value sets the state as
    ``Qt.PartiallyChecked``. If tristate is disabled, ``None`` is treated as
    ``False`` and unchecks the box.

    """

    fieldValueChanged = QtCore.Signal(object)
    fieldEdited = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
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
        if required and self.fieldValue() is None:
            requires = True
        else:
            requires = False
        if self.property("requiresFieldValue") != requires:
            self.setProperty("requiresFieldValue", requires)
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
        if required and self.fieldValue() is None:
            requires = True
        else:
            requires = False
        if self.property("requiresFieldValue") != requires:
            self.setProperty("requiresFieldValue", requires)
            self.style().unpolish(self)
            self.style().polish(self)


class StrLineEdit(QtWidgets.QLineEdit):
    """
    Line edit for string value.

    If the line edit is empty, field data is empty string. Setting ``None`` as
    the field value clears the widget.

    """

    fieldValueChanged = QtCore.Signal(str)
    fieldEdited = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
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
        if required and self.fieldValue() is None:
            requires = True
        else:
            requires = False
        if self.property("requiresFieldValue") != requires:
            self.setProperty("requiresFieldValue", requires)
            self.style().unpolish(self)
            self.style().polish(self)


T = TypeVar("T", bound="EnumComboBox")


class EnumComboBox(QtWidgets.QComboBox):
    """
    Combo box for :class:`enum.Enum` type.

    Standard way to construct this widget is by :meth:`fromEnum` class method.
    N-th item contains N-th member of the Enum as its data.

    Enum instance is stored in item data. Field value is the data of currently
    activated item. If the current index is -1, field value is ``None``.

    """

    fieldValueChanged = QtCore.Signal(object)
    fieldEdited = QtCore.Signal()

    @classmethod
    def fromEnum(cls: Type[T], enum: Type[Enum]) -> T:
        obj = cls()
        for e in enum:
            obj.addItem(e.name, userData=e)
        obj.setCurrentIndex(-1)
        return obj

    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentIndexChanged.connect(self._onCurrentIndexChange)
        self.activated.connect(self.fieldEdited)

    def fieldValue(self) -> Optional[Enum]:
        index = self.currentIndex()
        if index == -1:
            ret = None
        else:
            ret = self.itemData(index)
        return ret

    def setFieldValue(self, value: Optional[Enum]):
        if value is None:
            index = -1
        elif isinstance(value, Enum):
            index = self.findData(value)
        else:
            raise TypeError(f"EnumComboBox data must be Enum, not {type(value)}")
        self.setCurrentIndex(index)

    def _onCurrentIndexChange(self, index: int):
        data = self.itemData(index)
        self.fieldValueChanged.emit(data)

    def fieldName(self) -> str:
        return self.placeholderText()

    def setFieldName(self, name: str):
        self.setPlaceholderText(name)
        self.setToolTip(name)

    def setRequired(self, required: bool):
        if required and self.fieldValue() is None:
            requires = True
        else:
            requires = False
        if self.property("requiresFieldValue") != requires:
            self.setProperty("requiresFieldValue", requires)
            self.style().unpolish(self)
            self.style().polish(self)


V = TypeVar("V", bound="TupleGroupBox")


class TupleGroupBox(QtWidgets.QGroupBox):
    """
    Group box for tuple with fixed length.

    This is the group box which contains field widgets as subwidgets. Field value
    is the tuple of subwidgets values.

    """

    fieldValueChanged = QtCore.Signal(tuple)
    fieldEdited = QtCore.Signal()

    def __init__(
        self,
        orientation: QtCore.Qt.Orientation = QtCore.Qt.Orientation.Horizontal,
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
        """Insert the widget to layout and connect the signals."""
        for i in range(self.count()):
            w = self.widget(i)
            if w is None:
                break
        widget.fieldValueChanged.connect(self._onSubfieldValueChange)
        widget.fieldEdited.connect(self.fieldEdited)
        self.layout().insertWidget(index, widget, stretch, alignment)

    def addWidget(
        self,
        widget: FieldWidgetProtocol,
        stretch: int = 0,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag(0),
    ):
        """Add the widget to layout and connect the signals."""
        for i in range(self.count()):
            w = self.widget(i)
            if w is None:
                break
        widget.fieldValueChanged.connect(self._onSubfieldValueChange)
        widget.fieldEdited.connect(self.fieldEdited)
        self.layout().addWidget(widget, stretch, alignment)

    def removeWidget(self, widget: FieldWidgetProtocol):
        """Remove the widget from layout and disconnect the signals."""
        for i in range(self.count()):
            w = self.widget(i)
            if w is None:
                break
            if w == widget:
                widget.fieldValueChanged.disconnect(self._onSubfieldValueChange)
                widget.fieldEdited.disconnect(self.fieldEdited)
                break
        self.layout().removeWidget(widget)

    def fieldValue(self) -> tuple:
        ret = []
        for i in range(self.count()):
            widget = self.widget(i)
            if widget is None:
                break
            ret.append(widget.fieldValue())
        return tuple(ret)

    def setFieldValue(self, value: Optional[tuple]):
        if value is None:
            value = tuple(None for _ in range(self.count()))
        elif isinstance(value, tuple):
            pass
        else:
            raise TypeError(f"TupleGroupBox value must be tuple, not {type(value)}")

        for i in range(self.count()):
            widget = self.widget(i)
            if widget is None:
                break
            widget.fieldValueChanged.disconnect(self._onSubfieldValueChange)
            widget.setFieldValue(value[i])
            widget.fieldValueChanged.connect(self._onSubfieldValueChange)
        self.fieldValueChanged.emit(value)

    def _onSubfieldValueChange(self, value: Any):
        self.fieldValueChanged.emit(self.fieldValue())

    def fieldName(self) -> str:
        return self.title()

    def setFieldName(self, name: str):
        self.setTitle(name)
        self.setToolTip(name)

    def setRequired(self, required: bool):
        """Recursively set *required* to all subwidgets."""
        for i in range(self.count()):
            widget = self.widget(i)
            if widget is None:
                continue
            widget.setRequired(required)
