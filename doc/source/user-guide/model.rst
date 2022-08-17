.. _data-model:

==================
Mapping with model
==================

.. currentmodule:: dawiq

Delegate and mapper
===================

:class:`.DataclassDelegate` and :class:`.DataclassMapper` maps the widget constructed by :func:`.dataclass2Widget` with the model.

First, let's define a dataclass, a delegate and a mapper.

.. code-block:: python

    from dataclasses import dataclass
    from dawiq import DataclassDelegate, DataclassMapper

    @dataclass
    class DataClass:
        x: int
        y: bool

    delegate = DataclassDelegate()
    delegate.setDataclassType(DataClass)
    mapper = DataclassMapper()
    mapper.setItemDelegate(delegate)

Then we construct a model with two rows and set it to the mapper.

.. tabs::

    .. code-tab:: python
        :caption: PySide6

        from PySide6.QtGui import QStandardItemModel, QStandardItem

        model = QStandardItemModel()
        for i in range(2):
            model.appendRow(QStandardItem())
        mapper.setModel(model)

    .. code-tab:: python
        :caption: PyQt6

        from PyQt6.QtGui import QStandardItemModel, QStandardItem

        model = QStandardItemModel()
        for i in range(2):
            model.appendRow(QStandardItem())
        mapper.setModel(model)

    .. code-tab:: python
        :caption: PySide2

        from PySide2.QtGui import QStandardItemModel, QStandardItem

        model = QStandardItemModel()
        for i in range(2):
            model.appendRow(QStandardItem())
        mapper.setModel(model)

    .. code-tab:: python
        :caption: PyQt5

        from PyQt5.QtGui import QStandardItemModel, QStandardItem

        model = QStandardItemModel()
        for i in range(2):
            model.appendRow(QStandardItem())
        mapper.setModel(model)

Now, we create a widget with data widget from ``DataClass`` and buttons to change the model index.

.. tabs::

    .. code-tab:: python
        :caption: PySide6

        from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
        from dawiq import dataclass2Widget
        import sys

        app = QApplication(sys.argv)

        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        dataWidget = dataclass2Widget(DataClass)
        widget.layout().addWidget(dataWidget)
        btn1 = QPushButton("Previous")
        widget.layout().addWidget(btn1)
        btn2 = QPushButton("Next")
        widget.layout().addWidget(btn2)

        btn1.clicked.connect(mapper.toPrevious)
        btn2.clicked.connect(mapper.toNext)

        mapper.addMapping(dataWidget, 0)
        mapper.setCurrentIndex(0)

        widget.show()
        app.exec()
        app.quit()

    .. code-tab:: python
        :caption: PyQt6

        from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
        from dawiq import dataclass2Widget
        import sys

        app = QApplication(sys.argv)

        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        dataWidget = dataclass2Widget(DataClass)
        widget.layout().addWidget(dataWidget)
        btn1 = QPushButton("Previous")
        widget.layout().addWidget(btn1)
        btn2 = QPushButton("Next")
        widget.layout().addWidget(btn2)

        btn1.clicked.connect(mapper.toPrevious)
        btn2.clicked.connect(mapper.toNext)

        mapper.addMapping(dataWidget, 0)
        mapper.setCurrentIndex(0)

        widget.show()
        app.exec()
        app.quit()

    .. code-tab:: python
        :caption: PySide2

        from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
        from dawiq import dataclass2Widget
        import sys

        app = QApplication(sys.argv)

        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        dataWidget = dataclass2Widget(DataClass)
        widget.layout().addWidget(dataWidget)
        btn1 = QPushButton("Previous")
        widget.layout().addWidget(btn1)
        btn2 = QPushButton("Next")
        widget.layout().addWidget(btn2)

        btn1.clicked.connect(mapper.toPrevious)
        btn2.clicked.connect(mapper.toNext)

        mapper.addMapping(dataWidget, 0)
        mapper.setCurrentIndex(0)

        widget.show()
        app.exec_()
        app.quit()

    .. code-tab:: python
        :caption: PyQt5

        from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
        from dawiq import dataclass2Widget
        import sys

        app = QApplication(sys.argv)

        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        dataWidget = dataclass2Widget(DataClass)
        widget.layout().addWidget(dataWidget)
        btn1 = QPushButton("Previous")
        widget.layout().addWidget(btn1)
        btn2 = QPushButton("Next")
        widget.layout().addWidget(btn2)

        btn1.clicked.connect(mapper.toPrevious)
        btn2.clicked.connect(mapper.toNext)

        mapper.addMapping(dataWidget, 0)
        mapper.setCurrentIndex(0)

        widget.show()
        app.exec()
        app.quit()


Now, the widget and the model are synchronized. Try change the index and the editor data.

.. figure:: ../_images/model-example.jpg
   :align: center

   Widget with model

Data converter
==============

As explained in :ref:`Specifying type hint <type-hint>`, field type can be different from widget data.
The converter between them can be defined by setting two metadata to the field:

* ``toQt_converter``: converts field data to widget data
* ``fromQt_converter``: converts widget data to field data

Value of these metadata must be a unary callable. Here is a simple example:

.. code-block:: python

    from dataclasses import dataclass, field
    from typing import Tuple
    from dawiq import DataclassDelegate, DataclassMapper

    class CustomClass:
        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y

    @dataclass
    class DataClass:
        custom: CustomClass = field(metadata=dict(
            default=CustomClass(1, 2),
            Qt_typehint=Tuple[int, int],
            toQt_converter=lambda obj: (obj.x, obj.y),
            fromQt_converter=lambda args: CustomClass(*args),
        ))

    delegate = DataclassDelegate()
    delegate.setDataclassType(DataClass)
    mapper = DataclassMapper()
    mapper.setItemDelegate(delegate)

Constructing model and widget is same as the first section of this document. Here is the result:

.. figure:: ../_images/model-converter-example.jpg
   :align: center

   Widget with model compatible to custom type

Note that the dataclass defines default value, but the widget is still empty.
Default value is not updated to model and to empty widget, in order to distinguish the intensional empty input by the user.

Constructing dataclass
======================

Dictionary from the model data can be used to construct the dataclass instance.

>>> from dataclasses import dataclass
>>> @dataclass
... class DataClass:
...     x: int
...     y: int
>>> data = dict(x=1, y=2)
>>> DataClass(**data)
DataClass(x=1, y=2)

However, this does not recursively apply to nested dataclass.

>>> @dataclass
... class DataClass2:
...     a: DataClass
>>> data = dict(a=dict(x=1, y=2))
>>> DataClass2(**data)  # expect DataClass2(a=DataClass(x=1, y=2))
DataClass2(a={'x': 1, 'y': 2})

Therefore it is recommended to use third-party packages such as `cattrs <https://pypi.org/project/cattrs/1.5.0/>`_ which supports this feature.
