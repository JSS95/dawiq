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

We construct a model with three rows which stores the dataclass type and data.

.. tabs::

    .. code-tab:: python
        :caption: PySide6

        from PySide6.QtGui import QStandardItemModel, QStandardItem

        model = QStandardItemModel()
        for _ in range(3):
            model.appendRow(QStandardItem())

Defining a delegate
-------------------

Now we define a delegate for ``myWidget`` and ``model`` to update the data.

.. tabs::

    .. code-tab:: python
        :caption: PySide6

        from dawiq import DataclassDelegate

        class MyDelegate(DataclassDelegate):
            TypeRole = DataclassDelegate.DataRole + 1

            def setModelData(self, editor, model, index):
                if isinstance(editor, MyWidget):
                    dcls = editor.comboBox.currentData()
                    self.setDataclassType(dcls)
                    model.setData(index, dcls, role=self.TypeRole)
                    dataWidget = editor.stackedWidget.currentWidget()
                    self.setModelData(dataWidget, model, index)
                else:
                    super().setModelData(editor, model, index)

            def setEditorData(self, editor, index):
                if isinstance(editor, MyWidget):
                    dcls = index.data(role=self.TypeRole)
                    self.setDataclassType(dcls)
                    comboBoxIdx = editor.comboBox.findData(dcls)
                    editor.comboBox.setCurrentIndex(comboBoxIdx)
                    editor.stackedWidget.setCurrentIndex(comboBoxIdx + 1)
                    dataWidget = editor.stackedWidget.currentWidget()
                    self.setEditorData(dataWidget, index)
                else:
                    super().setEditorData(editor, index)

        delegate = MyDelegate()

Map the model and widget
------------------------

.. code-block:: python

    from dawiq import DataclassMapper, DataWidget

    mapper = DataclassMapper()
    mapper.setItemDelegate(delegate)
    mapper.setModel(model)
    myWidget.btn1.clicked.connect(mapper.toPrevious)
    myWidget.btn2.clicked.connect(mapper.toNext)

    mapper.addMapping(myWidget, 0)
    myWidget.comboBox.currentIndexChanged.connect(mapper.submit)
    for i in range(myWidget.stackedWidget.count()):
        widget = myWidget.stackedWidget.widget(i)
        if isinstance(widget, DataWidget):
            widget.dataValueChanged.connect(mapper.submit)

    mapper.setCurrentIndex(0)

Display
-------

.. tabs::

    .. code-tab:: python
        :caption: PySide6

        myWidget.show()
        app.exec()
        app.quit()
