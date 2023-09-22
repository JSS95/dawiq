from dawiq import DataclassStackedWidget, DataclassTabWidget, dataclass2Widget
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
def dataclassStackedWidget(qtbot):
    widget = DataclassStackedWidget()
    widget.addWidget(QtWidgets.QWidget())
    widget.addDataWidget(dataclass2Widget(DataClass1), DataClass1)
    widget.insertDataWidget(1, dataclass2Widget(DataClass2), DataClass2)
    return widget


def test_DataclassStackedWidget_currentDataclass(qtbot, dataclassStackedWidget):
    dataclassStackedWidget.setCurrentIndex(0)
    assert dataclassStackedWidget.currentDataclass() is None
    dataclassStackedWidget.setCurrentIndex(1)
    assert dataclassStackedWidget.currentDataclass() == DataClass2
    dataclassStackedWidget.setCurrentIndex(2)
    assert dataclassStackedWidget.currentDataclass() == DataClass1


def test_DataclassStackedWidget_indexOfDataclass(qtbot, dataclassStackedWidget):
    assert dataclassStackedWidget.indexOfDataclass(DataClass1) == 2
    assert dataclassStackedWidget.indexOfDataclass(DataClass2) == 1
    assert dataclassStackedWidget.indexOfDataclass(DataClass3) == -1


def test_DataclassStackedWidget_currentDataValueChanged(qtbot, dataclassStackedWidget):
    dataclassStackedWidget.setCurrentIndex(0)
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataValueChanged):
        dataclassStackedWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataValueChanged):
        dataclassStackedWidget.widget(2).widget(0).click()

    dataclassStackedWidget.setCurrentIndex(1)
    with qtbot.waitSignal(dataclassStackedWidget.currentDataValueChanged):
        dataclassStackedWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataValueChanged):
        dataclassStackedWidget.widget(2).widget(0).click()

    dataclassStackedWidget.setCurrentIndex(2)
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataValueChanged):
        dataclassStackedWidget.widget(1).widget(0).click()
    with qtbot.waitSignal(dataclassStackedWidget.currentDataValueChanged):
        dataclassStackedWidget.widget(2).widget(0).click()

    dataclassStackedWidget.setCurrentWidget(dataclassStackedWidget.widget(0))
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataValueChanged):
        dataclassStackedWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataValueChanged):
        dataclassStackedWidget.widget(2).widget(0).click()

    dataclassStackedWidget.setCurrentWidget(dataclassStackedWidget.widget(1))
    with qtbot.waitSignal(dataclassStackedWidget.currentDataValueChanged):
        dataclassStackedWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataValueChanged):
        dataclassStackedWidget.widget(2).widget(0).click()

    dataclassStackedWidget.setCurrentWidget(dataclassStackedWidget.widget(2))
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataValueChanged):
        dataclassStackedWidget.widget(1).widget(0).click()
    with qtbot.waitSignal(dataclassStackedWidget.currentDataValueChanged):
        dataclassStackedWidget.widget(2).widget(0).click()


def test_DataclassStackedWidget_currentDataEdited(qtbot, dataclassStackedWidget):
    dataclassStackedWidget.setCurrentIndex(0)
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataEdited):
        dataclassStackedWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataEdited):
        dataclassStackedWidget.widget(2).widget(0).click()

    dataclassStackedWidget.setCurrentIndex(1)
    with qtbot.waitSignal(dataclassStackedWidget.currentDataEdited):
        dataclassStackedWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataEdited):
        dataclassStackedWidget.widget(2).widget(0).click()

    dataclassStackedWidget.setCurrentIndex(2)
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataEdited):
        dataclassStackedWidget.widget(1).widget(0).click()
    with qtbot.waitSignal(dataclassStackedWidget.currentDataEdited):
        dataclassStackedWidget.widget(2).widget(0).click()

    dataclassStackedWidget.setCurrentWidget(dataclassStackedWidget.widget(0))
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataEdited):
        dataclassStackedWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataEdited):
        dataclassStackedWidget.widget(2).widget(0).click()

    dataclassStackedWidget.setCurrentWidget(dataclassStackedWidget.widget(1))
    with qtbot.waitSignal(dataclassStackedWidget.currentDataEdited):
        dataclassStackedWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataEdited):
        dataclassStackedWidget.widget(2).widget(0).click()

    dataclassStackedWidget.setCurrentWidget(dataclassStackedWidget.widget(2))
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataEdited):
        dataclassStackedWidget.widget(1).widget(0).click()
    with qtbot.waitSignal(dataclassStackedWidget.currentDataEdited):
        dataclassStackedWidget.widget(2).widget(0).click()


