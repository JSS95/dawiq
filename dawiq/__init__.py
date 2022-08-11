"""
DaWiQ - Dataclass Widget for Qt
===============================

DaWiQ is a package to build Qt widgets from dataclasses.

"""

from .version import __version__  # noqa


from .fieldwidgets import (
    BoolCheckBox,
    MISSING,
    EmptyIntValidator,
    IntLineEdit,
)
from .datawidget import (
    DataWidget,
    type2Widget,
    dataclass2Widget,
)
from .delegate import (
    DataclassDelegate,
)


__all__ = [
    "BoolCheckBox",
    "MISSING",
    "EmptyIntValidator",
    "IntLineEdit",
    "DataWidget",
    "type2Widget",
    "dataclass2Widget",
    "DataclassDelegate",
]
