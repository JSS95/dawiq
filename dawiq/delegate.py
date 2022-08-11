"""
Dataclass delegate
==================
"""

from .qt_compat import QtWidgets


__all__ = [
    "DataclassDelegate",
]


class DataclassDelegate(QtWidgets.QAbstractItemDelegate):
    ...
