from dawiq import (
    DataWidget,
    type2Widget,
    dataclass2Widget,
    BoolCheckBox,
    IntLineEdit,
    MISSING,
)
from dawiq.qt_compat import QtCore
import dataclasses
from typing import Optional
import pytest


def test_DataWidget_addWidget(qtbot):
    datawidget = DataWidget()
    assert datawidget.count() == 0

    w0 = BoolCheckBox()
    w0.setFieldName("w0")
    datawidget.addWidget(w0)
    assert datawidget.count() == 1
    assert datawidget.widget(0) is w0
    assert datawidget.widget(1) is None

    w1 = IntLineEdit()
    w1.setFieldName("w0")
    with pytest.raises(KeyError):
        datawidget.addWidget(w1)

    w1.setFieldName("w1")
    datawidget.addWidget(w1)
    assert datawidget.count() == 2
    assert datawidget.widget(0) is w0
    assert datawidget.widget(1) is w1

    with qtbot.waitSignal(datawidget.dataValueChanged):
        w0.click()
    with qtbot.waitSignal(datawidget.dataValueChanged):
        qtbot.keyPress(w1, QtCore.Qt.Key.Key_Return)


def test_DataWidget_insertWidget(qtbot):
    datawidget = DataWidget()
    assert datawidget.count() == 0

    w0 = BoolCheckBox()
    w0.setFieldName("w0")
    datawidget.insertWidget(0, w0)
    assert datawidget.count() == 1
    assert datawidget.widget(0) is w0
    assert datawidget.widget(1) is None

    w1 = IntLineEdit()
    w1.setFieldName("w0")
    with pytest.raises(KeyError):
        datawidget.insertWidget(0, w1)

    w1.setFieldName("w1")
    datawidget.insertWidget(0, w1)
    assert datawidget.count() == 2
    assert datawidget.widget(0) is w1
    assert datawidget.widget(1) is w0

    with qtbot.waitSignal(datawidget.dataValueChanged):
        w0.click()
    with qtbot.waitSignal(datawidget.dataValueChanged):
        qtbot.keyPress(w1, QtCore.Qt.Key.Key_Return)


def test_DataWidget_removeWidget(qtbot):
    datawidget = DataWidget()
    w0 = BoolCheckBox()
    w0.setFieldName("w0")
    w1 = IntLineEdit()
    w1.setFieldName("w1")

    datawidget.addWidget(w0)
    assert datawidget.count() == 1

    datawidget.removeWidget(w1)
    assert datawidget.count() == 1

    datawidget.removeWidget(w0)
    assert datawidget.count() == 0

    with qtbot.assertNotEmitted(datawidget.dataValueChanged):
        w0.click()


def test_DataWidget_dataValue(qtbot):
    @dataclasses.dataclass
    class Cls1:
        x: int

    @dataclasses.dataclass
    class Cls2:
        a: int
        b: Cls1

    dataWidget = dataclass2Widget(Cls2)
    assert dataWidget.dataValue() == dict(a=MISSING, b=dict(x=MISSING))

    dataWidget.widget(0).setText("1")
    dataWidget.widget(1).widget(0).setText("2")
    assert dataWidget.dataValue() == dict(a=1, b=dict(x=2))


def test_type2Widget(qtbot):
    assert isinstance(type2Widget(bool), BoolCheckBox)
    assert not type2Widget(bool).isTristate()
    assert isinstance(type2Widget(Optional[bool]), BoolCheckBox)
    assert type2Widget(Optional[bool]).isTristate()

    assert isinstance(type2Widget(int), IntLineEdit)


def test_dataclass2Widget(qtbot):
    @dataclasses.dataclass
    class Cls1:
        x: int

    @dataclasses.dataclass
    class Cls2:
        a: "int"
        b: bool
        c: float = dataclasses.field(metadata=dict(Qt_typehint=int))
        d: Cls1

    dataWidget = dataclass2Widget(Cls2)

    assert isinstance(dataWidget.widget(0), IntLineEdit)
    assert dataWidget.widget(0).fieldName() == "a"

    assert isinstance(dataWidget.widget(1), BoolCheckBox)
    assert dataWidget.widget(1).fieldName() == "b"

    assert isinstance(dataWidget.widget(2), IntLineEdit)
    assert dataWidget.widget(2).fieldName() == "c"

    assert isinstance(dataWidget.widget(3), DataWidget)
    assert dataWidget.widget(3).fieldName() == "d"
    assert isinstance(dataWidget.widget(3).widget(0), IntLineEdit)
    assert dataWidget.widget(3).widget(0).fieldName() == "x"
