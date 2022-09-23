from dawiq import DataWidgetStack, DataWidgetTab, dataclass2Widget
import dataclasses
import pytest


@pytest.fixture
def dataWidgetStack(qtbot):
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

    widget = DataWidgetStack()
    widget.addWidget(dataclass2Widget(DataClass1))
    widget.addWidget(dataclass2Widget(DataClass2))

    return widget


def test_DataWidgetStack_currentDataValueChanged(qtbot, dataWidgetStack):
    dataWidgetStack.setCurrentIndex(0)
    with qtbot.waitSignal(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(0).widget(0).click()
    with qtbot.assertNotEmitted(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(1).widget(0).click()

    dataWidgetStack.setCurrentIndex(1)
    with qtbot.assertNotEmitted(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(0).widget(0).click()
    with qtbot.waitSignal(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(1).widget(0).click()

    widget0 = dataWidgetStack.widget(0)
    dataWidgetStack.setCurrentWidget(widget0)
    with qtbot.waitSignal(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(0).widget(0).click()
    with qtbot.assertNotEmitted(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(1).widget(0).click()

    widget1 = dataWidgetStack.widget(1)
    dataWidgetStack.setCurrentWidget(widget1)
    with qtbot.assertNotEmitted(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(0).widget(0).click()
    with qtbot.waitSignal(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(1).widget(0).click()


def test_DataWidgetStack_removeWidget(qtbot, dataWidgetStack):
    dataWidgetStack.setCurrentIndex(1)
    oldWidget = dataWidgetStack.currentWidget()
    dataWidgetStack.removeWidget(oldWidget)
    assert dataWidgetStack.currentIndex() == 0
    with qtbot.waitSignal(dataWidgetStack.currentDataValueChanged):
        dataWidgetStack.widget(0).widget(0).click()
    with qtbot.assertNotEmitted(dataWidgetStack.currentDataValueChanged):
        oldWidget.widget(0).click()

    oldWidget = dataWidgetStack.currentWidget()
    dataWidgetStack.removeWidget(oldWidget)
    assert dataWidgetStack.currentIndex() == -1
    with qtbot.assertNotEmitted(dataWidgetStack.currentDataValueChanged):
        oldWidget.widget(0).click()


@pytest.fixture
def dataWidgetTab(qtbot):
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

    widget = DataWidgetTab()
    widget.addTab(dataclass2Widget(DataClass1), DataClass1.__name__)
    widget.addTab(dataclass2Widget(DataClass2), DataClass2.__name__)

    return widget


def test_DataWidgetTab_currentDataValueChanged(qtbot, dataWidgetTab):
    dataWidgetTab.setCurrentIndex(0)
    with qtbot.waitSignal(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(0).widget(0).click()
    with qtbot.assertNotEmitted(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(1).widget(0).click()

    dataWidgetTab.setCurrentIndex(1)
    with qtbot.assertNotEmitted(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(0).widget(0).click()
    with qtbot.waitSignal(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(1).widget(0).click()

    widget0 = dataWidgetTab.widget(0)
    dataWidgetTab.setCurrentWidget(widget0)
    with qtbot.waitSignal(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(0).widget(0).click()
    with qtbot.assertNotEmitted(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(1).widget(0).click()

    widget1 = dataWidgetTab.widget(1)
    dataWidgetTab.setCurrentWidget(widget1)
    with qtbot.assertNotEmitted(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(0).widget(0).click()
    with qtbot.waitSignal(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(1).widget(0).click()


def test_DataWidgetTab_removeTab(qtbot, dataWidgetTab):
    dataWidgetTab.setCurrentIndex(1)
    oldTab = dataWidgetTab.currentWidget()
    dataWidgetTab.removeTab(1)
    assert dataWidgetTab.currentIndex() == 0
    with qtbot.waitSignal(dataWidgetTab.currentDataValueChanged):
        dataWidgetTab.widget(0).widget(0).click()
    with qtbot.assertNotEmitted(dataWidgetTab.currentDataValueChanged):
        oldTab.widget(0).click()

    oldTab = dataWidgetTab.currentWidget()
    dataWidgetTab.removeTab(0)
    assert dataWidgetTab.currentIndex() == -1
    with qtbot.assertNotEmitted(dataWidgetTab.currentDataValueChanged):
        oldTab.widget(0).click()
