"""
Type annotations
================

:mod:`dawiq.typing` provides special type annotations.
"""

from typing import Protocol, Dict, Any


__all__ = [
    "DataclassProtocol",
    "FieldWidgetProtocol",
]


class DataclassProtocol(Protocol):
    """Type annotation for dataclass type object."""

    # https://stackoverflow.com/a/55240861/11501976
    __dataclass_fields__: Dict


class FieldWidgetProtocol(Protocol):
    """Type annotation for data widget object."""

    def dataValue(self) -> Any:
        ...

    def setDataValue(self, value: Any):
        ...

    def fieldName(self) -> str:
        ...

    def setFieldName(self, name: str):
        ...
