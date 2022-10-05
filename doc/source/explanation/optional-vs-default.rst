================================
Optional field and default value
================================

For a dataclass field, two important questions arise:

1. It is ``Optional``?
2. Does it have a default value?

If the field type is ``Optional``, :obj:`None` is allowed for placeholder object in addition to the main type.
And if there is default value, the field is not mandatory i.e. its data does not need to be passed. In such case the default value is used.

>>> from dataclasses import dataclass
>>> from typing import Optional
>>> @dataclass
... class DataClass:
...     a: int
...     b: Optional[int]
...     c: int = 0
...     d: Optional[int] = None
>>> DataClass(1)
Traceback (most recent call last):
...
TypeError: __init__() missing 1 required positional argument: 'b'
>>> DataClass(1, None)
DataClass(a=1, b=None, c=0, d=None)

Here, ``DataClass.b`` can take :obj:`None` but it is mandatory. On the other hand, ``DataClass.c`` is not mandatory but it should not be :obj:`None`.

.. note::
    In fact, Python does not perform type check and allows you to pass :obj:`None` to ``DataClass.c``.
    However this shouldn't be performed for robust typing.

How will the data widget from ``DataClass`` be?

.. tabs::

    .. code-tab:: python
        :caption: PySide6

        from PySide6.QtGui import QStandardItemModel, QStandardItem
        from PySide6.QtWidgets import QApplication
        from dawiq import DataclassDelegate, DataclassMapper, dataclass2Widget
        import sys

        model = QStandardItemModel()
        item = QStandardItem()
        item.setData(DataClass, role=DataclassDelegate.TypeRole)
        model.appendRow(item)

        delegate = DataclassDelegate()
        mapper = DataclassMapper()
        mapper.setItemDelegate(delegate)
        mapper.setModel(model)

        app = QApplication(sys.argv)
        app.setStyleSheet("*[requiresFieldData=true]{border: 1px solid red}")

        widget = dataclass2Widget(DataClass)
        mapper.addMapping(widget, 0)
        mapper.setCurrentIndex(0)

        widget.show()
        app.exec()
        app.quit()

    .. code-tab:: python
        :caption: PyQt6

        from PyQt6.QtGui import QStandardItemModel, QStandardItem
        from PyQt6.QtWidgets import QApplication
        from dawiq import DataclassDelegate, DataclassMapper, dataclass2Widget
        import sys

        model = QStandardItemModel()
        item = QStandardItem()
        item.setData(DataClass, role=DataclassDelegate.TypeRole)
        model.appendRow(item)

        delegate = DataclassDelegate()
        mapper = DataclassMapper()
        mapper.setItemDelegate(delegate)
        mapper.setModel(model)

        app = QApplication(sys.argv)
        app.setStyleSheet("*[requiresFieldData=true]{border: 1px solid red}")

        widget = dataclass2Widget(DataClass)
        mapper.addMapping(widget, 0)
        mapper.setCurrentIndex(0)

        widget.show()
        app.exec()
        app.quit()

    .. code-tab:: python
        :caption: PySide2

        from PySide2.QtGui import QStandardItemModel, QStandardItem
        from PySide2.QtWidgets import QApplication
        from dawiq import DataclassDelegate, DataclassMapper, dataclass2Widget
        import sys

        model = QStandardItemModel()
        item = QStandardItem()
        item.setData(DataClass, role=DataclassDelegate.TypeRole)
        model.appendRow(item)

        delegate = DataclassDelegate()
        mapper = DataclassMapper()
        mapper.setItemDelegate(delegate)
        mapper.setModel(model)

        app = QApplication(sys.argv)
        app.setStyleSheet("*[requiresFieldData=true]{border: 1px solid red}")

        widget = dataclass2Widget(DataClass)
        mapper.addMapping(widget, 0)
        mapper.setCurrentIndex(0)

        widget.show()
        app.exec_()
        app.quit()

    .. code-tab:: python
        :caption: PyQt5

        from PyQt5.QtGui import QStandardItemModel, QStandardItem
        from PyQt5.QtWidgets import QApplication
        from dawiq import DataclassDelegate, DataclassMapper, dataclass2Widget
        import sys

        model = QStandardItemModel()
        item = QStandardItem()
        item.setData(DataClass, role=DataclassDelegate.TypeRole)
        model.appendRow(item)

        delegate = DataclassDelegate()
        mapper = DataclassMapper()
        mapper.setItemDelegate(delegate)
        mapper.setModel(model)

        app = QApplication(sys.argv)
        app.setStyleSheet("*[requiresFieldData=true]{border: 1px solid red}")

        widget = dataclass2Widget(DataClass)
        mapper.addMapping(widget, 0)
        mapper.setCurrentIndex(0)

        widget.show()
        app.exec()
        app.quit()


.. figure:: ../_images/optionalfield-example.jpg
   :align: center

   Widget from ``DataClass``

We can see that the default values have nothing to do with the widget value and thus the editors are all empty.
However if a field does not have a default value, the delegate marks the widget to indicate that it should not be empty and the style sheet highlights it.

What about the widget data and the model data?

>>> widget.dataValue()  # doctest: +SKIP
{'a': None, 'b': None, 'c': None, 'd': None}
>>> item.data(role=DataclassDelegate.DataRole)  # doctest: +SKIP
{}

Data values of all widgets are :obj:`None`, as :obj:`None` is designed to be.
When setting the widget data to the model data, the delegate ignores the field with :obj:`None`.
Therefore the model data is an empty dictionary.

Now let's change the widget data to update the model data.

>>> widget.setDataValue(dict(a=3, b=4, d=5))  # doctest: +SKIP
>>> mapper.submit()  # doctest: +SKIP
>>> widget.dataValue()  # doctest: +SKIP
{'a': 3, 'b': 4, 'c': None, 'd': 6}
>>> item.data(role=DataclassDelegate.DataRole)  # doctest: +SKIP
{'a': 3, 'b': 4, 'd': 5}

Valid data (not None) in the field widget is updated to the model as well.
At this time it is easy to construct the dataclass instance from the model data.

>>> args = item.data(role=DataclassDelegate.DataRole)  # doctest: +SKIP
>>> DataClass(**args)  # doctest: +SKIP
DataClass(a=3, b=4, c=0, d=None)

We can see that ``DataClass.c`` does not exist in the model data so the dataclass constructor used the default value instead.

Now if we want to set ``None`` to ``DataClass.d``, we can just delete the field widget data.
Then the field data in the model will be deleted and dataclass constructor will use the default value, which is ``None``.

>>> widget.setDataValue(dict(a=3, b=4))  # doctest: +SKIP
>>> mapper.submit()  # doctest: +SKIP
>>> args = item.data(role=DataclassDelegate.DataRole)  # doctest: +SKIP
>>> DataClass(**args)  # doctest: +SKIP
DataClass(a=3, b=4, c=0, d=None)

But how can we set ``None`` to ``DataClass.b``?

>>> widget.setDataValue(dict(a=3))  # doctest: +SKIP
>>> mapper.submit()  # doctest: +SKIP
>>> widget.dataValue()  # doctest: +SKIP
{'a': 3, 'b': None, 'c': None, 'd': None}
>>> args = item.data(role=DataclassDelegate.DataRole)  # doctest: +SKIP
>>> args
{'a': 3}
>>> DataClass(**args)  # doctest: +SKIP
Traceback (most recent call last):
...
TypeError: __init__() missing 1 required positional argument: 'b'

Sadly, we can't. ``None`` is reserved to indicate the empty value and it cannot be a valid value.
