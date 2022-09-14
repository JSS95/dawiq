=============================
How to implement field widget
=============================

You can define your custom field widget instead of default widgets provided by :mod:`dawiq`.

Field widget must have the structure of :class:`FieldWidgetProtocol <.typing.FieldWidgetProtocol>`.
Once you defined your field widget, define a function which replaces :func:`type2Widget` and pass it to :func:`dataclass2Widget` when constructing the data widget.
