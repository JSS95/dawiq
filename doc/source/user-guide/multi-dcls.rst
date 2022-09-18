===================================
How to use multiple dataclass types
===================================

.. currentmodule:: dawiq

Sometimes the items in your model may need to store data from different dataclasses.

First, let's define dataclasses.

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

We create a widget which consists of:

* Combo box to display dataclass types of the model.
* Stacked widget which contains data widgets.
* Buttons to change the model index.

.. tabs::

    .. code-tab:: python
        :caption: PySide6

        from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QComboBox,
            QStackedWidget, QPushButton)
        from dawiq import dataclass2Widget
        import sys

        app = QApplication(sys.argv)

        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        comboBox = QComboBox()
        widget.layout().addWidget(comboBox)
        stackedWidget = QStackedWidget()
        widget.layout().addWidget(stackedWidget)
        btn1 = QPushButton("Previous")
        widget.layout().addWidget(btn1)
        btn2 = QPushButton("Next")
        widget.layout().addWidget(btn2)

.. tabs::

    .. code-tab:: python
        :caption: PySide6

        stackedWidget.addWidget(dataclass2Widget(DataClass1))
        stackedWidget.addWidget(dataclass2Widget(DataClass2))

        widget.show()
        app.exec()
        app.quit()
