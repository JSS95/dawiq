"""
Dataclass delegate
==================

"""

import dataclasses
from .qt_compat import QtWidgets, QtCore
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

    If the field value does not exist or is :obj:`MISSING`, the field is not
    included in the resulting dictionary. Default value of the field is ignored.

    Field may define `fromQt_converter` metadata to convert the widget data to
    field data. It is a unary callable which takes the widget data and returns
    the field data.

    Examples
    ========

    >>> from dataclasses import dataclass, field
    >>> from dawiq import MISSING
    >>> from dawiq.delegate import convertFromQt
    >>> def conv(arg):
    ...     return (arg,)
    >>> @dataclass
    ... class Cls:
    ...     x: tuple = field(metadata=dict(fromQt_converter=conv), default=(1,))
    >>> convertFromQt(Cls, dict(x=10))
    {'x': (10,)}
    >>> convertFromQt(Cls, dict(x=MISSING))
    {}

    """
    # Return value is not dataclass but dictionary because necessary fields might
    # be missing from the widget.
    ret = {}
    for f in dataclasses.fields(dcls):
        val = data.get(f.name, MISSING)
        if val is MISSING:
            continue

        if dataclasses.is_dataclass(f.type):
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

    If the data does not have the value for a field, :obj:`MISSING` is passed as
    its value instead.

    Field may define `toQt_converter` metadata to convert the field data to
    widget data. It is a unary callable which takes the field data and returns
    the widget data.

    Examples
    ========

    >>> from dataclasses import dataclass, field
    >>> from dawiq import MISSING
    >>> from dawiq.delegate import convertToQt
    >>> @dataclass
    ... class Cls:
    ...     x: tuple = field(metadata=dict(toQt_converter=lambda tup: tup[0]))
    >>> convertToQt(Cls, dict(x=(10,)))
    {'x': 10}
    >>> convertToQt(Cls, dict()) == dict(x=MISSING)
    True

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
    """
    Delegate to update the model and editor with structured dictionary.

    By setting :meth:`dataclassType`, this delegate can convert the widget data
    to field data and vice versa. If :meth:`dataclassType` is :obj:`None`,
    data value from :class:`DataWidget` is directly stored to the model.

    Item data role for the model to store data value for dataclass is
    :attr:`DataRole`. By default, this is ``Qt.UserRole``.

    Even if the fields of :meth:`dataclassType` has default value, it is not
    applied to the widget and the model. This is to make sure that empty input
    by user is distinguished.

    """

    DataRole = QtCore.Qt.ItemDataRole.UserRole

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dataclass_type = None

    def dataclassType(self) -> Optional[Type[DataclassProtocol]]:
        """
        Dataclass type whose fields are used to convert the data.

        ``None`` indicates that the dataclass type is not set, and data will
        not be converted.
        """
        return self._dataclass_type

    def setDataclassType(self, dcls: Optional[Type[DataclassProtocol]]):
        self._dataclass_type = dcls

    def setModelData(self, editor, model, index):
        """
        Set the data from *editor* to the item of *model* at *index*.

        If *editor* is :class:`DataWidget` and :meth:`dataclassType` is set, its
        data is converted by :func:`convertFromQt` before being set to the model.
        """
        if isinstance(editor, DataWidget):
            dcls = self.dataclassType()
            data = editor.dataValue()
            if dcls is not None:
                data = convertFromQt(dcls, data)
            model.setData(index, data, role=self.DataRole)
        else:
            super().setModelData(editor, model, index)

    def setEditorData(self, editor, index):
        """
        Set the data from *index* to *editor*.

        If *editor* is :class:`DataWidget` and :meth:`dataclassType` is set, the
        data is converted by :func:`convertToQt` before being set to the editor.
        """
        if isinstance(editor, DataWidget):
            dcls = self.dataclassType()
            data = index.data(role=self.DataRole)
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

    Default submit policy is ``ManualSubmit``.

    Notes
    =====

    When mapping :class:`DataWidget`, *propertyName* argument of
    :meth:`addMapping` must not be passed.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSubmitPolicy(self.ManualSubmit)

    def addMapping(self, widget, section, propertyName=b""):
        super().addMapping(widget, section, propertyName)
        if isinstance(widget, DataWidget):
            widget.dataValueChanged.connect(self.submit)

    def removeMapping(self, widget):
        super().removeMapping(widget)
        if isinstance(widget, DataWidget):
            widget.dataValueChanged.disconnect(self.submit)
