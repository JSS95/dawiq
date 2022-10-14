"""
DaWiQ - Dataclass Widget for Qt
===============================

DaWiQ is a package to build Qt widgets from dataclasses.

"""

from .version import __version__  # noqa


from .fieldwidgets import (
    BoolCheckBox,
    EmptyIntValidator,
    IntLineEdit,
    EmptyFloatValidator,
    FloatLineEdit,
    StrLineEdit,
    EnumComboBox,
    TupleGroupBox,
)
from .datawidget import (
    DataWidget,
    type2Widget,
    dataclass2Widget,
)
from .multitype import (
    DataclassStackedWidget,
    DataclassTabWidget,
)
from .delegate import (
    convertFromQt,
    convertToQt,
    highlightEmptyField,
    DataclassDelegate,
    DataclassMapper,
)


__all__ = [
    "BoolCheckBox",
    "EmptyIntValidator",
    "IntLineEdit",
    "EmptyFloatValidator",
    "FloatLineEdit",
    "StrLineEdit",
    "EnumComboBox",
    "TupleGroupBox",
    "DataWidget",
    "type2Widget",
    "dataclass2Widget",
    "DataclassStackedWidget",
    "DataclassTabWidget",
    "convertFromQt",
    "convertToQt",
    "highlightEmptyField",
    "DataclassDelegate",
    "DataclassMapper",
]
