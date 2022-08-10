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
    """Type annotation for field widget object."""

    def fieldName(self) -> str:
        """
        Name of the field.

        It is recommended to make this name visible in the widget without
        affecting the data value. Placeholder text of the line edit or title of
        the group box are good examples.

        :attr:`setFieldName` changes the field name.
        """
        ...

    def setFieldName(self, name: str):
        ...

    def dataValue(self) -> Any:
        ...

    def setDataValue(self, value: Any):
        ...
