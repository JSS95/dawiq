.. _widget:

==============================
How to create dataclass widget
==============================

.. currentmodule:: dawiq

User can create :class:`.DataWidget` from the dataclass type using :func:`.dataclass2Widget`.

By default, type hint of every field must be supported by :func:`.type2Widget`.
If your type hint is not supported, specify the alternative type hint by setting ``Qt_typehint`` metadata to the field.

Basic example
=============

Here is a reproducible code for the example in :ref:`intro` page.
First, let's define a simple dataclass.

.. code-block:: python

    from dataclasses import dataclass

    @dataclass
    class DataClass:
        x: int
        y: bool

We then create a widget and display it.

.. tabs::

    .. code-tab:: python
        :caption: PySide6

        from PySide6.QtWidgets import QApplication
        from dawiq import dataclass2Widget
        import sys

        app = QApplication(sys.argv)
        dataWidget = dataclass2Widget(DataClass)
        dataWidget.show()
        app.exec()
        app.quit()

    .. code-tab:: python
        :caption: PyQt6

        from PyQt6.QtWidgets import QApplication
        from dawiq import dataclass2Widget
        import sys

        app = QApplication(sys.argv)
        dataWidget = dataclass2Widget(DataClass)
        dataWidget.show()
        app.exec()
        app.quit()

    .. code-tab:: python
        :caption: PySide2

        from PySide2.QtWidgets import QApplication
        from dawiq import dataclass2Widget
        import sys

        app = QApplication(sys.argv)
        dataWidget = dataclass2Widget(DataClass)
        dataWidget.show()
        app.exec_()
        app.quit()

    .. code-tab:: python
        :caption: PyQt5

        from PyQt5.QtWidgets import QApplication
        from dawiq import dataclass2Widget
        import sys

        app = QApplication(sys.argv)
        dataWidget = dataclass2Widget(DataClass)
        dataWidget.show()
        app.exec()
        app.quit()

Your widget will look like this:

.. figure:: ../_images/widget-example.jpg
   :align: center

   Widget with :class:`.IntLineEdit` and :class:`.BoolCheckBox`

Nested dataclass example
========================

Nested dataclass is supported by nested widget.

.. code-block:: python

    from dataclasses import dataclass

    @dataclass
    class Inner:
        a: int

    @dataclass
    class DataClass:
        x: bool
        y: Inner

.. figure:: ../_images/nested-example.jpg
   :align: center

   Widget with :class:`.BoolCheckBox` and nested :class:`.DataWidget`

Type hint example
=================

.. _type-hint:

The following example shows how to specify the alternative type hint using ``Qt_typehint`` metadata.

On the first example, the type hint is ``Union[int, float]`` but :func:`.dataclass2Widget` treats the field as :class:`float`.

.. code-block:: python

    from dataclasses import dataclass, field
    from typing import Union

    @dataclass
    class DataClass:
        x: Union[int, float] = field(metadata=dict(Qt_typehint=float))

.. figure:: ../_images/typehint-example.jpg
   :align: center

   Widget with :class:`.FloatLineEdit`

Now for the second example we define ``CustomClass`` which takes two integers as parameters.
:func:`.dataclass2Widget` treats the field as ``Tuple[int, int]`` and creates the widget which fits to it.

.. code-block:: python

    from dataclasses import dataclass, field
    from typing import Tuple

    class CustomClass:
        def __init__(self, x, y):
            ...

    @dataclass
    class DataClass:
        custom: CustomClass = field(metadata=dict(Qt_typehint=Tuple[int, int]))

.. figure:: ../_images/custom-typehint-example.jpg
   :align: center

   Widget with :class:`.TupleGroupBox` with two :class:`.IntLineEdit`

When setting or retrieving the data from this widget, other metadata are required to convert ``CustomClass`` to ``Tuple[int, int]`` and vice versa.
It is explained in :ref:`data-model` page.
