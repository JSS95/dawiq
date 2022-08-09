from dawiq import type2Widget, BoolCheckBox
from dawiq.qt_compat import QtCore
from typing import Optional


def test_type2Widget(qtbot):
    assert isinstance(type2Widget(bool), BoolCheckBox)
    assert not type2Widget(bool).isTristate()
    assert isinstance(type2Widget(Optional[bool]), BoolCheckBox)
    assert type2Widget(Optional[bool]).isTristate()


def test_BoolCheckBox(qtbot):
    widget = BoolCheckBox()

    # test dataValueChanged signal
    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val is True,
    ):
        widget.setCheckState(QtCore.Qt.CheckState.Checked)
    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val is False,
    ):
        widget.setCheckState(QtCore.Qt.CheckState.Unchecked)

    # test tristate
    widget.setTristate(True)
    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val is True,
    ):
        widget.setCheckState(QtCore.Qt.CheckState.Checked)
    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val is False,
    ):
        widget.setCheckState(QtCore.Qt.CheckState.Unchecked)
    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val is None,
    ):
        widget.setCheckState(QtCore.Qt.CheckState.PartiallyChecked)
