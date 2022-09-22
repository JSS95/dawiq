===================================
How to use multiple dataclass types
===================================

.. currentmodule:: dawiq

Sometimes the items in your model may need to store the data from different dataclasses, and you want to modify not only the data but the dataclass type as well.
This requires complicated delegate to update both the widget and the model.

Basic example
=============

As an example, we create a widget which consists of:

* Combo box to choose the dataclass type.
* Stacked widget which contains the data widgets.
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
        z: bool

    @dataclass
    class DataClass2:
        x: int
        y: float
        z: bool
        t: int

Note that the two dataclasses partially share their fields.
When the the data widget is changed by selecting different dataclass type, values of the common fields in the model data will be updated to the new widget.

Creating the widget
-------------------

We create the widget, add the dataclass types to the combo box and the data widgets to the stacked widget.
The first widget of the stacked widget is an empty widget to represent invalid dataclass type.

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

We construct a model with three items.
Each item will store the dataclass type and the data with different data role.

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
Caution should be made to prevent the model from being updated multiple times.

.. code-block:: python

    from dawiq import DataclassDelegate

    class MyDelegate(DataclassDelegate):
        TypeRole = DataclassDelegate.DataRole + 1

        def __init__(self, parent=None):
            super().__init__(parent)
            self.freeze_model = False

        def setModelData(self, editor, model, index):
            if isinstance(editor, MyWidget) and not self.freeze_model:
                dcls = editor.comboBox.currentData()
                if dcls is not model.data(index, role=self.TypeRole):
                    self.setDataclassType(dcls)
                    model.setData(index, dcls, role=self.TypeRole)
                else:
                    dataWidget = editor.stackedWidget.currentWidget()
                    self.setModelData(dataWidget, model, index)
            else:
                super().setModelData(editor, model, index)

        def setEditorData(self, editor, index):
            if isinstance(editor, MyWidget):
                dcls = index.data(role=self.TypeRole)
                comboBoxIdx = editor.comboBox.findData(dcls)
                if comboBoxIdx != editor.comboBox.currentIndex():
                    self.setDataclassType(dcls)
                    self.freeze_model = True
                    editor.comboBox.setCurrentIndex(comboBoxIdx)
                    self.freeze_model = False
                if (comboBoxIdx + 1) != editor.stackedWidget.currentIndex():
                    editor.stackedWidget.setCurrentIndex(comboBoxIdx + 1)
                dataWidget = editor.stackedWidget.currentWidget()
                self.setEditorData(dataWidget, index)
            else:
                super().setEditorData(editor, index)

    delegate = MyDelegate()

Map the model and widget
------------------------

The last step is to map the model and the widget.
Mapper submits the data when the dataclass type is changed by combo box, or when the data value is changed by the data widget.

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

Result
------

Now let's set the model data and display the widget.

.. tabs::

    .. code-tab:: python
        :caption: PySide6

        model.setData(model.index(0, 0), DataClass1, MyDelegate.TypeRole)
        model.setData(model.index(0, 0), dict(z=True), MyDelegate.DataRole)

        myWidget.show()
        app.exec()
        app.quit()

.. figure:: ../_images/multi-dcls-example.jpg
   :align: center

   Widget with multiple dataclasses

Try change the dataclass type, set the data and switch the model index.
