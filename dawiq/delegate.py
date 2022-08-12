"""
Dataclass delegate
==================

"""

import dataclasses
from .qt_compat import QtWidgets
from .fieldwidgets import MISSING
from .datawidget import DataWidget
from .typing import DataclassProtocol
from typing import Optional, Type, Dict, Any


__all__ = [
    "convertFromQt",
    "convertToQt",
    "DataclassDelegate",
    "DataclassMapper",
]


def convertFromQt(
    dcls: Type[DataclassProtocol],
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convert dict from :class:`DataWidget` to structured dict for dataclass.

    If the field value does not exist or is :obj:`MISSING`, default value of the
    field is used. If there is no default value, the field is not included in
    the resulting dictionary.

    Field may define `fromQt_converter` metadata to convert the widget data to
    field data. It is a unary callable which takes the widget data and returns
    the field data.

    If the data is nested or default value is used, field data itself may be
    passed to the converter. Therefore `fromQt_converter` must perform type check
    to distinguish the field data input and widget data input.

    Examples
    ========

    >>> from dataclasses import dataclass, field
    >>> from dawiq.delegate import convertFromQt
    >>> def conv(arg):
    ...     if isinstance(arg, tuple):
    ...         return arg
    ...     return (arg,)
    >>> @dataclass
    ... class Cls:
    ...     x: tuple = field(metadata=dict(fromQt_converter=conv), default=(1,))
    >>> convertFromQt(Cls, dict(x=10))
    {'x': (10,)}
    >>> convertFromQt(Cls, dict())
    {'x': (1,)}

    """
    # Return value is not dataclass but dictionary because necessary fields might
    # be missing from the widget.
    ret = {}
    for f in dataclasses.fields(dcls):
        val = data.get(f.name, MISSING)

        if val is MISSING:
            default = f.default
            if default is dataclasses.MISSING:
                continue
            val = default  # this may be dataclass instance

        if dataclasses.is_dataclass(f.type):
            if dataclasses.is_dataclass(val) and not isinstance(val, type):
                # convert dataclass instance to dict
                val = dataclasses.asdict(val)
            val = convertFromQt(f.type, val)

        converter = f.metadata.get("fromQt_converter", None)
        if converter is not None:
            val = converter(val)
        ret[f.name] = val
    return ret


def convertToQt(
    dcls: Type[DataclassProtocol],
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convert structured dict from dataclass to dict for :class:`DataWidget`.

    If the field does not exist in the data, :obj:`MISSING` is passed as its
    value instead.

    Field may define `toQt_converter` metadata to convert the field data to
    widget data. It is a unary callable which takes the field data and returns
    the widget data.

    Examples
    ========

    >>> from dataclasses import dataclass, field
    >>> from dawiq.delegate import convertToQt
    >>> @dataclass
    ... class Cls:
    ...     x: tuple = field(metadata=dict(toQt_converter=lambda tup: tup[0]))
    >>> convertToQt(Cls, dict(x=(10,)))
    {'x': 10}

    """
    ret = {}
    for f in dataclasses.fields(dcls):
        val = data.get(f.name, MISSING)
        if val is MISSING:
            pass
        elif dataclasses.is_dataclass(f.type):
            val = convertToQt(f.type, val)
        converter = f.metadata.get("toQt_converter", None)
        if val is not MISSING and converter is not None:
            val = converter(val)
        ret[f.name] = val
    return ret


class DataclassDelegate(QtWidgets.QStyledItemDelegate):
    """Delegate to update the model and editor with structured dictionary."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dataclass_type = None

    def dataclassType(self) -> Optional[Type[DataclassProtocol]]:
        return self._dataclass_type

    def setDataclassType(self, dcls: Optional[Type[DataclassProtocol]]):
        self._dataclass_type = dcls

    def setModelData(self, editor, model, index):
        """
        Set the data from *editor* to the item of *model* at *index*.

        If *editor* is :class:`DataWidget`, its data is converted by
        :func:`convertFromQt` before being set to the model.
        """
        if isinstance(editor, DataWidget):
            dcls = self.dataclassType()
            data = editor.dataValue()
            if dcls is not None:
                data = convertFromQt(dcls, data)
            model.setData(index, data)
        else:
            super().setModelData(editor, model, index)

    def setEditorData(self, editor, index):
        """
        Set the data from *index* to *editor*.

        If *editor* is :class:`DataWidget`, the data is converted by
        :func:`convertToQt` before being set to the editor.
        """
        if isinstance(editor, DataWidget):
            dcls = self.dataclassType()
            data = index.data()
            if data is None:
                data = {}
            if dcls is not None:
                data = convertToQt(dcls, data)
            editor.setDataValue(data)
        else:
            super().setEditorData(editor, index)


class DataclassMapper(QtWidgets.QDataWidgetMapper):
    """
    Mapper between :class:`DataWidget` and model.

    Notes
    =====

    When mapping :class:`DataWidget`, *propertyName* argument must not be passed.
    """

    def addMapping(self, widget, section, propertyName=b""):
        super().addMapping(widget, section, propertyName)
        if isinstance(widget, DataWidget):
            widget.dataValueChanged.connect(self.submit)

    def removeMapping(self, widget):
        super().removeMapping(widget)
        if isinstance(widget, DataWidget):
            widget.dataValueChanged.disconnect(self.submit)
