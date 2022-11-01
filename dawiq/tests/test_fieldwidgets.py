from dawiq import (
    BoolCheckBox,
    EmptyIntValidator,
    IntLineEdit,
    EmptyFloatValidator,
    FloatLineEdit,
    StrLineEdit,
    EnumComboBox,
    TupleGroupBox,
)
import enum
from dawiq.qt_compat import QtCore, QtWidgets


def test_BoolCheckBox(qtbot):
    widget = BoolCheckBox()
    widget.setCheckState(QtCore.Qt.CheckState.Unchecked)

    # test value change by setFieldValue
    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val is True,
    ):
        widget.setFieldValue(True)
    assert widget.fieldValue() is True
    assert widget.checkState() == QtCore.Qt.CheckState.Checked

    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val is False,
    ):
        widget.setFieldValue(False)
    assert widget.fieldValue() is False
    assert widget.checkState() == QtCore.Qt.CheckState.Unchecked

    widget.setCheckState(QtCore.Qt.CheckState.Unchecked)

    # test value change by clicking
    with qtbot.waitSignals(
        [widget.fieldValueChanged, widget.fieldEdited],
        check_params_cbs=[lambda val: val is True, lambda: True],
    ):
        widget.click()
    assert widget.fieldValue() is True
    assert widget.checkState() == QtCore.Qt.CheckState.Checked

    with qtbot.waitSignals(
        [widget.fieldValueChanged, widget.fieldEdited],
        check_params_cbs=[lambda val: val is False, lambda: True],
    ):
        widget.click()
    assert widget.fieldValue() is False
    assert widget.checkState() == QtCore.Qt.CheckState.Unchecked


def test_BoolCheckBox_tristate(qtbot):
    widget = BoolCheckBox()
    widget.setCheckState(QtCore.Qt.CheckState.Checked)

    widget.setTristate(False)
    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val is False,
    ):
        widget.setFieldValue(None)
    assert widget.fieldValue() is False
    assert widget.checkState() == QtCore.Qt.CheckState.Unchecked

    widget.setTristate(True)
    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val is None,
    ):
        widget.setFieldValue(None)
    assert widget.fieldValue() is None
    assert widget.checkState() == QtCore.Qt.CheckState.PartiallyChecked


def test_BoolCheckBox_setRequired(qtbot):
    """Check box always has field value."""
    widget = BoolCheckBox()

    widget.setRequired(True)
    assert not widget.property("requiresFieldValue")
    widget.click()
    widget.setRequired(True)
    assert not widget.property("requiresFieldValue")

    widget.setRequired(False)
    assert not widget.property("requiresFieldValue")
    widget.click()
    widget.setRequired(False)
    assert not widget.property("requiresFieldValue")


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

    assert widget.fieldValue() is None
    assert not widget.text()

    # test value change by setFieldValue
    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val == 1,
    ):
        widget.setFieldValue(1)
    assert widget.fieldValue() == 1
    assert widget.text() == "1"

    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val is None,
    ):
        widget.setFieldValue(None)
    assert widget.fieldValue() is None
    assert not widget.text()

    # test value change by keyboard
    widget.clear()
    with qtbot.waitSignals(
        [widget.fieldEdited],
        check_params_cbs=[lambda: True],
    ):
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    assert widget.fieldValue() is None

    with qtbot.waitSignals(
        [widget.fieldValueChanged, widget.fieldEdited],
        check_params_cbs=[lambda val: val == 1, lambda: True],
    ):
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    assert widget.fieldValue() == 1


def test_IntLineEdit_setRequired(qtbot):
    widget = IntLineEdit()

    widget.setRequired(True)
    assert widget.property("requiresFieldValue")
    widget.setFieldValue(10)
    widget.setRequired(True)
    assert not widget.property("requiresFieldValue")

    widget.clear()
    widget.setRequired(False)
    assert not widget.property("requiresFieldValue")
    widget.setRequired(True)
    assert widget.property("requiresFieldValue")


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

    assert widget.fieldValue() is None
    assert not widget.text()

    # test value change by setFieldValue
    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val == 1.2,
    ):
        widget.setFieldValue(1.2)
    assert widget.fieldValue() == 1.2
    assert widget.text() == "1.2"

    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val is None,
    ):
        widget.setFieldValue(None)
    assert widget.fieldValue() is None
    assert not widget.text()

    # test value change by keyboard
    widget.clear()
    with qtbot.waitSignals(
        [widget.fieldEdited],
        check_params_cbs=[lambda: True],
    ):
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    assert widget.fieldValue() is None

    with qtbot.waitSignals(
        [widget.fieldValueChanged, widget.fieldEdited],
        check_params_cbs=[lambda val: val == 1.2, lambda: True],
    ):
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, ".")
        qtbot.keyPress(widget, "2")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    assert widget.fieldValue() == 1.2