def test_DataclassStackedWidget_removeWidget(qtbot, dataclassStackedWidget):
    dataclassStackedWidget.setCurrentIndex(2)
    oldWidget = dataclassStackedWidget.currentWidget()
    dataclassStackedWidget.removeWidget(oldWidget)
    assert dataclassStackedWidget.indexOfDataclass(DataClass2) == 1
    assert dataclassStackedWidget.currentIndex() == 1
    with qtbot.waitSignals(
        [
            dataclassStackedWidget.currentDataValueChanged,
            dataclassStackedWidget.currentDataEdited,
        ]
    ):
        dataclassStackedWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataValueChanged):
        oldWidget.widget(0).click()
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataEdited):
        oldWidget.widget(0).click()

    oldWidget = dataclassStackedWidget.currentWidget()
    dataclassStackedWidget.removeWidget(oldWidget)
    assert dataclassStackedWidget.indexOfDataclass(DataClass1) == -1
    assert dataclassStackedWidget.currentIndex() == 0
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataValueChanged):
        oldWidget.widget(0).click()
    with qtbot.assertNotEmitted(dataclassStackedWidget.currentDataEdited):
        oldWidget.widget(0).click()

    oldWidget = dataclassStackedWidget.currentWidget()
    dataclassStackedWidget.removeWidget(oldWidget)
    assert dataclassStackedWidget.currentIndex() == -1


@pytest.fixture
def dataclassTabWidget(qtbot):
    widget = DataclassTabWidget()
    widget.addTab(QtWidgets.QWidget(), "EmptyTab")
    widget.addDataWidget(dataclass2Widget(DataClass1), DataClass1, DataClass1.__name__)
    widget.insertDataWidget(
        1, dataclass2Widget(DataClass2), DataClass2, DataClass2.__name__
    )
    return widget


def test_DataclassTabWidget_currentDataclass(qtbot, dataclassTabWidget):
    dataclassTabWidget.setCurrentIndex(0)
    assert dataclassTabWidget.currentDataclass() is None
    dataclassTabWidget.setCurrentIndex(1)
    assert dataclassTabWidget.currentDataclass() == DataClass2
    dataclassTabWidget.setCurrentIndex(2)
    assert dataclassTabWidget.currentDataclass() == DataClass1


def test_DataclassTabWidget_indexOfDataclass(qtbot, dataclassTabWidget):
    assert dataclassTabWidget.indexOfDataclass(DataClass1) == 2
    assert dataclassTabWidget.indexOfDataclass(DataClass2) == 1
    assert dataclassTabWidget.indexOfDataclass(DataClass3) == -1


