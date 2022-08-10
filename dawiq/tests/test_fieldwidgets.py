from dawiq import (
    type2Widget,
    BoolCheckBox,
    EmptyIntValidator,
    IntLineEdit,
    MISSING,
)
from dawiq.qt_compat import QtCore, QtWidgets
from typing import Optional


def test_type2Widget(qtbot):
    assert isinstance(type2Widget(bool), BoolCheckBox)
    assert not type2Widget(bool).isTristate()
    assert isinstance(type2Widget(Optional[bool]), BoolCheckBox)
    assert type2Widget(Optional[bool]).isTristate()

    assert isinstance(type2Widget(int), IntLineEdit)
    assert not type2Widget(int).hasDefaultDataValue()
    assert isinstance(type2Widget(Optional[int]), IntLineEdit)
    assert type2Widget(Optional[int]).hasDefaultDataValue()


def test_BoolCheckBox(qtbot):
    widget = BoolCheckBox()

    # test dataValueChanged signal
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is True,
    ):
        widget.setCheckState(QtCore.Qt.CheckState.Checked)
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is False,
    ):
        widget.setCheckState(QtCore.Qt.CheckState.Unchecked)

    # test tristate
    widget.setTristate(True)
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is True,
    ):
        widget.setCheckState(QtCore.Qt.CheckState.Checked)
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is False,
    ):
        widget.setCheckState(QtCore.Qt.CheckState.Unchecked)
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is None,
    ):
        widget.setCheckState(QtCore.Qt.CheckState.PartiallyChecked)


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

    widget.setText("")
    widget.setDefaultDataValue(MISSING)
    assert not widget.hasDefaultDataValue()
    assert widget.dataValue() is MISSING
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is MISSING,
    ):
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val == 1,
    ):
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)

    widget.setText("")
    widget.setDefaultDataValue(None)
    assert widget.hasDefaultDataValue()
    assert widget.dataValue() is None
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val is None,
    ):
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val == 1,
    ):
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)

    widget.setText("")
    widget.setDefaultDataValue(10)
    assert widget.hasDefaultDataValue()
    assert widget.dataValue() == 10
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val == 10,
    ):
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    with qtbot.waitSignal(
        widget.dataValueChanged,
        check_params_cb=lambda val: val == 1,
    ):
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
