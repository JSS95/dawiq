============
Introduction
============

.. currentmodule:: dawiq

DaWiQ is a Python package for generating Qt widget from dataclass.
Widget data can be stored in Qt's item model as dictionary, which can be easily constructed to dataclass instance.
Item delegate and widget mapper are provided for this purpose.

Widgets for basic types such as :class:`int`, :class:`bool`, :class:`enum.Enum` are provided.
You may represent the custom object with basic types and construct pre-defined widgets from them.
This can be done by passing the converters to the metadata of dataclass fields.

Supported Qt bindings
=====================

DaWiQ is compatible with the following Qt binding packages:

* `PySide6 <https://pypi.org/project/PySide6/>`_
* `PyQt6 <https://pypi.org/project/PyQt6/>`_
* `PySide2 <https://pypi.org/project/PySide2/>`_
* `PyQt5 <https://pypi.org/project/PyQt5/>`_

Available package is searched and selected in the order mentioned above.
To force a particular API, set environment variable ``DAWIQ_QT_API`` with package name. Letter case does not matter.
