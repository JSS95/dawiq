from dawiq import (
    BoolCheckBox,
    EmptyIntValidator,
    IntLineEdit,
    EmptyFloatValidator,
    FloatLineEdit,
    StrLineEdit,
    EnumComboBox,
    TupleGroupBox,
    MISSING,
)
import enum
from dawiq.qt_compat import QtCore, QtWidgets


def test_BoolCheckBox(qtbot):
    widget = BoolCheckBox()
    widget.setTristate(True)
    widget.setCheckState(QtCore.Qt.CheckState.Unchecked)

    # test value change by setDataValue
    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue(True)
    assert widget.dataValue() is True
    assert widget.checkState() == QtCore.Qt.CheckState.Checked

    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue(False)
    assert widget.dataValue() is False
    assert widget.checkState() == QtCore.Qt.CheckState.Unchecked

    widget.setCheckState(QtCore.Qt.CheckState.Checked)  # set to True to test MISSING
    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue(MISSING)
    assert widget.dataValue() is False
    assert widget.checkState() == QtCore.Qt.CheckState.Unchecked

    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue(None)
    assert widget.dataValue() is None
    assert widget.checkState() == QtCore.Qt.CheckState.PartiallyChecked

    widget.setCheckState(QtCore.Qt.CheckState.Unchecked)

    # test value change by clicking
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is None,
    ):
        widget.click()
    assert widget.dataValue() is None
    assert widget.checkState() == QtCore.Qt.CheckState.PartiallyChecked

    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is True,
    ):
        widget.click()
    assert widget.dataValue() is True
    assert widget.checkState() == QtCore.Qt.CheckState.Checked

    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is False,
    ):
        widget.click()
    assert widget.dataValue() is False
    assert widget.checkState() == QtCore.Qt.CheckState.Unchecked


def test_EmptyIntValidator(qtbot):
    widget = QtWidgets.QLineEdit()
    widget.setValidator(EmptyIntValidator(widget))

    # empty text is valid
    with qtbot.waitSignal(widget.editingFinished):
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)

    with qtbot.assertNotEmitted(widget.editingFinished):
        qtbot.keyPress(widget, "-")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)

    with qtbot.waitSignal(widget.editingFinished):
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)


def test_IntLineEdit(qtbot):
    widget = IntLineEdit()

    # test value change by setDataValue
    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue(MISSING)
    assert widget.dataValue() is MISSING
    assert not widget.text()

    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue(1)
    assert widget.dataValue() == 1
    assert widget.text() == "1"

    widget.clear()

    # test value change by keyboard
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is MISSING,
    ):
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    assert widget.dataValue() is MISSING

    with qtbot.assertNotEmitted(widget.dataValueChanged):
        qtbot.keyPress(widget, "-")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    assert widget.dataValue() is MISSING

    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val == -1,
    ):
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    assert widget.dataValue() == -1


def test_EmptyFloatValidator(qtbot):
    widget = QtWidgets.QLineEdit()
    widget.setValidator(EmptyFloatValidator(widget))

    # empty text is valid
    with qtbot.waitSignal(widget.editingFinished):
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)

    with qtbot.assertNotEmitted(widget.editingFinished):
        qtbot.keyPress(widget, "-")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)

    with qtbot.waitSignal(widget.editingFinished):
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)

    with qtbot.waitSignal(widget.editingFinished):
        qtbot.keyPress(widget, ".")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)

    with qtbot.waitSignal(widget.editingFinished):
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)


def test_FloatLineEdit(qtbot):
    widget = FloatLineEdit()

    # test value change by setDataValue
    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue(MISSING)
    assert widget.dataValue() is MISSING
    assert not widget.text()

    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue(1.0)
    assert widget.dataValue() == float(1)
    assert widget.text() == "1.0"

    widget.clear()

    # test value change by keyboard
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is MISSING,
    ):
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    assert widget.dataValue() is MISSING

    with qtbot.assertNotEmitted(widget.dataValueChanged):
        qtbot.keyPress(widget, "-")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    assert widget.dataValue() is MISSING

    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val == float(-1),
    ):
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    assert widget.dataValue() == float(-1)


def test_StrLineEdit(qtbot):
    widget = StrLineEdit()

    # test value change by setDataValue
    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue(MISSING)
    assert widget.dataValue() == ""
    assert not widget.text()

    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue("1")
    assert widget.dataValue() == "1"
    assert widget.text() == "1"

    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue("x")
    assert widget.dataValue() == "x"
    assert widget.text() == "x"

    widget.clear()

    # test value change by keyboard
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val == "",
    ):
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    assert widget.dataValue() == ""

    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val == "x",
    ):
        qtbot.keyPress(widget, "x")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    assert widget.dataValue() == "x"


