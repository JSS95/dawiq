===================================
How to use multiple dataclass types
===================================

.. currentmodule:: dawiq

Sometimes the items in your model may need to store data from different dataclasses.

Basic example
=============

As an example, we create a widget which consists of:

* Combo box to display dataclass types of the model. Change of index submits data.
* Stacked widget which contains data widgets.
* Buttons to change the model index.

Creating the dataclasses
------------------------

First, let's define the dataclasses.

.. code-block:: python

    from dataclasses import dataclass

    @dataclass
    class DataClass1:
        x: int
        y: bool

    @dataclass
    class DataClass2:
        x: int
        y: float
        z: bool

Creating the widget
-------------------

We create the widget, add the dataclass types to the combo box and data widget to the stacked widget.
The first widget of the stacked widget is an empty widget.

.. tabs::

    .. code-tab:: python
        :caption: PySide6

        from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QComboBox,
            QStackedWidget, QPushButton)
        from dawiq import dataclass2Widget
        import sys

        app = QApplication(sys.argv)

        class MyWidget(QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)

                self.setLayout(QVBoxLayout())

                self.comboBox = QComboBox()
                self.comboBox.setPlaceholderText("Select dataclass type")
                self.layout().addWidget(self.comboBox)

                self.stackedWidget = QStackedWidget()
                self.layout().addWidget(self.stackedWidget)

                self.btn1 = QPushButton("Previous")
                self.btn2 = QPushButton("Next")
                self.layout().addWidget(self.btn1)
                self.layout().addWidget(self.btn2)

        myWidget = MyWidget()

        myWidget.stackedWidget.addWidget(QWidget())

        for cls in [DataClass1, DataClass2]:
            myWidget.comboBox.addItem(cls.__name__, cls)
            myWidget.stackedWidget.addWidget(dataclass2Widget(cls))

Constructing the model
----------------------

We construct a model with three rows and two columns.
The first column stores the dataclass type and the second column stores the dataclass data.

.. tabs::

    .. code-tab:: python
        :caption: PySide6

        from PySide6.QtGui import QStandardItemModel, QStandardItem

        model = QStandardItemModel()
        for _ in range(3):
            model.appendRow([QStandardItem(), QStandardItem()])

Defining a delegate
-------------------

Now we define a delegate for ``MyWidget`` and ``model`` to update data.

.. tabs::

    .. code-tab:: python
        :caption: PySide6

        from PySide6.QtCore import Qt
        from dawiq import DataclassDelegate

        class MyDelegate(DataclassDelegate):
            ClassRole = Qt.UserRole
            ...

        delegate = MyDelegate()

Map the model and widget
------------------------

.. code-block:: python

    from dawiq import DataclassMapper

    mapper = DataclassMapper()
    mapper.setItemDelegate(delegate)
    mapper.setModel(model)
    mapper.addMapping(myWidget.comboBox, 0)
    mapper.addMapping(myWidget.stackedWidget, 1)
    mapper.setCurrentIndex(0)

Display
-------

.. tabs::

    .. code-tab:: python
        :caption: PySide6

        myWidget.show()
        app.exec()
        app.quit()
