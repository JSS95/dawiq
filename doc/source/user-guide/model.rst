.. _data-model:

==================
Mapping with model
==================

.. currentmodule:: dawiq

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
