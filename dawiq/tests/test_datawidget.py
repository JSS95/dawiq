from dawiq import DataWidget, BoolCheckBox
import pytest


def test_DataWidget_addWidget(qtbot):
    datawidget = DataWidget()
    assert datawidget.count() == 0

    w0 = BoolCheckBox()
    w0.setText("w0")
    datawidget.addWidget(w0)
    assert datawidget.count() == 1
    assert datawidget.widget(0) is w0
    assert datawidget.widget(1) is None

    w1 = BoolCheckBox()
    w1.setText("w0")
    with pytest.raises(KeyError):
        datawidget.addWidget(w1)

    w1.setText("w1")
    datawidget.addWidget(w1)
    assert datawidget.count() == 2
    assert datawidget.widget(0) is w0
    assert datawidget.widget(1) is w1


def test_DataWidget_insertWidget(qtbot):
    datawidget = DataWidget()
    assert datawidget.count() == 0

    w0 = BoolCheckBox()
    w0.setText("w0")
    datawidget.insertWidget(0, w0)
    assert datawidget.count() == 1
    assert datawidget.widget(0) is w0
    assert datawidget.widget(1) is None

    w1 = BoolCheckBox()
    w1.setText("w0")
    with pytest.raises(KeyError):
        datawidget.insertWidget(0, w1)

    w1.setText("w1")
    datawidget.insertWidget(0, w1)
    assert datawidget.count() == 2
    assert datawidget.widget(0) is w1
    assert datawidget.widget(1) is w0


def test_DataWidget_removeWidget(qtbot):
    datawidget = DataWidget()
    w0 = BoolCheckBox()
    w0.setText("w0")
    w1 = BoolCheckBox()
    w1.setText("w1")

    datawidget.addWidget(w0)
    assert datawidget.count() == 1

    datawidget.removeWidget(w1)
    assert datawidget.count() == 1

    datawidget.removeWidget(w0)
    assert datawidget.count() == 0
