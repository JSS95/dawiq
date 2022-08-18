# DaWiQ - Dataclass Widget for Qt

[![Build Status](https://github.com/JSS95/dawiq/actions/workflows/ci.yml/badge.svg)](https://github.com/JSS95/dawiq/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/dawiq/badge/?version=latest)](https://dawiq.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/github/license/JSS95/dawiq)](https://github.com/JSS95/dawiq/blob/master/LICENSE)

DaWiQ is a Python package to generate Qt widget from dataclass.

It provides:
- Dynamic construction of widget from dataclass
- Customizing widget for user-defined type
- Delegate and mapper for dataclass widget

The following Qt bindings are supported:
- [PySide6](https://pypi.org/project/PySide6/)
- [PySide2](https://pypi.org/project/PySide2/)
- [PyQt6](https://pypi.org/project/PyQt6/)
- [PyQt5](https://pypi.org/project/PyQt5/)

# Usage

Here is a simple dataclass:

```python
from dataclasses import dataclass
from typing import Tuple

@dataclass
class DataClass:
    a: int
    b: bool
```

DaWiQ can build a widget from this dataclass. For PySide6 example,

```python
from PySide6.QtWidgets import QApplication
from dawiq import dataclass2Widget
import sys

app = QApplication(sys.argv)
dataWidget = dataclass2Widget(DataClass)
dataWidget.show()
app.exec()
app.quit()
```

<div align="center">
  <img src="https://github.com/JSS95/dawiq/raw/master/doc/source/_images/widget-example.jpg"/><br>
</div>

This widget can be mapped to item model for storing the data.
More examples are provided in the documentation.

# Documentation

Documentation can be found on Read the Docs:

> https://dawiq.readthedocs.io/