def test_DataclassTabWidget_currentDataValueChanged(qtbot, dataclassTabWidget):
    dataclassTabWidget.setCurrentIndex(0)
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataValueChanged):
        dataclassTabWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataValueChanged):
        dataclassTabWidget.widget(2).widget(0).click()

    dataclassTabWidget.setCurrentIndex(1)
    with qtbot.waitSignal(dataclassTabWidget.currentDataValueChanged):
        dataclassTabWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataValueChanged):
        dataclassTabWidget.widget(2).widget(0).click()

    dataclassTabWidget.setCurrentIndex(2)
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataValueChanged):
        dataclassTabWidget.widget(1).widget(0).click()
    with qtbot.waitSignal(dataclassTabWidget.currentDataValueChanged):
        dataclassTabWidget.widget(2).widget(0).click()

    dataclassTabWidget.setCurrentWidget(dataclassTabWidget.widget(0))
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataValueChanged):
        dataclassTabWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataValueChanged):
        dataclassTabWidget.widget(2).widget(0).click()

    dataclassTabWidget.setCurrentWidget(dataclassTabWidget.widget(1))
    with qtbot.waitSignal(dataclassTabWidget.currentDataValueChanged):
        dataclassTabWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataValueChanged):
        dataclassTabWidget.widget(2).widget(0).click()

    dataclassTabWidget.setCurrentWidget(dataclassTabWidget.widget(2))
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataValueChanged):
        dataclassTabWidget.widget(1).widget(0).click()
    with qtbot.waitSignal(dataclassTabWidget.currentDataValueChanged):
        dataclassTabWidget.widget(2).widget(0).click()


def test_DataclassTabWidget_currentDataEdited(qtbot, dataclassTabWidget):
    dataclassTabWidget.setCurrentIndex(0)
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataEdited):
        dataclassTabWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataEdited):
        dataclassTabWidget.widget(2).widget(0).click()

    dataclassTabWidget.setCurrentIndex(1)
    with qtbot.waitSignal(dataclassTabWidget.currentDataEdited):
        dataclassTabWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataEdited):
        dataclassTabWidget.widget(2).widget(0).click()

    dataclassTabWidget.setCurrentIndex(2)
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataEdited):
        dataclassTabWidget.widget(1).widget(0).click()
    with qtbot.waitSignal(dataclassTabWidget.currentDataEdited):
        dataclassTabWidget.widget(2).widget(0).click()

    dataclassTabWidget.setCurrentWidget(dataclassTabWidget.widget(0))
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataEdited):
        dataclassTabWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataEdited):
        dataclassTabWidget.widget(2).widget(0).click()

    dataclassTabWidget.setCurrentWidget(dataclassTabWidget.widget(1))
    with qtbot.waitSignal(dataclassTabWidget.currentDataEdited):
        dataclassTabWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataEdited):
        dataclassTabWidget.widget(2).widget(0).click()

    dataclassTabWidget.setCurrentWidget(dataclassTabWidget.widget(2))
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataEdited):
        dataclassTabWidget.widget(1).widget(0).click()
    with qtbot.waitSignal(dataclassTabWidget.currentDataEdited):
        dataclassTabWidget.widget(2).widget(0).click()


def test_DataclassTabWidget_removeTab(qtbot, dataclassTabWidget):
    dataclassTabWidget.setCurrentIndex(2)
    oldTab = dataclassTabWidget.currentWidget()
    dataclassTabWidget.removeTab(dataclassTabWidget.indexOf(oldTab))
    assert dataclassTabWidget.currentIndex() == 1
    with qtbot.waitSignals(
        [
            dataclassTabWidget.currentDataValueChanged,
            dataclassTabWidget.currentDataEdited,
        ]
    ):
        dataclassTabWidget.widget(1).widget(0).click()
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataValueChanged):
        oldTab.widget(0).click()
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataEdited):
        oldTab.widget(0).click()

    oldTab = dataclassTabWidget.currentWidget()
    dataclassTabWidget.removeTab(dataclassTabWidget.indexOf(oldTab))
    assert dataclassTabWidget.currentIndex() == 0
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataValueChanged):
        oldTab.widget(0).click()
    with qtbot.assertNotEmitted(dataclassTabWidget.currentDataEdited):
        oldTab.widget(0).click()

    oldTab = dataclassTabWidget.currentWidget()
    dataclassTabWidget.removeTab(dataclassTabWidget.indexOf(oldTab))
    assert dataclassTabWidget.currentIndex() == -1
