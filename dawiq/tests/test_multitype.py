from dawiq import DataclassStackWidget, DataWidgetTab, dataclass2Widget
from dawiq.qt_compat import QtWidgets
import dataclasses
import pytest


@dataclasses.dataclass
class DataClass1:
    x: bool


@dataclasses.dataclass
class DataClass2:
    a: bool
    b: bool
    c: bool
    d: bool
    e: bool


@dataclasses.dataclass
class DataClass3:
    x: bool


@pytest.fixture
def dataclassStackWidget(qtbot):
    widget = DataclassStackWidget()
    widget.addWidget(QtWidgets.QWidget())
    for dcls in [DataClass1, DataClass2]:
        widget.addDataWidget(dataclass2Widget(dcls), dcls)

    return widget


def test_DataclassStackWidget_currentDataclass(qtbot, dataclassStackWidget):
    dataclassStackWidget.setCurrentIndex(0)
    assert dataclassStackWidget.currentDataclass() is None
    dataclassStackWidget.setCurrentIndex(1)
    assert dataclassStackWidget.currentDataclass() == DataClass1
    dataclassStackWidget.setCurrentIndex(2)
    assert dataclassStackWidget.currentDataclass() == DataClass2


def test_DataclassStackWidget_indexOfDataclass(qtbot, dataclassStackWidget):
    assert dataclassStackWidget.indexOfDataclass(DataClass1) == 1
    assert dataclassStackWidget.indexOfDataclass(DataClass2) == 2
    assert dataclassStackWidget.indexOfDataclass(DataClass3) == -1


def test_DataclassStackWidget_currentDataValueChanged(qtbot, dataclassStackWidget):
    dataclassStackWidget.setCurrentIndex(0)
    with qtbot.assertNotEmitted(dataclassStackWidget.currentDataValueChanged):
        dataclassStackWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassStackWidget.currentDataValueChanged):
        dataclassStackWidget.widget(2).widget(0).click()

    dataclassStackWidget.setCurrentIndex(1)
    with qtbot.waitSignal(dataclassStackWidget.currentDataValueChanged):
        dataclassStackWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassStackWidget.currentDataValueChanged):
        dataclassStackWidget.widget(2).widget(0).click()

    dataclassStackWidget.setCurrentIndex(2)
    with qtbot.assertNotEmitted(dataclassStackWidget.currentDataValueChanged):
        dataclassStackWidget.widget(1).widget(0).click()
    with qtbot.waitSignal(dataclassStackWidget.currentDataValueChanged):
        dataclassStackWidget.widget(2).widget(0).click()

    dataclassStackWidget.setCurrentWidget(dataclassStackWidget.widget(0))
    with qtbot.assertNotEmitted(dataclassStackWidget.currentDataValueChanged):
        dataclassStackWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassStackWidget.currentDataValueChanged):
        dataclassStackWidget.widget(2).widget(0).click()

    dataclassStackWidget.setCurrentWidget(dataclassStackWidget.widget(1))
    with qtbot.waitSignal(dataclassStackWidget.currentDataValueChanged):
        dataclassStackWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassStackWidget.currentDataValueChanged):
        dataclassStackWidget.widget(2).widget(0).click()

    dataclassStackWidget.setCurrentWidget(dataclassStackWidget.widget(2))
    with qtbot.assertNotEmitted(dataclassStackWidget.currentDataValueChanged):
        dataclassStackWidget.widget(1).widget(0).click()
    with qtbot.waitSignal(dataclassStackWidget.currentDataValueChanged):
        dataclassStackWidget.widget(2).widget(0).click()


