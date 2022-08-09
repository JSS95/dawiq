from dawiq import BoolCheckBox
from dawiq.dynqt import QtCore


def test_BoolCheckBox(qtbot):
    widget = BoolCheckBox()

    # test dataValueChanged signal
    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val is True,
    ):
        widget.setCheckState(QtCore.Qt.Checked)
    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val is False,
    ):
        widget.setCheckState(QtCore.Qt.Unchecked)

    # test tristate
    widget.setTristate(True)
    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val is True,
    ):
        widget.setCheckState(QtCore.Qt.Checked)
    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val is False,
    ):
        widget.setCheckState(QtCore.Qt.Unchecked)
    with qtbot.waitSignal(
        widget.dataValueChanged,
        raising=True,
        check_params_cb=lambda val: val is None,
    ):
        widget.setCheckState(QtCore.Qt.PartiallyChecked)
