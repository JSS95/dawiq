# DaWiQ - Dataclass Widget with Qt

[![PyPI version](https://badge.fury.io/py/DaWiQ.svg)](https://badge.fury.io/py/DaWiQ)
[![Python Version](https://img.shields.io/pypi/pyversions/dawiq)](https://pypi.org/project/dawiq/)
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

# Installation

DaWiQ can be installed from `PyPI`.

```
$ pip install dawiq
```

To install from GitHub source, clone the repository with `git` and install with `pip`.

```
$ git clone https://github.com/JSS95/dawiq.git
$ cd dawiq
$ pip install .
```

DaWiQ does not specify the Qt binding requirement, therefore you must manually install one.

# Documentation

DaWiQ is documented with [Sphinx](https://pypi.org/project/Sphinx/). Documentation can be found on Read the Docs:

> https://dawiq.readthedocs.io/

If you want to build the document yourself, get the source code and install with `[doc]` option.
Then go to `doc` directory and build the document.

```
$ pip install .[doc]
$ cd doc
$ make html
```

Document will be generated in `build/html` directory. Open `index.html` to see the central page.
