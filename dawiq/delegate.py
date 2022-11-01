"""
Dataclass delegate
==================

"""

import dataclasses
from .qt_compat import QtWidgets, TypeRole, DataRole
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
    ignoreMissing=True,
) -> Dict[str, Any]:
    """
    Convert the dict from :class:`DataWidget` to structured dict for dataclass.

    If the field value does not exist in *data* or is :obj:`None`, it is
    considered to be absent. If *ignoreMissing* is True, the absent value is not
    included in the resulting dictionary. Else, the default value of the field is
    used if there is any.

    Field may define ``fromQt_converter`` metadata to convert the widget data to
    field data. It is a unary callable which takes the widget data and returns
    the field data.

    Examples
    ========

    ``None`` is considered as missing value.

    >>> from dataclasses import dataclass, field
    >>> from dawiq.delegate import convertFromQt
    >>> from typing import Optional
    >>> @dataclass
    ... class Cls1:
    ...     a: int
    ...     b: int = 10
    ...     c: Optional[int] = None
    ...     d: list = field(default_factory=list)
    >>> convertFromQt(Cls1, {})
    {}
    >>> convertFromQt(Cls1, dict(a=1, b=None, c=None))
    {'a': 1}

    *ignoreMissing* controls whether the default value should be used.

    >>> convertFromQt(Cls1, {}, ignoreMissing=False)
    {'b': 10, 'c': None, 'd': []}

    Nested dataclasses are recusively converted.

    >>> @dataclass
    ... class Cls2:
    ...     x: int = 20
    ...     y: Cls1 = field(default_factory=lambda: Cls1(a=5))
    >>> convertFromQt(Cls2, {}, ignoreMissing=False)
    {'x': 20, 'y': {'a': 5, 'b': 10, 'c': None, 'd': []}}

    ``fromQt_converter`` metadata converts the data from the widet.

    >>> def conv(arg):
    ...     return (arg,)
    >>> @dataclass
    ... class Cls3:
    ...     x: tuple = field(default=(1,), metadata=dict(fromQt_converter=conv))
    >>> convertFromQt(Cls3, dict(x=1))
    {'x': (1,)}

    """
    # Return value is not dataclass but dictionary because necessary fields might
    # be missing from the widget.
    ret: Dict[str, Any] = {}
    for f in dataclasses.fields(dcls):
        val = data.get(f.name, None)
        t = f.type

        if val is None:
            if ignoreMissing:
                continue
            val = (
                f.default_factory()
                if f.default_factory is not dataclasses.MISSING
                else f.default
            )
            if val is dataclasses.MISSING:
                if dataclasses.is_dataclass(t):
                    val = convertFromQt(t, {}, ignoreMissing)
                else:
                    continue
            if dataclasses.is_dataclass(val) and not isinstance(val, type):
                val = dataclasses.asdict(val)

        else:
            if dataclasses.is_dataclass(t):
                val = convertFromQt(t, val, ignoreMissing)
            converter = f.metadata.get("fromQt_converter", None)
            if converter is not None:
                val = converter(val)
        ret[f.name] = val
    return ret


def convertToQt(
    dcls: Type[DataclassProtocol],
    data: Dict[str, Any],
    ignoreMissing=True,
) -> Dict[str, Any]:
    """
    Convert structured dict from dataclass to dict for :class:`DataWidget`.

    If the field value does not exist in *data* or is :obj:`None`, it is
    considered to be absent. If *ignoreMissing* is True, ``None`` is used as the
    placeholder in the resulting dictionary. Else, the default value of the field
    is used if there is any.

    Field may define ``toQt_converter`` metadata to convert the field data to
    widget data. It is a unary callable which takes the field data and returns
    the widget data.

    Examples
    ========

    ``None`` is considered as missing value.

    >>> from dataclasses import dataclass, field
    >>> from dawiq.delegate import convertToQt
    >>> from typing import Optional
    >>> @dataclass
    ... class Cls1:
    ...     a: int
    ...     b: int = 10
    ...     c: Optional[int] = None
    ...     d: list = field(default_factory=list)
    >>> convertToQt(Cls1, dict(a=1, b=2, c=3))
    {'a': 1, 'b': 2, 'c': 3, 'd': None}
    >>> convertToQt(Cls1, {})
    {'a': None, 'b': None, 'c': None, 'd': None}

    *ignoreMissing* controls whether the default value should be used.

    >>> convertToQt(Cls1, {}, ignoreMissing=False)
    {'a': None, 'b': 10, 'c': None, 'd': []}

    Nested dataclasses are recusively converted.

    >>> @dataclass
    ... class Cls2:
    ...     x: int = 20
    ...     y: Cls1 = field(default_factory=lambda: Cls1(a=5))
    >>> convertToQt(Cls2, {}, ignoreMissing=False)
    {'x': 20, 'y': {'a': 5, 'b': 10, 'c': None, 'd': []}}

    ``toQt_converter`` metadata converts the data to the widget.

    >>> @dataclass
    ... class Cls3:
    ...     x: int = field(metadata=dict(toQt_converter=lambda tup: tup[0]))
    >>> convertToQt(Cls3, dict(x=(1,)))
    {'x': 1}

    """
    ret: Dict[str, Any] = {}
    for f in dataclasses.fields(dcls):
        val = data.get(f.name, None)
        t = f.type

        if val is None:
            if ignoreMissing:
                ret[f.name] = None
                continue
            val = (
                f.default_factory()
                if f.default_factory is not dataclasses.MISSING
                else f.default
            )
            if val is dataclasses.MISSING:
                if dataclasses.is_dataclass(t):
                    val = convertToQt(t, {}, ignoreMissing)
                else:
                    ret[f.name] = None
                    continue
            if dataclasses.is_dataclass(val) and not isinstance(val, type):
                val = dataclasses.asdict(val)

        else:
            if dataclasses.is_dataclass(t):
                val = convertToQt(t, val, ignoreMissing)
            converter = f.metadata.get("toQt_converter", None)
            if converter is not None:
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
            default = (
                f.default_factory()
                if f.default_factory is not dataclasses.MISSING
                else f.default
            )
            required = default is dataclasses.MISSING
            if isinstance(widget, DataWidget):
                if required and dataclasses.is_dataclass(f.type):
                    highlightEmptyField(widget, f.type)
                else:
                    widget.setRequired(required)
            else:
                widget.setRequired(required)


