==================
Mapping with model
==================

.. code-block:: python

    from dataclasses import dataclass
    from dawiq import DataclassDelegate, DataclassMapper

    @dataclass
    class DataClass:
        x: int
        y: bool

    delegate = DataclassDelegate()
    mapper = DataclassMapper()
