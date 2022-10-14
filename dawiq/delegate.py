"""
Dataclass delegate
==================

"""

import dataclasses
from .qt_compat import QtCore, QtWidgets, TypeRole, DataRole
from .datawidget import DataWidget
from .multitype import DataclassStackedWidget, DataclassTabWidget
from .typing import DataclassProtocol
from typing import Type, Dict, Any, Optional


__all__ = [
    "convertFromQt",
    "convertToQt",
    "highlightEmptyField",
    "DataclassDelegate",
    "DataclassMapper",
]


def convertFromQt(
    dcls: Type[DataclassProtocol],
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convert the dict from :class:`DataWidget` to structured dict for dataclass.

    If the field value does not exist in *data* or is :obj:`None`, the field
    is not included in the resulting dictionary. Default value of the field is
    ignored.

    Field may define `fromQt_converter` metadata to convert the widget data to
    field data. It is a unary callable which takes the widget data and returns
    the field data.

    Examples
    ========

    >>> from dataclasses import dataclass, field
    >>> from dawiq.delegate import convertFromQt
    >>> from typing import Optional
    >>> def conv(arg):
    ...     return (arg,)
    >>> @dataclass
    ... class Cls:
    ...     x: int = 1
    ...     y: Optional[int] = None
    ...     z: tuple = field(default=(1,), metadata=dict(fromQt_converter=conv))
    >>> convertFromQt(Cls, dict())  # empty dict (default value is not used)
    {}
    >>> convertFromQt(Cls, dict(x=None, y=None, z=None))  # None is removed
    {}
    >>> convertFromQt(Cls, dict(z=1))  # data is converted
    {'z': (1,)}

    """
    # Return value is not dataclass but dictionary because necessary fields might
    # be missing from the widget.
    ret = {}
    for f in dataclasses.fields(dcls):
        val = data.get(f.name, None)
        t = f.type

        if val is None:
            continue

        if dataclasses.is_dataclass(t):
            val = convertFromQt(t, val)

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

    If the data does not have the value for a field, :obj:`None` is passed as
    its value instead to clear the widget.

    Field may define `toQt_converter` metadata to convert the field data to
    widget data. It is a unary callable which takes the field data and returns
    the widget data.

    Examples
    ========

    >>> from dataclasses import dataclass, field
    >>> from dawiq.delegate import convertToQt
    >>> @dataclass
    ... class Cls:
    ...     x: int = field(metadata=dict(toQt_converter=lambda tup: tup[0]))
    >>> convertToQt(Cls, dict(x=(1,)))  # data converted
    {'x': 1}
    >>> convertToQt(Cls, dict())  # None is used for placeholder
    {'x': None}
    >>> convertToQt(Cls, dict(x=None))  # None is not passed to the converter
    {'x': None}

    """
    ret = {}
    for f in dataclasses.fields(dcls):
        val = data.get(f.name, None)
        if val is None:
            pass
        elif dataclasses.is_dataclass(f.type):
            val = convertToQt(f.type, val)
        converter = f.metadata.get("toQt_converter", None)
        if val is not None and converter is not None:
            val = converter(val)
        ret[f.name] = val
    return ret


def highlightEmptyField(editor: DataWidget, dcls: Optional[Type[DataclassProtocol]]):
    """Recursively highlight the empty field whose data is required."""
    if dcls is None:
        editor.setRequired(False)
    else:
        # get field widgets from *editor*
        field_widgets = {}
        for i in range(editor.count()):
            widget = editor.widget(i)
            if widget is None:
                continue
            field_widgets[widget.fieldName()] = widget

        # if the field does not have default value, the field is required.
        for f in dataclasses.fields(dcls):
            widget = field_widgets.pop(f.name, None)
            if widget is None:  # no widget for field
                continue
            required = f.default is dataclasses.MISSING
            if isinstance(widget, DataWidget):
                if required and dataclasses.is_dataclass(f.type):
                    highlightEmptyField(widget, f.type)
                else:
                    widget.setRequired(required)
            else:
                widget.setRequired(required)


class DataclassDelegate(QtWidgets.QStyledItemDelegate):
    """Delegate to update the model and the :class:`DataWidget`."""

    TypeRole = TypeRole
    DataRole = DataRole

    def __init__(self, parent=None):
        super().__init__(parent)
        self._freeze_model = False

    def setModelDataclassData(
        self,
        index: QtCore.QModelIndex,
        dcls: Type[DataclassProtocol],
        data: Dict,
    ):
        """Set the dataclass data from the model index."""
        if dcls is not None:
            data = convertFromQt(dcls, data)
        index.model().setData(index, data, role=self.DataRole)

    def setEditorDataclassData(
        self,
        editor: DataWidget,
        dcls: Type[DataclassProtocol],
        data: Optional[Dict],
    ):
        """Set the dataclass data to the editor."""
        if data is None:
            data = {}
        if dcls is not None:
            data = convertToQt(dcls, data)
        editor.setDataValue(data)
        highlightEmptyField(editor, dcls)

    def setModelData(self, editor, model, index):
        """
        Set the data from *editor* to the item of *model* at *index*.

        If *editor* is :class:`DataWidget` and the model contains dataclass type,
        the data from the editor is converted by :func:`convertFromQt` before
        being set to the model.
        """
        if self._freeze_model:
            return

        if isinstance(editor, (DataclassStackedWidget, DataclassTabWidget)):
            dcls = editor.currentDataclass()
            if dcls != model.data(index, role=self.TypeRole):
                index.model().setData(index, dcls, role=self.TypeRole)
            self.setModelData(editor.currentWidget(), model, index)

        elif isinstance(editor, DataWidget):
            dcls = model.data(index, role=self.TypeRole)
            data = editor.dataValue()
            self.setModelDataclassData(index, dcls, data)

        super().setModelData(editor, model, index)

    def setEditorData(self, editor, index):
        """
        Set the data from *index* to *editor*.

        If *editor* is :class:`DataWidget` and the model contains dataclass type,
        the data from the editor is converted by :func:`convertToQt` before
        being set to the editor.
        """
        if isinstance(editor, (DataclassStackedWidget, DataclassTabWidget)):
            dcls = index.data(role=self.TypeRole)
            if dcls is not None:
                widgetIndex = editor.indexOfDataclass(dcls)
            else:
                widgetIndex = -1
            self._freeze_model = True
            editor.setCurrentIndex(widgetIndex)
            self._freeze_model = False
            self.setEditorData(editor.currentWidget(), index)

        elif isinstance(editor, DataWidget):
            dcls = index.data(role=self.TypeRole)
            data = index.data(role=self.DataRole)
            self.setEditorDataclassData(editor, dcls, data)

        super().setEditorData(editor, index)


class DataclassMapper(QtWidgets.QDataWidgetMapper):
    """
    Mapper between the :class:`DataWidget` and the model.

    Default submit policy is ``SubmitPolicy.ManualSubmit``.

    Notes
    =====

    When mapping :class:`DataWidget`, *propertyName* argument of
    :meth:`addMapping` must not be passed.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSubmitPolicy(self.SubmitPolicy.ManualSubmit)

    def addMapping(self, widget, section, propertyName=b""):
        if isinstance(widget, (DataclassStackedWidget, DataclassTabWidget)):
            widget.currentChanged.connect(self.submit)
            widget.currentDataValueChanged.connect(self.submit)
        elif isinstance(widget, DataWidget):
            widget.dataValueChanged.connect(self.submit)
        super().addMapping(widget, section, propertyName)

    def removeMapping(self, widget):
        if isinstance(widget, (DataclassStackedWidget, DataclassTabWidget)):
            widget.currentChanged.disconnect(self.submit)
            widget.currentDataValueChanged.disconnect(self.submit)
        elif isinstance(widget, DataWidget):
            widget.dataValueChanged.disconnect(self.submit)
        super().removeMapping(widget)
