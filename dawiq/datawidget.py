"""
Data widget
===========

:mod:`dawiq.datawidget` provides :class:`DataWidget` to represent the data
structure established by the dataclass.
"""

from .qt_compat import QtCore, QtWidgets
from .fieldwidgets import BoolCheckBox, IntLineEdit
import dataclasses
from typing import Optional, Any, Union, Type, Callable, Dict, get_type_hints
from .typing import FieldWidgetProtocol, DataclassProtocol


__all__ = [
    "DataWidget",
    "type2Widget",
    "dataclass2Widget",
]


class DataWidget(QtWidgets.QGroupBox):
    """
    Widget to represent the data structure.
    """

    def __init__(
        self,
        orientation: QtCore.Qt.Orientation = QtCore.Qt.Orientation.Vertical,
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

    def dataName(self) -> str:
        return self.title()

    def setDataName(self, name: str):
        self.setTitle(name)

    def orientation(self) -> QtCore.Qt.Orientation:
        return self._orientation

    def count(self) -> int:
        return self.layout().count()

    def widget(self, index: int) -> Optional[FieldWidgetProtocol]:
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
        for i in range(self.count()):
            w = self.widget(i)
            if w is None:
                break
            elif widget.dataName() == w.dataName():
                raise KeyError(f"Data name '{widget.dataName()}' is duplicate")
        self.layout().insertWidget(index, widget, stretch, alignment)

    def addWidget(
        self,
        widget: FieldWidgetProtocol,
        stretch: int = 0,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag(0),
    ):
        for i in range(self.count()):
            w = self.widget(i)
            if w is None:
                break
            elif widget.dataName() == w.dataName():
                raise KeyError(f"Data name '{widget.dataName()}' is duplicate")
        self.layout().addWidget(widget, stretch, alignment)

    def removeWidget(self, widget: FieldWidgetProtocol):
        self.layout().removeWidget(widget)


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

    *field_converter* is a function which constructs the field widget from the
    type hint of the dataclass field.

    Each field is converted to field widget by passing its type hint to
    *field_converter* argument. If the field has `Qt_typehint` metadata, its
    value is passed to the converter instead.

    *orientation* is the argument for :class:`DataWidget`.
    *globalns*, *localns*, and *include_extras* are the arguments for
    :func:`get_type_hints` to resolve the forward-referenced type annotations.

    """
    widget = DataWidget(orientation)
    fields = dataclasses.fields(dcls)
    annots = get_type_hints(dcls, globalns, localns, include_extras)

    for f in fields:
        typehint = f.metadata.get("Qt_typehint", annots[f.name])
        field_w = field_converter(typehint)
        field_w.setDataName(f.name)
        widget.addWidget(field_w)
    return widget
