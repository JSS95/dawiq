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
)


__all__ = [
    "type2Widget",
    "BoolCheckBox",
    "MISSING",
    "EmptyIntValidator",
    "IntLineEdit",
    "DataWidget",
]