def test_FloatLineEdit_setRequired(qtbot):
    widget = FloatLineEdit()

    widget.setRequired(True)
    assert widget.property("requiresFieldValue")
    widget.setFieldValue(10.0)
    widget.setRequired(True)
    assert not widget.property("requiresFieldValue")

    widget.clear()
    widget.setRequired(False)
    assert not widget.property("requiresFieldValue")
    widget.setRequired(True)
    assert widget.property("requiresFieldValue")


def test_StrLineEdit(qtbot):
    widget = StrLineEdit()

    assert widget.fieldValue() == ""
    assert not widget.text()

    # test value change by setFieldValue
    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val == "1",
    ):
        widget.setFieldValue("1")
    assert widget.fieldValue() == "1"
    assert widget.text() == "1"
    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val == "x",
    ):
        widget.setFieldValue("x")
    assert widget.fieldValue() == "x"
    assert widget.text() == "x"

    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val == "",
    ):
        widget.setFieldValue(None)
    assert widget.fieldValue() == ""
    assert widget.text() == ""

    # test value change by keyboard
    widget.clear()
    with qtbot.waitSignals(
        [widget.fieldEdited],
        check_params_cbs=[lambda: True],
    ):
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    assert widget.fieldValue() == ""

    with qtbot.waitSignals(
        [widget.fieldValueChanged, widget.fieldEdited],
        check_params_cbs=[lambda val: val == "x", lambda: True],
    ):
        qtbot.keyPress(widget, "x")
        qtbot.keyPress(widget, QtCore.Qt.Key.Key_Return)
    assert widget.fieldValue() == "x"


def test_StrLineEdit_setRequired(qtbot):
    """String line edit always has field value."""
    widget = StrLineEdit()

    widget.setRequired(True)
    assert not widget.property("requiresFieldValue")
    widget.setFieldValue("spam")
    widget.setRequired(True)
    assert not widget.property("requiresFieldValue")

    widget.clear()
    widget.setRequired(False)
    assert not widget.property("requiresFieldValue")
    widget.setRequired(True)
    assert not widget.property("requiresFieldValue")


def test_EnumComboBox(qtbot):
    class MyEnum(enum.Enum):
        x = 1
        y = 2
        z = 3

    widget = EnumComboBox.fromEnum(MyEnum)

    assert widget.count() == 3
    assert widget.currentIndex() == -1
    assert widget.fieldValue() is None

    # test with setFieldValue
    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val == MyEnum.x,
    ):
        widget.setFieldValue(MyEnum.x)
    assert widget.currentIndex() == 0
    assert widget.fieldValue() == MyEnum.x

    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val == MyEnum.y,
    ):
        widget.setFieldValue(MyEnum.y)
    assert widget.currentIndex() == 1
    assert widget.fieldValue() == MyEnum.y

    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val == MyEnum.z,
    ):
        widget.setFieldValue(MyEnum.z)
    assert widget.currentIndex() == 2
    assert widget.fieldValue() == MyEnum.z

    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val is None,
    ):
        widget.setFieldValue(None)
    assert widget.currentIndex() == -1
    assert widget.fieldValue() is None

    # test with setCurrentIndex
    with qtbot.waitSignals(
        [widget.fieldValueChanged, widget.fieldEdited],
        check_params_cbs=[lambda val: val == MyEnum.x, lambda: True],
    ):
        qtbot.keyClick(widget, MyEnum.x.name)
    assert widget.currentIndex() == 0
    assert widget.fieldValue() == MyEnum.x


def test_EnumComboBox_setRequired(qtbot):
    class MyEnum(enum.Enum):
        x = 1
        y = 2
        z = 3

    widget = EnumComboBox.fromEnum(MyEnum)

    widget.setRequired(True)
    assert widget.property("requiresFieldValue")
    widget.setCurrentIndex(1)
    widget.setRequired(True)
    assert not widget.property("requiresFieldValue")

    widget.setRequired(False)
    assert not widget.property("requiresFieldValue")
    widget.setCurrentIndex(-1)
    widget.setRequired(False)
    assert not widget.property("requiresFieldValue")


def test_TupleGroupBox_addWidget(qtbot):
    widget = TupleGroupBox()
    assert widget.count() == 0

    w0 = BoolCheckBox()
    widget.addWidget(w0)
    assert widget.count() == 1
    assert widget.widget(0) is w0
    assert widget.widget(1) is None

    w1 = IntLineEdit()
    widget.addWidget(w1)
    assert widget.count() == 2
    assert widget.widget(0) is w0
    assert widget.widget(1) is w1

    # test that signals are connected
    with qtbot.waitSignals([widget.fieldValueChanged, widget.fieldEdited]):
        w0.click()
    with qtbot.waitSignals([widget.fieldValueChanged, widget.fieldEdited]):
        qtbot.keyPress(w1, "1")
        qtbot.keyPress(w1, QtCore.Qt.Key.Key_Return)


