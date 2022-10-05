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
        this method converts the current check state to :class:`bool` and
        returns.

        If the data value is :obj:`None`, it typically indicates that the widget
        is empty and the delegate should specially handle it. One of the few
        exceptions is :class:`BoolCheckBox <dawiq.fieldwidgets.BoolCheckBox>`
        where :obj:`None` indicates partially checked state.

        When the data value is changed by user input, :attr:`dataValueChanged`
        signal must emit the new value.

        """
        ...

    def setDataValue(self, value: Any):
        """
        Set the data value to the widget.

        This method is the API for the delegate to set the data to the widget.
        For example, in :class:`BoolCheckBox <dawiq.fieldwidgets.BoolCheckBox>`
        this method converts :class:`bool` to :obj:`Qt.CheckState` and sets to
        the widget.

        If the data value is :obj:`None`, it typically means that the value is
        null and the widget should be cleared. One of the few exceptions is
        :class:`BoolCheckBox <dawiq.fieldwidgets.BoolCheckBox>` where :obj:`None`
        indicates fuzzy boolean value.

        For valid *value*, its type must be strictly checked and :obj:`TypeError`
        must be raised on invalid input.

        This method MUST NOT emit :attr:`dataValueChanged` signal, as doing so
        can cause infinite loop in nested widgets.
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

    def setRequired(self, required: bool):
        """
        Set if *self* represents a required field.

        If *required* is True, it indicates that the field is mandatory. On such
        case, this methods checks the :meth:`dataValue` of *self* and sets
        ``requiresFieldData`` property of the editor widget. If the data value of
        required field is missing, the property is set to be True.

        .. code-block:: python

            widget.setProperty("requiresFieldData", True)
            widget.style().unpolish(widget)
            widget.style().polish(widget)

        The editor widget is usually *self*, but there are exceptions such as
        :class:`TupleGroupBox`. Note that the widget needs to be re-polished.

        Style sheet can be set to highlight the required field with empty widget.
        Common way is to set the style sheet of :class:`QApplication` before
        starting the app.

        .. code-block:: python

            qApp.setStyleSheet(
                "*[requiresFieldData=true]{border: 1px solid red}"
            )

        Notes
        =====

        This method is designed to be called by the :class:`DataclassDelegate`,
        not directly by the user.

        """
        ...
