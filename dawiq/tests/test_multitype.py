from dawiq import DataWidgetStack, DataWidgetTab, dataclass2Widget
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
def dataWidgetStack(qtbot):
    widget = DataWidgetStack()
    widget.addWidget(QtWidgets.QWidget())
    for dcls in [DataClass1, DataClass2]:
        widget.addDataWidget(dataclass2Widget(dcls), dcls)

    return widget


def test_DataWidgetStack_indexOfDataclass(qtbot, dataWidgetStack):
    assert dataWidgetStack.indexOfDataclass(DataClass1) == 1
    assert dataWidgetStack.indexOfDataclass(DataClass2) == 2
    assert dataWidgetStack.indexOfDataclass(DataClass3) == -1


def test_DataWidgetStack_currentDataValueChanged(qtbot, dataWidgetStack):
    dataWidgetStack.setCurrentIndex(0)
    with qtbot.assertNotEmitted(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(2).widget(0).click()

    dataWidgetStack.setCurrentIndex(1)
    with qtbot.waitSignal(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(2).widget(0).click()

    dataWidgetStack.setCurrentIndex(2)
    with qtbot.assertNotEmitted(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(1).widget(0).click()
    with qtbot.waitSignal(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(2).widget(0).click()

    dataWidgetStack.setCurrentWidget(dataWidgetStack.widget(0))
    with qtbot.assertNotEmitted(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(2).widget(0).click()

    dataWidgetStack.setCurrentWidget(dataWidgetStack.widget(1))
    with qtbot.waitSignal(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(2).widget(0).click()

    dataWidgetStack.setCurrentWidget(dataWidgetStack.widget(2))
    with qtbot.assertNotEmitted(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(1).widget(0).click()
    with qtbot.waitSignal(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(2).widget(0).click()


def test_DataWidgetStack_removeWidget(qtbot, dataWidgetStack):
    dataWidgetStack.setCurrentIndex(2)
    oldWidget = dataWidgetStack.currentWidget()
    dataWidgetStack.removeWidget(oldWidget)
    assert dataWidgetStack.indexOfDataclass(DataClass2) == -1
    assert dataWidgetStack.currentIndex() == 1
    with qtbot.waitSignal(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataWidgetStack.currentDataValueChanged):
        oldWidget.widget(0).click()

    oldWidget = dataWidgetStack.currentWidget()
    dataWidgetStack.removeWidget(oldWidget)
    assert dataWidgetStack.indexOfDataclass(DataClass1) == -1
    assert dataWidgetStack.currentIndex() == 0
    with qtbot.assertNotEmitted(dataWidgetStack.currentDataValueChanged):
        oldWidget.widget(0).click()

    oldWidget = dataWidgetStack.currentWidget()
    dataWidgetStack.removeWidget(oldWidget)
    assert dataWidgetStack.currentIndex() == -1


@pytest.fixture
def dataWidgetTab(qtbot):
    widget = DataWidgetTab()
    widget.addTab(QtWidgets.QWidget(), "EmptyTab")
    widget.addTab(dataclass2Widget(DataClass1), DataClass1.__name__)
    widget.addTab(dataclass2Widget(DataClass2), DataClass2.__name__)

    return widget


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
