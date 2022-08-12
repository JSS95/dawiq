from dawiq import (
    BoolCheckBox,
    EmptyIntValidator,
    IntLineEdit,
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
