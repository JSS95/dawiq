from dawiq import (
    DataWidget,
    type2Widget,
    dataclass2Widget,
    BoolCheckBox,
    IntLineEdit,
    FloatLineEdit,
    StrLineEdit,
    EnumComboBox,
    TupleGroupBox,
)
from dawiq.qt_compat import QtCore
import dataclasses
from enum import Enum
from typing import Optional, Tuple
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

    # test that signals are connected
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

    # test that signals are disconnected
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

    # test that signals are disconnected
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
    assert dataWidget.dataValue() == dict(a=None, b=dict(x=None))

    dataWidget.widget(0).setText("1")
    dataWidget.widget(1).widget(0).setText("2")
    assert dataWidget.dataValue() == dict(a=1, b=dict(x=2))


def test_DataWidget_setDataValue(qtbot):
    @dataclasses.dataclass
    class Cls1:
        x: bool

    @dataclasses.dataclass
    class Cls2:
        a: int
        b: Cls1

    dataWidget = dataclass2Widget(Cls2)

    class Counter:
        def __init__(self):
            self.i = 0

        def count(self):
            self.i += 1

    counter = Counter()
    dataWidget.dataValueChanged.connect(counter.count)
    dval = dict(a=1, b=dict(x=True))

    with qtbot.assertNotEmitted(dataWidget.dataValueChanged):
        dataWidget.setDataValue(dval)
    assert dataWidget.dataValue() == dval
    assert counter.i == 0

    with qtbot.assertNotEmitted(dataWidget.dataValueChanged):
        dataWidget.setDataValue(None)
    assert dataWidget.dataValue() == dict(a=None, b=dict(x=False))


def test_DataWidget_subwidget(qtbot):
    @dataclasses.dataclass
    class Cls1:
        x: bool

    @dataclasses.dataclass
    class Cls2:
        a: int
        b: Cls1

    dataWidget = dataclass2Widget(Cls2)

    with qtbot.waitSignal(
        dataWidget.dataValueChanged,
        check_params_cb=lambda val: val == dict(a=None, b=dict(x=True)),
    ):
        dataWidget.widget(1).widget(0).click()
    assert dataWidget.dataValue() == dict(a=None, b=dict(x=True))

    with qtbot.waitSignal(
        dataWidget.dataValueChanged,
        check_params_cb=lambda tup: tup == dict(a=1, b=dict(x=True)),
    ):
        qtbot.keyPress(dataWidget.widget(0), "1")
        qtbot.keyPress(dataWidget.widget(0), QtCore.Qt.Key.Key_Return)
    assert dataWidget.dataValue() == dict(a=1, b=dict(x=True))


def test_type2Widget(qtbot):
    assert isinstance(type2Widget(bool), BoolCheckBox)
    assert not type2Widget(bool).isTristate()
    assert isinstance(type2Widget(Optional[bool]), BoolCheckBox)
    assert type2Widget(Optional[bool]).isTristate()

    assert isinstance(type2Widget(int), IntLineEdit)
    assert isinstance(type2Widget(Optional[int]), IntLineEdit)

    assert isinstance(type2Widget(float), FloatLineEdit)
    assert isinstance(type2Widget(Optional[float]), FloatLineEdit)

    assert isinstance(type2Widget(str), StrLineEdit)
    assert isinstance(type2Widget(Optional[str]), StrLineEdit)

    class E(Enum):
        x = 1

    assert isinstance(type2Widget(E), EnumComboBox)
    assert isinstance(type2Widget(Optional[E]), EnumComboBox)

    with pytest.raises(TypeError):
        type2Widget(Tuple)
    with pytest.raises(TypeError):
        type2Widget(Tuple[int, ...])
    assert isinstance(type2Widget(Tuple[int, bool, E]), TupleGroupBox)


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
