.. _data-model:

=====================
How to use item model
=====================

.. currentmodule:: dawiq

:class:`.DataWidget` can be synced with item model by using :class:`.DataclassDelegate` and :class:`.DataclassMapper`.
The data are stored as :obj:`dict`, and user can convert it to dataclass instance if required.

.. note::
   Nested dataclasses are stored as nested dictionaries, which can be easily reconstructed by using `cattrs <https://pypi.org/project/cattrs/1.5.0/>`_ package.

As explained in :ref:`widget`, field type can be different from widget data type.
In this case we need to define the converters between them by setting two metadata to the field:

* ``toQt_converter``: unary callable which converts field data to widget data
* ``fromQt_converter``: unary callable which converts widget data to field data

Basic example
=============

This is the basic example without data converter.

First we define a dataclass, and construct a delegate and a mapper.

.. code-block:: python

    from dataclasses import dataclass
    from dawiq import DataclassDelegate, DataclassMapper

    @dataclass
    class DataClass:
        x: float
        y: bool

    delegate = DataclassDelegate()
    mapper = DataclassMapper()
    mapper.setItemDelegate(delegate)

Then we construct a model with two items and set it to the mapper.
Each item stores the dataclass type which will be read by the delegate.

.. note::
   Dataclass type in the model is read-only with default :class:`DataclassDelegate`.
   To make it writable, refer to :ref:`multi-dcls` example.

.. tabs::

    .. code-tab:: python
        :caption: PySide6

        from PySide6.QtGui import QStandardItemModel, QStandardItem

        model = QStandardItemModel()
        for _ in range(2):
            item = QStandardItem()
            item.setData(DataClass, role=delegate.TypeRole)
            model.appendRow(item)
        mapper.setModel(model)

    .. code-tab:: python
        :caption: PyQt6

        from PyQt6.QtGui import QStandardItemModel, QStandardItem

        model = QStandardItemModel()
        for _ in range(2):
            item = QStandardItem()
            item.setData(DataClass, role=delegate.TypeRole)
            model.appendRow(item)
        mapper.setModel(model)

    .. code-tab:: python
        :caption: PySide2

        from PySide2.QtGui import QStandardItemModel, QStandardItem

        model = QStandardItemModel()
        for _ in range(2):
            item = QStandardItem()
            item.setData(DataClass, role=delegate.TypeRole)
            model.appendRow(item)
        mapper.setModel(model)

    .. code-tab:: python
        :caption: PyQt5

        from PyQt5.QtGui import QStandardItemModel, QStandardItem

        model = QStandardItemModel()
        for _ in range(2):
            item = QStandardItem()
            item.setData(DataClass, role=delegate.TypeRole)
            model.appendRow(item)
        mapper.setModel(model)

Now, we create a widget which consists of:
* Data widget from ``DataClass``
* Buttons to change the model index

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

Data converter example
======================

In this example, we define the data converters for ``CustomClass`` from :ref:`Specifying type hint <type-hint>`.

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
    mapper = DataclassMapper()
    mapper.setItemDelegate(delegate)

.. figure:: ../_images/model-converter-example.jpg
   :align: center

   Widget with model compatible to custom type

Note that the dataclass defines default value, but the widget is still empty.
Default value is not updated to model and to empty widget, in order to distinguish the intensional empty input by the user.
