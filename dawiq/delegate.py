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
    Convert the data from :class:`DataWidget` to structured data for dataclass.

    If the field value is :obj:`MISSING`, it is not included in the resulting
    dictionary.

    If the field has `fromQt_converter` metadata which is a unary callable,
    widget data is converted by it. This allows complicated type to be
    represented by simple widget.

    Notes
    =====

    Return value is not dataclass but dictionary because necessary fields might
    be missing from the widget.
    """
    ret = {}
    for f in dataclasses.fields(dcls):
        val = data[f.name]
        if val is MISSING:
            continue
        elif dataclasses.is_dataclass(f.type):
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
    Convert the dictionary from dataclass to the data for :class:`DataWidget`.

    If the field does not exist in the data, :obj:`MISSING` is passed as its
    value instead.

    If the field has `toQt_converter` metadata which is a unary callable,
    dataclass data is converted by it. This allows complicated type to be
    represented by simple widget.

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


class DataclassDelegate(QtWidgets.QAbstractItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._dataclass_type = None

    def dataclassType(self) -> Optional[Type[DataclassProtocol]]:
        return self._dataclass_type

    def setDataclassType(self, dcls: Optional[Type[DataclassProtocol]]):
        self._dataclass_type = dcls

    def setModelData(
        self,
        editor: DataWidget,
        model: QtCore.QAbstractItemModel,
        index: QtCore.QModelIndex,
    ):
        dcls = self.dataclassType()
        data = editor.dataValue()
        if dcls is not None:
            data = convertFromQt(dcls, data)
        model.setData(index, data)

    def setEditorData(self, editor: DataWidget, index: QtCore.QModelIndex):
        dcls = self.dataclassType()
        data = index.data()
        if data is None:
            data = {}
        if dcls is not None:
            data = convertToQt(dcls, data)
        editor.setDataValue(data)


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
