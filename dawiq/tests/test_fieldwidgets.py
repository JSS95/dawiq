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
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is True,
    ):
        widget.setDataValue(True)
    assert widget.dataValue() is True
    assert widget.checkState() == QtCore.Qt.CheckState.Checked

    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is False,
    ):
        widget.setDataValue(False)
    assert widget.dataValue() is False
    assert widget.checkState() == QtCore.Qt.CheckState.Unchecked

    widget.setCheckState(QtCore.Qt.CheckState.Checked)  # set to True to test MISSING
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is False,
    ):
        widget.setDataValue(MISSING)
    assert widget.dataValue() is False
    assert widget.checkState() == QtCore.Qt.CheckState.Unchecked

    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is None,
    ):
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
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is MISSING,
    ):
        widget.setDataValue(MISSING)
    assert widget.dataValue() is MISSING
    assert not widget.text()

    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val == 1,
    ):
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
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is MISSING,
    ):
        widget.setDataValue(MISSING)
    assert widget.dataValue() is MISSING
    assert not widget.text()

    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val == float(1),
    ):
        widget.setDataValue(1)
    assert widget.dataValue() == float(1)
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
        check_params_cb=lambda val: val == float(-1),
    ):
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    assert widget.dataValue() == float(-1)


def test_StrLineEdit(qtbot):
    widget = StrLineEdit()

    # test value change by setDataValue
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val == "",
    ):
        widget.setDataValue(MISSING)
    assert widget.dataValue() == ""
    assert not widget.text()

    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val == "1",
    ):
        widget.setDataValue("1")
    assert widget.dataValue() == "1"
    assert widget.text() == "1"

    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val == "x",
    ):
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

    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val == MyEnum.x,
    ):
        widget.setDataValue(MyEnum.x)
    assert widget.currentIndex() == 0
    assert widget.dataValue() == MyEnum.x

    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val == MyEnum.y,
    ):
        widget.setDataValue(MyEnum.y)
    assert widget.currentIndex() == 1
    assert widget.dataValue() == MyEnum.y

    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val == MyEnum.z,
    ):
        widget.setDataValue(MyEnum.z)
    assert widget.currentIndex() == 2
    assert widget.dataValue() == MyEnum.z

    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val is MISSING,
    ):
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


def test_TupleGroupBox_dataValue(qtbot):
    widget = TupleGroupBox.fromWidgets([IntLineEdit(), IntLineEdit()])
    assert widget.dataValue() == (MISSING, MISSING)

    widget.widget(0).setText("1")
    widget.widget(1).setText("2")
    assert widget.dataValue() == (1, 2)


def test_TupleGroupBox_setDataValue(qtbot):
    widget = TupleGroupBox.fromWidgets([IntLineEdit(), IntLineEdit()])

    class Counter:
        def __init__(self):
            self.i = 0

        def count(self):
            self.i += 1

    counter = Counter()
    widget.dataValueChanged.connect(counter.count)

    with qtbot.waitSignal(
        widget.dataValueChanged, check_params_cb=lambda tup: tup == (1, 2)
    ):
        widget.setDataValue((1, 2))
    assert widget.dataValue() == (1, 2)
    assert counter.i == 1

    with qtbot.waitSignal(
        widget.dataValueChanged, check_params_cb=lambda tup: tup == (MISSING, MISSING)
    ):
        widget.setDataValue(MISSING)
    assert widget.dataValue() == (MISSING, MISSING)


def test_TupleGroupBox_subwidget(qtbot):
    widget = TupleGroupBox.fromWidgets([IntLineEdit(), IntLineEdit()])

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
