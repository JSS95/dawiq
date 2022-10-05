.. _construct-dataclass:

===============================
Constructing dataclass instance
===============================

.. currentmodule:: dawiq

In :ref:`data-model` document, we learned how to store the widget data into the model.
Here, we will construct the dataclass instance from the model data.

Constructing nested dataclass
=============================

First we define a complicated, nested dataclass.

>>> import dataclasses
>>> from typing import Tuple, Optional
>>> @dataclasses.dataclass
... class Inner:
...     x: int
>>> @dataclasses.dataclass
... class DataClass:
...     a: Tuple[Optional[int], Optional[int]] = dataclasses.field(
...         metadata=dict(Qt_typehint=Tuple[int, int]),
...     )
...     b: Inner

The nested dataclass can be unstructured by :func:`dataclasses.asdict`, but there is no standard way to restructure the dataclass from the dictionary.

>>> dcls = DataClass((None, 2), Inner(3))
>>> dcls
DataClass(a=(None, 2), b=Inner(x=3))
>>> args = dataclasses.asdict(dcls)
>>> args
{'a': (None, 2), 'b': {'x': 3}}
>>> DataClass(**args)  # inner dataclass is not reconstructed.
DataClass(a=(None, 2), b={'x': 3})

There are many third-party packages to resolve this.
Here, we use `cattrs <https://pypi.org/project/cattrs/1.5.0/>`_ package which supports nested reconstructions and converters.

>>> import cattrs
>>> cattrs.structure(args, DataClass)
DataClass(a=(None, 2), b=Inner(x=3))

We will see how to use the converters of :mod:`cattrs` shortly after.

Converting argument types
=========================

In our example, the items of ``DataClass.a`` have ``Optional[int]`` type; :class:`int` is the valid value and :obj:`None` is the placeholder.
However the :class:`.TupleGroupBox` generated from ``DataClass.a`` uses :obj:`.MISSING` as the placeholder for empty widget data.

>>> from dawiq import MISSING
>>> cattrs.structure(dict(a=(MISSING, 2), b=dict(x=3)), DataClass)
Traceback (most recent call last):
...
ClassValidationError: While structuring DataClass (1 sub-exception)

Using Qt converters explained in :ref:`data-model` is undesirable here because it will need :mod:`dawiq` to be imported in dataclass definition.
We don't want this because we want to separate the dataclass and the GUI.