class DataclassDelegate(QtWidgets.QStyledItemDelegate):
    """
    Delegate to update the model and the data widget.

    This delegate stores dataclass type and dataclass data to the model, and
    updates the data widget with model data.

    Supported data widgets are:

    * :class:`DataWidget`
    * :class:`DataclassStackedWidget`
    * :class:`DataclassTabWidget`

    Dataclass type is stored to the model with :attr:`TypeRole` as item data role
    and dataclass data is stored with :attr:`DataRole`.

    By default, missing values are not replaced by default values of the fields.
    This is to preserve the intentional empty input by the user. Setting
    :meth:`ignoreMissing` changes this behavior.
    """

    TypeRole = TypeRole
    DataRole = DataRole

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ignoreMissing = True

    def ignoreMissing(self) -> bool:
        """If True, default values are used for missing fields."""
        return self._ignoreMissing

    def setIgnoreMissing(self, val: bool):
        self._ignoreMissing = val

    def setModelData(self, editor, model, index):
        if isinstance(editor, (DataclassStackedWidget, DataclassTabWidget)):
            dcls = editor.currentDataclass()
            model.setData(index, dcls, role=self.TypeRole)
            self.setModelData(editor.currentWidget(), model, index)

        elif isinstance(editor, DataWidget):
            dcls = model.data(index, role=self.TypeRole)
            data = editor.dataValue()
            if dcls is not None:
                data = convertFromQt(dcls, data, self.ignoreMissing())
            model.setData(index, data, role=self.DataRole)

        super().setModelData(editor, model, index)

    def setEditorData(self, editor, index):
        if isinstance(editor, (DataclassStackedWidget, DataclassTabWidget)):
            dcls = index.data(role=self.TypeRole)
            if dcls is not None:
                widgetIndex = editor.indexOfDataclass(dcls)
            else:
                widgetIndex = -1
            editor.setCurrentIndex(widgetIndex)
            self.setEditorData(editor.currentWidget(), index)

        elif isinstance(editor, DataWidget):
            dcls = index.data(role=self.TypeRole)
            data = index.data(role=self.DataRole)
            if data is None:
                data = {}
            if dcls is not None:
                data = convertToQt(dcls, data, self.ignoreMissing())
            editor.setDataValue(data)
            highlightEmptyField(editor, dcls)

        super().setEditorData(editor, index)


class DataclassMapper(QtWidgets.QDataWidgetMapper):
    """
    Mapper between the data widget and the model.

    Supported data widgets are:

    * :class:`DataWidget`
    * :class:`DataclassStackedWidget`
    * :class:`DataclassTabWidget`

    Notes
    =====

    When mapping :class:`DataWidget`, *propertyName* argument of
    :meth:`addMapping` must not be passed.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSubmitPolicy(self.SubmitPolicy.ManualSubmit)

    def addMapping(self, widget, section, propertyName=b""):
        if isinstance(widget, DataclassStackedWidget):
            widget.currentDataEdited.connect(self.submit)
        elif isinstance(widget, DataclassTabWidget):
            widget.activated.connect(self.submit)
            widget.currentDataEdited.connect(self.submit)
        elif isinstance(widget, DataWidget):
            widget.dataEdited.connect(self.submit)
        super().addMapping(widget, section, propertyName)

    def removeMapping(self, widget):
        if isinstance(widget, DataclassStackedWidget):
            widget.currentDataEdited.disconnect(self.submit)
        elif isinstance(widget, DataclassTabWidget):
            widget.activated.disconnect(self.submit)
            widget.currentDataEdited.disconnect(self.submit)
        elif isinstance(widget, DataWidget):
            widget.dataEdited.disconnect(self.submit)
        super().removeMapping(widget)
