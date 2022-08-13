from dawiq import (
    BoolCheckBox,
    EmptyIntValidator,
    IntLineEdit,
    EmptyFloatValidator,
    FloatLineEdit,
    StrLineEdit,
    MISSING,
)
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
