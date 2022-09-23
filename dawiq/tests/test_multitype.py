from dawiq import DataWidgetStack, dataclass2Widget
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
