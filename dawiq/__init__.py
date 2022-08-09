"""
DaWiQ - Dataclass Widget for Qt
===============================

DaWiQ is a package to build Qt widgets from dataclasses.

"""

from .version import __version__  # noqa


from .fieldwidgets import (
    type2Widget,
    BoolCheckBox,
)


__all__ = [
    "type2Widget",
    "BoolCheckBox",
]