def test_TupleGroupBox_insertWidget(qtbot):
    widget = TupleGroupBox()
    assert widget.count() == 0

    w0 = BoolCheckBox()
    widget.insertWidget(0, w0)
    assert widget.count() == 1
    assert widget.widget(0) is w0
    assert widget.widget(1) is None

    w1 = IntLineEdit()
    widget.insertWidget(0, w1)
    assert widget.count() == 2
    assert widget.widget(0) is w1
    assert widget.widget(1) is w0

    # test that signals are connected
    with qtbot.waitSignals([widget.fieldValueChanged, widget.fieldEdited]):
        w0.click()
    with qtbot.waitSignals([widget.fieldValueChanged, widget.fieldEdited]):
        qtbot.keyPress(w1, "1")
        qtbot.keyPress(w1, QtCore.Qt.Key.Key_Return)


def test_TupleGroupBox_removeWidget(qtbot):
    widget = TupleGroupBox()
    w0 = BoolCheckBox()
    w1 = IntLineEdit()

    widget.addWidget(w0)
    assert widget.count() == 1

    widget.removeWidget(w1)
    assert widget.count() == 1

    widget.removeWidget(w0)
    assert widget.count() == 0

    # test that signals are disconnected
    with qtbot.assertNotEmitted(widget.fieldValueChanged):
        w0.click()
    with qtbot.assertNotEmitted(widget.fieldEdited):
        w0.click()
    with qtbot.assertNotEmitted(widget.fieldValueChanged):
        qtbot.keyPress(w1, "1")
        qtbot.keyPress(w1, QtCore.Qt.Key.Key_Return)
    with qtbot.assertNotEmitted(widget.fieldEdited):
        qtbot.keyPress(w1, "1")
        qtbot.keyPress(w1, QtCore.Qt.Key.Key_Return)


def test_TupleGroupBox_fieldValue(qtbot):
    widget = TupleGroupBox()
    widget.addWidget(IntLineEdit())
    widget.addWidget(IntLineEdit())
    assert widget.fieldValue() == (None, None)

    widget.widget(0).setText("1")
    widget.widget(1).setText("2")
    assert widget.fieldValue() == (1, 2)


def test_TupleGroupBox_setFieldValue(qtbot):
    widget = TupleGroupBox()
    widget.addWidget(IntLineEdit())
    widget.addWidget(IntLineEdit())

    class Counter:
        def __init__(self):
            self.i = 0

        def count(self):
            self.i += 1

        def reset(self):
            self.i = 0

    counter = Counter()
    widget.fieldValueChanged.connect(counter.count)

    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val == (1, 2),
    ):
        widget.setFieldValue((1, 2))
    assert widget.fieldValue() == (1, 2)
    assert counter.i == 1

    counter.reset()
    with qtbot.waitSignal(
        widget.fieldValueChanged,
        check_params_cb=lambda val: val == (None, None),
    ):
        widget.setFieldValue(None)
    assert widget.fieldValue() == (None, None)
    assert counter.i == 1


def test_TupleGroupBox_subwidget(qtbot):
    widget = TupleGroupBox()
    widget.addWidget(IntLineEdit())
    widget.addWidget(IntLineEdit())

    with qtbot.waitSignals(
        [widget.fieldValueChanged, widget.fieldEdited],
        check_params_cbs=[lambda val: val == (1, None), lambda: True],
    ):
        qtbot.keyPress(widget.widget(0), "1")
        qtbot.keyPress(widget.widget(0), QtCore.Qt.Key.Key_Return)
    assert widget.fieldValue() == (1, None)

    with qtbot.waitSignals(
        [widget.fieldValueChanged, widget.fieldEdited],
        check_params_cbs=[lambda val: val == (1, 2), lambda: True],
    ):
        qtbot.keyPress(widget.widget(1), "2")
        qtbot.keyPress(widget.widget(1), QtCore.Qt.Key.Key_Return)
    assert widget.fieldValue() == (1, 2)


def test_TupleGroupBox_setRequired(qtbot):
    widget = TupleGroupBox()
    widget.addWidget(IntLineEdit())
    widget.addWidget(IntLineEdit())

    widget.setRequired(True)
    assert widget.widget(0).property("requiresFieldValue")
    assert widget.widget(1).property("requiresFieldValue")
    widget.setFieldValue((None, 1))
    widget.setRequired(True)
    assert widget.widget(0).property("requiresFieldValue")
    assert not widget.widget(1).property("requiresFieldValue")
    widget.setFieldValue((0, 1))
    widget.setRequired(True)
    assert not widget.widget(0).property("requiresFieldValue")
    assert not widget.widget(1).property("requiresFieldValue")

    widget.widget(0).clear()
    widget.widget(1).clear()

    widget.setRequired(False)
    assert not widget.widget(0).property("requiresFieldValue")
    assert not widget.widget(1).property("requiresFieldValue")
    widget.setFieldValue((None, 1))
    widget.setRequired(False)
    assert not widget.widget(0).property("requiresFieldValue")
    assert not widget.widget(1).property("requiresFieldValue")
    widget.setFieldValue((0, 1))
    widget.setRequired(False)
    assert not widget.widget(0).property("requiresFieldValue")
    assert not widget.widget(1).property("requiresFieldValue")
