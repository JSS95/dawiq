"""
Dataclass delegate
==================

"""

import dataclasses
from .qt_compat import QtWidgets, TypeRole, DataRole
from .fieldwidgets import MISSING
from .datawidget import DataWidget
from .multitype import DataclassStackedWidget, DataclassTabWidget
from .typing import DataclassProtocol
from typing import Type, Dict, Any, Union, Optional


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

    If the field value does not exist in *data* or is :obj:`MISSING`, the field
    type is checked. If the field type is ``Optional``, then :obj:`None` is used
    as the value. Else, the field is not included in the resulting dictionary.
    Default value of the field is ignored.

    Field may define `fromQt_converter` metadata to convert the widget data to
    field data. It is a unary callable which takes the widget data and returns
    the field data.

    Examples
    ========

    >>> from dataclasses import dataclass, field
    >>> from dawiq import MISSING
    >>> from dawiq.delegate import convertFromQt
    >>> from typing import Optional
    >>> def conv(arg):
    ...     return (arg,)
    >>> @dataclass
    ... class Cls:
    ...     x: int
    ...     y: Optional[int]
    ...     z: tuple = field(metadata=dict(fromQt_converter=conv), default=(1,))
    >>> convertFromQt(Cls, dict(z=10))
    {'y': None, 'z': (10,)}
    >>> convertFromQt(Cls, dict(x=MISSING, y=MISSING))
    {'y': None}

    """
    # Return value is not dataclass but dictionary because necessary fields might
    # be missing from the widget.
    ret = {}
    for f in dataclasses.fields(dcls):
        val = data.get(f.name, MISSING)
        t = f.type

        if val is MISSING:
            origin = getattr(t, "__origin__", None)
            args = [a for a in getattr(t, "__args__", ()) if not isinstance(None, a)]
            if origin is Union and len(args) == 1:
                # f.type is Optional[...]
                val = None
            else:
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

    If the data does not have the value for a field, :obj:`MISSING` is passed as
    its value instead to clear the widget.

    Field may define `toQt_converter` metadata to convert the field data to
    widget data. It is a unary callable which takes the field data and returns
    the widget data.

    Examples
    ========

    >>> from dataclasses import dataclass, field
    >>> from dawiq import MISSING
    >>> from dawiq.delegate import convertToQt
    >>> from typing import Optional
    >>> @dataclass
    ... class Cls:
    ...     x: int
    ...     y: Optional[int]
    ...     z: tuple = field(metadata=dict(toQt_converter=lambda tup: tup[0]))
    >>> convertToQt(Cls, dict(x=1, y=2, z=(10,)))
    {'x': 1, 'y': 2, 'z': 10}
    >>> convertToQt(Cls, dict()) == dict(x=MISSING, y=MISSING, z=MISSING)
    True
    >>> convertToQt(Cls, dict(y=None)) ==  dict(x=MISSING, y=None, z=MISSING)
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
    """
    Delegate to update the model and the :class:`DataWidget`.

    :attr:`TypeRole` and :attr:`DataRole` are ``Qt.ItemDataRole`` for the model
    to store the dataclass type and the dataclass data. Dataclass instance can be
    constructed by these values.

    Default values of the dataclass fields are not applied to the widget and to
    the model. This is to make sure that empty input by user is distinguished.

    """

    TypeRole = TypeRole
    DataRole = DataRole

    def __init__(self, parent=None):
        super().__init__(parent)
        self._freeze_model = False

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
                model.setData(index, dcls, role=self.TypeRole)
            self.setModelData(editor.currentWidget(), model, index)
        elif isinstance(editor, DataWidget):
            dcls = model.data(index, role=self.TypeRole)
            data = editor.dataValue()
            if dcls is not None:
                data = convertFromQt(dcls, data)
            model.setData(index, data, role=self.DataRole)
        else:
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
            if data is None:
                data = {}
            if dcls is not None:
                data = convertToQt(dcls, data)
            editor.setDataValue(data)
            highlightEmptyField(editor, dcls)

        else:
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