def test_DataclassStackWidget_removeWidget(qtbot, dataclassStackWidget):
    dataclassStackWidget.setCurrentIndex(2)
    oldWidget = dataclassStackWidget.currentWidget()
    dataclassStackWidget.removeWidget(oldWidget)
    assert dataclassStackWidget.indexOfDataclass(DataClass2) == -1
    assert dataclassStackWidget.currentIndex() == 1
    with qtbot.waitSignal(dataclassStackWidget.currentDataValueChanged):
        dataclassStackWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassStackWidget.currentDataValueChanged):
        oldWidget.widget(0).click()

    oldWidget = dataclassStackWidget.currentWidget()
    dataclassStackWidget.removeWidget(oldWidget)
    assert dataclassStackWidget.indexOfDataclass(DataClass1) == -1
    assert dataclassStackWidget.currentIndex() == 0
    with qtbot.assertNotEmitted(dataclassStackWidget.currentDataValueChanged):
        oldWidget.widget(0).click()

    oldWidget = dataclassStackWidget.currentWidget()
    dataclassStackWidget.removeWidget(oldWidget)
    assert dataclassStackWidget.currentIndex() == -1


@pytest.fixture
def dataWidgetTab(qtbot):
    widget = DataWidgetTab()
    widget.addTab(QtWidgets.QWidget(), "EmptyTab")
    for dcls in [DataClass1, DataClass2]:
        widget.addDataWidget(dataclass2Widget(dcls), dcls.__name__, dcls)

    return widget


def test_DataWidgetTab_currentDataclass(qtbot, dataWidgetTab):
    dataWidgetTab.setCurrentIndex(0)
    assert dataWidgetTab.currentDataclass() is None
    dataWidgetTab.setCurrentIndex(1)
    assert dataWidgetTab.currentDataclass() == DataClass1
    dataWidgetTab.setCurrentIndex(2)
    assert dataWidgetTab.currentDataclass() == DataClass2


def test_DataWidgetTab_indexOfDataclass(qtbot, dataWidgetTab):
    assert dataWidgetTab.indexOfDataclass(DataClass1) == 1
    assert dataWidgetTab.indexOfDataclass(DataClass2) == 2
    assert dataWidgetTab.indexOfDataclass(DataClass3) == -1


def test_DataWidgetTab_currentDataValueChanged(qtbot, dataWidgetTab):
    dataWidgetTab.setCurrentIndex(0)
    with qtbot.assertNotEmitted(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(2).widget(0).click()

    dataWidgetTab.setCurrentIndex(1)
    with qtbot.waitSignal(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(2).widget(0).click()

    dataWidgetTab.setCurrentIndex(2)
    with qtbot.assertNotEmitted(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(1).widget(0).click()
    with qtbot.waitSignal(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(2).widget(0).click()

    dataWidgetTab.setCurrentWidget(dataWidgetTab.widget(0))
    with qtbot.assertNotEmitted(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(2).widget(0).click()

    dataWidgetTab.setCurrentWidget(dataWidgetTab.widget(1))
    with qtbot.waitSignal(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(2).widget(0).click()

    dataWidgetTab.setCurrentWidget(dataWidgetTab.widget(2))
    with qtbot.assertNotEmitted(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(1).widget(0).click()
    with qtbot.waitSignal(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(2).widget(0).click()


def test_DataWidgetTab_removeTab(qtbot, dataWidgetTab):
    dataWidgetTab.setCurrentIndex(2)
    oldTab = dataWidgetTab.currentWidget()
    dataWidgetTab.removeTab(dataWidgetTab.indexOf(oldTab))
    assert dataWidgetTab.currentIndex() == 1
    with qtbot.waitSignal(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataWidgetTab.currentDataValueChanged):
        oldTab.widget(0).click()

    oldTab = dataWidgetTab.currentWidget()
    dataWidgetTab.removeTab(dataWidgetTab.indexOf(oldTab))
    assert dataWidgetTab.currentIndex() == 0
    with qtbot.assertNotEmitted(dataWidgetTab.currentDataValueChanged):
        oldTab.widget(0).click()

    oldTab = dataWidgetTab.currentWidget()
    dataWidgetTab.removeTab(dataWidgetTab.indexOf(oldTab))
    assert dataWidgetTab.currentIndex() == -1
