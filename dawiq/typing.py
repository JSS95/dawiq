"""
Type annotations
================

:mod:`dawiq.typing` provides special type annotations.
"""

from typing import Protocol, Dict, Any
from .qt_compat import QtCore


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

    dataValueChanged: QtCore.Signal

    def dataValue(self) -> Any:
        """
        Data value that the widget represents.

        This is the API for the delegate to get the data from the widget.
        For example, in :class:`BoolCheckBox <dawiq.fieldwidgets.BoolCheckBox>`
        this method converts :class:`bool` to :obj:`Qt.CheckState` and sets the
        check state.

        If the data value is :obj:`dawiq.MISSING`, it indicates that the field is
        empty and delegate should handle it specially.

        When the data value is changed by user input, :attr:`dataValueChanged`
        signal must emit the new value.

        """
        ...

    def setDataValue(self, value: Any):
        """
        Set the data value to the widget.

        This method is the API for the delegate to set the data to the widget.
        For example, in :class:`BoolCheckBox <dawiq.fieldwidgets.BoolCheckBox>`
        this method converts the check state to :class:`bool` and returns.

        This method must specially treat :obj:`dawiq.MISSING` as empty data by
        clearing the widget. Else, type of *value* must be strictly checked and
        :obj:`TypeError` must be raised on invalid input.

        This method MUST NOT emit :attr:`dataValueChanged` signal, as doing so
        can cause infinite loop.
        """
        ...

    def fieldName(self) -> str:
        """
        Name of the field.

        It is recommended to make this name visible in the widget without
        affecting the data value. Placeholder text of the line edit or title of
        the group box are good examples.

        """
        ...

    def setFieldName(self, name: str):
        """Set the name of the field."""
        ...
