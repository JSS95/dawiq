from .dynqt import QtWidgets
from typing import Any
from .typing import FieldWidgetProtocol


__all__ = [
    "type2Widget",
    "BoolCheckBox",
]


def type2Widget(t: Any) -> FieldWidgetProtocol:
    """Return the widget instance for given type annotation."""
    if isinstance(t, type) and issubclass(t, bool):
        return BoolCheckBox()
    raise TypeError("Unknown type or annotation: %s" % t)


class BoolCheckBox(QtWidgets.QCheckBox):
    def dataName(self) -> str:
        return self.text()

    def setDataName(self, name: str):
        self.setText(name)
        self.setToolTip(name)
