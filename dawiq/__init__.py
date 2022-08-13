"""
DaWiQ - Dataclass Widget for Qt
===============================

DaWiQ is a package to build Qt widgets from dataclasses.

"""

from .version import __version__  # noqa


from .fieldwidgets import (
    MISSING,
    BoolCheckBox,
    EmptyIntValidator,
    IntLineEdit,
    EmptyFloatValidator,
)
from .datawidget import (
    DataWidget,
    type2Widget,
    dataclass2Widget,
)
from .delegate import (
    DataclassDelegate,
    DataclassMapper,
)


__all__ = [
    "BoolCheckBox",
    "MISSING",
    "EmptyIntValidator",
    "IntLineEdit",
    "EmptyFloatValidator",
    "DataWidget",
    "type2Widget",
    "dataclass2Widget",
    "DataclassDelegate",
    "DataclassMapper",
]