def test_EnumComboBox(qtbot):
    class MyEnum(enum.Enum):
        x = 1
        y = 2
        z = 3

    widget = EnumComboBox.fromEnum(MyEnum)
    assert widget.count() == 3
    assert widget.currentIndex() == -1
    assert widget.dataValue() is MISSING

    # test with setDataValue
    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue(MyEnum.x)
    assert widget.currentIndex() == 0
    assert widget.dataValue() == MyEnum.x

    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue(MyEnum.y)
    assert widget.currentIndex() == 1
    assert widget.dataValue() == MyEnum.y

    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue(MyEnum.z)
    assert widget.currentIndex() == 2
    assert widget.dataValue() == MyEnum.z

    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue(MISSING)
    assert widget.currentIndex() == -1
    assert widget.dataValue() is MISSING

    # test with setCurrentIndex

    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val == MyEnum.x,
    ):
        widget.setCurrentIndex(0)
    assert widget.dataValue() == MyEnum.x

    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val == MyEnum.y,
    ):
        widget.setCurrentIndex(1)
    assert widget.dataValue() == MyEnum.y

    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val == MyEnum.z,
    ):
        widget.setCurrentIndex(2)
    assert widget.dataValue() == MyEnum.z

    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val is MISSING,
    ):
        widget.setCurrentIndex(-1)
    assert widget.dataValue() is MISSING


def test_TupleGroupBox_addWidget(qtbot):
    tupleWidget = TupleGroupBox()
    assert tupleWidget.count() == 0

    w0 = BoolCheckBox()
    tupleWidget.addWidget(w0)
    assert tupleWidget.count() == 1
    assert tupleWidget.widget(0) is w0
    assert tupleWidget.widget(1) is None

    w1 = IntLineEdit()
    tupleWidget.addWidget(w1)
    assert tupleWidget.count() == 2
    assert tupleWidget.widget(0) is w0
    assert tupleWidget.widget(1) is w1

    # test that signals are connected
    with qtbot.waitSignal(tupleWidget.dataValueChanged):
        w0.click()
    with qtbot.waitSignal(tupleWidget.dataValueChanged):
        qtbot.keyPress(w1, QtCore.Qt.Key.Key_Return)


def test_TupleGroupBox_insertWidget(qtbot):
    tupleWidget = TupleGroupBox()
    assert tupleWidget.count() == 0

    w0 = BoolCheckBox()
    tupleWidget.insertWidget(0, w0)
    assert tupleWidget.count() == 1
    assert tupleWidget.widget(0) is w0
    assert tupleWidget.widget(1) is None

    w1 = IntLineEdit()
    tupleWidget.insertWidget(0, w1)
    assert tupleWidget.count() == 2
    assert tupleWidget.widget(0) is w1
    assert tupleWidget.widget(1) is w0

    # test that signals are connected
    with qtbot.waitSignal(tupleWidget.dataValueChanged):
        w0.click()
    with qtbot.waitSignal(tupleWidget.dataValueChanged):
        qtbot.keyPress(w1, QtCore.Qt.Key.Key_Return)


def test_TupleGroupBox_removeWidget(qtbot):
    tupleWidget = TupleGroupBox()
    w0 = BoolCheckBox()
    w1 = IntLineEdit()

    tupleWidget.addWidget(w0)
    assert tupleWidget.count() == 1

    tupleWidget.removeWidget(w1)
    assert tupleWidget.count() == 1

    tupleWidget.removeWidget(w0)
    assert tupleWidget.count() == 0

    # test that signals are disconnected
    with qtbot.assertNotEmitted(tupleWidget.dataValueChanged):
        w0.click()


def test_TupleGroupBox_dataValue(qtbot):
    widget = TupleGroupBox()
    widget.addWidget(IntLineEdit())
    widget.addWidget(IntLineEdit())
    assert widget.dataValue() == (MISSING, MISSING)

    widget.widget(0).setText("1")
    widget.widget(1).setText("2")
    assert widget.dataValue() == (1, 2)


def test_TupleGroupBox_setDataValue(qtbot):
    widget = TupleGroupBox()
    widget.addWidget(IntLineEdit())
    widget.addWidget(IntLineEdit())

    class Counter:
        def __init__(self):
            self.i = 0

        def count(self):
            self.i += 1

    counter = Counter()
    widget.dataValueChanged.connect(counter.count)

    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue((1, 2))
    assert widget.dataValue() == (1, 2)
    assert counter.i == 0

    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setDataValue(MISSING)
    assert widget.dataValue() == (MISSING, MISSING)


def test_TupleGroupBox_subwidget(qtbot):
    widget = TupleGroupBox()
    widget.addWidget(IntLineEdit())
    widget.addWidget(IntLineEdit())

    with qtbot.waitSignal(
        widget.dataValueChanged, check_params_cb=lambda tup: tup == (1, MISSING)
    ):
        qtbot.keyPress(widget.widget(0), "1")
        qtbot.keyPress(widget.widget(0), QtCore.Qt.Key.Key_Return)
    assert widget.dataValue() == (1, MISSING)

    with qtbot.waitSignal(
        widget.dataValueChanged, check_params_cb=lambda tup: tup == (1, 2)
    ):
        qtbot.keyPress(widget.widget(1), "2")
        qtbot.keyPress(widget.widget(1), QtCore.Qt.Key.Key_Return)
    assert widget.dataValue() == (1, 2)
