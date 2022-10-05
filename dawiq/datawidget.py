"""
Data widget
===========

:mod:`dawiq.datawidget` provides :class:`DataWidget` to represent the data
structure established by the dataclass.
"""

from .qt_compat import QtCore, QtWidgets
from .fieldwidgets import (
    BoolCheckBox,
    IntLineEdit,
    FloatLineEdit,
    StrLineEdit,
    EnumComboBox,
    TupleGroupBox,
)
import dataclasses
from enum import Enum
from typing import Optional, Any, Union, Type, Callable, Dict, get_type_hints
from .typing import FieldWidgetProtocol, DataclassProtocol


__all__ = [
    "DataWidget",
    "type2Widget",
    "dataclass2Widget",
]


class DataWidget(QtWidgets.QGroupBox):
    """
    Group box for structured data.

    This is the group box which contains field widgets as subwidgets. Data value
    is constructed from the data of subwidgets as dict.

    :meth:`dataValue` returns the current dict value. When the data value of any
    subwidget is changed by user, :attr:`dataValueChanged` signal is emitted.
    :meth:`setDataValue` changes the data of subwidgets.

    Data value is the dict containing subwidget data, and never :obj:`None`.

    :meth:`setDataValue` sets the subwidget data. If :obj:`None` is passed,
    it is propagated to all subwidget.

    Notes
    =====

    This class can be constructed from :func:`dataclass2Widget`, but the widget
    does not store the dataclass type. To associate the data widget to the
    dataclass use :class:`DataclassDelegate`.

    """

    dataValueChanged = QtCore.Signal(dict)

    def __init__(
        self,
        orientation: QtCore.Qt.Orientation = QtCore.Qt.Orientation.Vertical,
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
            if widget.fieldName() == w.fieldName():
                raise KeyError(f"Data name '{widget.fieldName()}' is duplicate")
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
            if widget.fieldName() == w.fieldName():
                raise KeyError(f"Data name '{widget.fieldName()}' is duplicate")
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

    def dataValue(self) -> Dict[str, Any]:
        ret = {}
        for i in range(self.count()):
            w = self.widget(i)
            if w is None:
                break
            ret[w.fieldName()] = w.dataValue()
        return ret

    def setDataValue(self, data: Optional[Dict[str, Any]]):
        if data is None:
            data = {}

        self._block_dataValueChanged = True
        for i in range(self.count()):
            w = self.widget(i)
            if w is None:
                break
            val = data.get(w.fieldName(), None)  # type: ignore[union-attr]
            try:
                w.setDataValue(val)
            except TypeError:
                w.setDataValue(None)
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


def type2Widget(t: Any) -> FieldWidgetProtocol:
    """
    Construct the widget for given type annotation *t*.

    The following types are supported. Dataclass type is not converted here but
    by :func:`dataclass2Widget`.

    * :class:`enum.Enum` -> :class:`.EnumComboBox`
    * :class:`bool` -> :class:`.BoolCheckBox`
    * :obj:`Optional[bool]` -> :class:`.BoolCheckBox` with tristate
    * :class:`int` or :obj:`Optional[int]` -> :class:`.IntLineEdit`
    * :class:`float` or :obj:`Optional[float]` -> :class:`.FloatLineEdit`
    * :class:`str` or :obj:`Optional[str]` -> :class:`.StrLineEdit`
    * :obj:`Tuple` -> :class:`.TupleGroupBox` with nested field widgets

    For :obj:`Tuple`, its length must be finite (no :class:`Ellipsis` in args)
    and item types must be the supported type.

    """
    # When new type is supported, update intro.rst as well

    if isinstance(t, type) and issubclass(t, Enum):
        return EnumComboBox.fromEnum(t)
    if t is bool:
        return BoolCheckBox()
    if t is int:
        return IntLineEdit()
    if t is float:
        return FloatLineEdit()
    if t is str:
        return StrLineEdit()

    origin = getattr(t, "__origin__", None)  # t is tuple

    if origin is tuple:
        args = getattr(t, "__args__", None)
        if args is None:
            raise TypeError("%s does not have argument type" % t)
        if Ellipsis in args:
            txt = "Number of arguments of %s not fixed" % t
            raise TypeError(txt)

        subwidgets = [type2Widget(arg) for arg in args]
        tupwidget = TupleGroupBox()
        for w in subwidgets:
            tupwidget.addWidget(w)
        return tupwidget

    if origin is Union:
        args = [a for a in getattr(t, "__args__") if not isinstance(None, a)]
        if len(args) > 1:
            msg = f"Cannot convert Union with multiple types: {t}"
            raise TypeError(msg)
        # t is Optional[...]
        widget = type2Widget(args[0])
        if isinstance(widget, BoolCheckBox):
            widget.setTristate(True)
        return widget

    raise TypeError("Unknown type or annotation: %s" % t)


def dataclass2Widget(
    dcls: Type[DataclassProtocol],
    field_converter: Callable[[Any], FieldWidgetProtocol] = type2Widget,
    orientation: QtCore.Qt.Orientation = QtCore.Qt.Orientation.Vertical,
    globalns: Optional[Dict] = None,
    localns: Optional[Dict] = None,
    include_extras: bool = False,
) -> DataWidget:
    """
    Construct :class:`DataWidget` from *dcls*.

    Each field of *dcls* is converted to field widget by :func:`type2Widget`
    with the type hint of the field. If the field has ``Qt_typehint`` metadata,
    its value is used instead of the type hint.

    If the field type is dataclass, construction is recursively done with same
    parameters.

    Parameters
    ==========

    dcls
        Dataclass type which will be converted to widget.

    field_converter
        Callable to convert non-dataclass fields to widgets. Default is
        :class:`type2Widget`.

    orientation
        Argument for :class:`DataWidget`.

    globalns, localns, include_extras
        Arguments for :func:`get_type_hints` to resolve the forward-referenced
        type annotations.

    """
    widget = DataWidget(orientation)
    fields = dataclasses.fields(dcls)
    annots = get_type_hints(dcls, globalns, localns, include_extras)

    for f in fields:
        typehint = f.metadata.get("Qt_typehint", annots[f.name])
        if dataclasses.is_dataclass(typehint):
            field_w = dataclass2Widget(
                typehint,
                field_converter,
                orientation,
                globalns,
                localns,
                include_extras,
            )
        else:
            field_w = field_converter(typehint)  # type: ignore[assignment]
        field_w.setFieldName(f.name)
        widget.addWidget(field_w)
    return widget
