import dataclasses
from dawiq import dataclass2Widget, MISSING, DataclassStackWidget, DataclassTabWidget
from dawiq.delegate import (
    convertFromQt,
    convertToQt,
    DataclassDelegate,
    DataclassMapper,
)
from dawiq.qt_compat import QtGui, QtWidgets, QtCore
from typing import Tuple
import pytest


def test_convertFromQt():
    class CustomField:
        def __init__(self, x):
            self.x = x

        def __eq__(self, other):
            return type(self) == type(other) and self.x == other.x

    @dataclasses.dataclass
    class Cls0:
        a: CustomField = dataclasses.field(
            metadata=dict(fromQt_converter=lambda arg: CustomField(arg))
        )

    @dataclasses.dataclass
    class Cls1:
        x: int
        y: CustomField = dataclasses.field(
            metadata=dict(fromQt_converter=lambda arg: CustomField(arg))
        )
        z: Cls0

    assert convertFromQt(Cls1, dict(x=1, y=2, z=dict(a=3))) == dict(
        x=1, y=CustomField(2), z=dict(a=CustomField(3))
    )
    assert convertFromQt(Cls1, dict(x=MISSING, y=MISSING, z=MISSING)) == dict()


def test_convertFromQt_defaultvalue():
    """Test that default value is ignored."""

    class CustomField:
        def __init__(self, x):
            self.x = x

        def __eq__(self, other):
            return type(self) == type(other) and self.x == other.x

    @dataclasses.dataclass
    class Cls0:
        x: CustomField = dataclasses.field(
            metadata=dict(fromQt_converter=lambda arg: CustomField(arg))
        )
        y: CustomField = dataclasses.field(
            default=CustomField(0),
            metadata=dict(fromQt_converter=lambda arg: CustomField(arg)),
        )
        z: int = 3

    assert convertFromQt(Cls0, dict(x=3, y=2, z=1)) == dict(
        x=CustomField(3), y=CustomField(2), z=1
    )
    assert convertFromQt(Cls0, dict()) == dict()
    assert convertFromQt(Cls0, dict(x=MISSING, y=MISSING, z=MISSING)) == dict()

    @dataclasses.dataclass
    class Cls1:
        a: Cls0
        b: Cls0 = Cls0(x=CustomField(1))

    assert convertFromQt(
        Cls1, dict(a=dict(x=1, y=2, z=5), b=dict(x=3, y=2, z=1))
    ) == dict(
        a=dict(x=CustomField(1), y=CustomField(2), z=5),
        b=dict(x=CustomField(3), y=CustomField(2), z=1),
    )
    assert convertFromQt(Cls1, dict()) == dict()
    assert convertFromQt(Cls1, dict(a=MISSING, b=MISSING)) == dict()
    assert convertFromQt(
        Cls1, dict(a=MISSING, b=dict(x=MISSING, y=MISSING, z=MISSING))
    ) == dict(b=dict())

    @dataclasses.dataclass
    class Cls2:
        c: Cls1
        d: Cls1 = Cls1(Cls0(CustomField(10)))

    assert convertFromQt(Cls2, dict()) == dict()


def test_convertToQt():
    class CustomField:
        def __init__(self, x):
            self.x = x

        def __eq__(self, other):
            return type(self) == type(other) and self.x == other.x

    @dataclasses.dataclass
    class Cls0:
        a: CustomField = dataclasses.field(
            metadata=dict(toQt_converter=lambda val: val.x)
        )

    @dataclasses.dataclass
    class Cls1:
        x: int
        y: CustomField = dataclasses.field(
            metadata=dict(toQt_converter=lambda val: val.x)
        )
        z: Cls0

    assert convertToQt(
        Cls1, dict(x=1, y=CustomField(2), z=dict(a=CustomField(3)))
    ) == dict(x=1, y=2, z=dict(a=3))
    assert convertToQt(Cls1, dict()) == dict(x=MISSING, y=MISSING, z=MISSING)


def test_convertToQt_defaultvalue():
    """Test that default value is ignored."""

    class CustomField:
        def __init__(self, x):
            self.x = x

        def __eq__(self, other):
            return type(self) == type(other) and self.x == other.x

    @dataclasses.dataclass
    class Cls0:
        x: CustomField = dataclasses.field(
            metadata=dict(toQt_converter=lambda val: val.x)
        )
        y: CustomField = dataclasses.field(
            default=CustomField(0),
            metadata=dict(toQt_converter=lambda val: val.x),
        )
        z: int = 3

    assert convertToQt(Cls0, dict()) == dict(x=MISSING, y=MISSING, z=MISSING)

    @dataclasses.dataclass
    class Cls1:
        a: Cls0
        b: Cls0 = Cls0(x=CustomField(1))

    assert convertToQt(Cls1, dict()) == dict(a=MISSING, b=MISSING)
    assert convertToQt(Cls1, dict(b=dict())) == dict(
        a=MISSING, b=dict(x=MISSING, y=MISSING, z=MISSING)
    )

    @dataclasses.dataclass
    class Cls2:
        c: Cls1
        d: Cls1 = Cls1(Cls0(CustomField(10)))

    assert convertToQt(Cls2, dict()) == dict(c=MISSING, d=MISSING)
    assert convertToQt(Cls2, dict(d=dict())) == dict(
        c=MISSING, d=dict(a=MISSING, b=MISSING)
    )


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


@pytest.fixture
def dataclassTabWidget(qtbot):
    widget = DataclassTabWidget()
    widget.addTab(QtWidgets.QWidget(), "EmptyWidget")
    for dcls in [DataClass1, DataClass2]:
        widget.addDataWidget(dataclass2Widget(dcls), dcls.__name__, dcls)

    return widget


def test_DataclassDelegate_setModelData(qtbot):
    @dataclasses.dataclass
    class Dcls:
        x: int

    delegate = DataclassDelegate()
    model = QtGui.QStandardItemModel()

    item = QtGui.QStandardItem()
    item.setData(Dcls, role=DataclassDelegate.TypeRole)
    model.appendRow(item)

    dataWidget = dataclass2Widget(Dcls)
    mapper = QtWidgets.QDataWidgetMapper()

    mapper.setModel(model)
    mapper.addMapping(dataWidget, 0)
    mapper.setItemDelegate(delegate)

    modelIndex = model.index(0, 0)
    mapper.setCurrentModelIndex(modelIndex)
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) is None

    delegate.commitData.emit(dataWidget)
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) == dict()

    dataWidget.widget(0).setText("0")
    delegate.commitData.emit(dataWidget)
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) == dict(x=0)

    dataWidget.widget(0).setText("1")
    mapper.submit()
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) == dict(x=1)

    dataWidget.dataValueChanged.connect(mapper.submit)
    with qtbot.waitSignal(dataWidget.dataValueChanged):
        dataWidget.widget(0).setText("2")
        qtbot.keyPress(dataWidget.widget(0), QtCore.Qt.Key.Key_Return)
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) == dict(x=2)


def test_DataclassDelegate_setModelData_dataclassStackWidget(
    qtbot, dataclassStackWidget
):
    model = QtGui.QStandardItemModel()
    item = QtGui.QStandardItem()
    item.setData(DataClass1, role=DataclassDelegate.TypeRole)
    model.appendRow(item)

    delegate = DataclassDelegate()
    mapper = QtWidgets.QDataWidgetMapper()
    mapper.setItemDelegate(delegate)
    mapper.setModel(model)
    mapper.addMapping(dataclassStackWidget, 0)

    modelIndex = model.index(0, 0)
    mapper.setCurrentModelIndex(modelIndex)
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) is None

    delegate.commitData.emit(dataclassStackWidget)
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) == dict(x=False)

    dataclassStackWidget.currentWidget().widget(0).click()
    delegate.commitData.emit(dataclassStackWidget)
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) == dict(x=True)

    dataclassStackWidget.currentWidget().widget(0).click()
    mapper.submit()
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) == dict(x=False)

    dataclassStackWidget.currentDataValueChanged.connect(mapper.submit)
    with qtbot.waitSignal(dataclassStackWidget.currentDataValueChanged):
        dataclassStackWidget.currentWidget().widget(0).click()
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) == dict(x=True)

    # data type change
    dataclassStackWidget.setCurrentIndex(0)
    mapper.submit()
    assert model.data(modelIndex, role=DataclassDelegate.TypeRole) is None
    dataclassStackWidget.setCurrentIndex(2)
    mapper.submit()
    assert model.data(modelIndex, role=DataclassDelegate.TypeRole) == DataClass2


def test_DataclassDelegate_setModelData_dataclassTabWidget(qtbot, dataclassTabWidget):
    model = QtGui.QStandardItemModel()
    item = QtGui.QStandardItem()
    item.setData(DataClass1, role=DataclassDelegate.TypeRole)
    model.appendRow(item)

    delegate = DataclassDelegate()
    mapper = QtWidgets.QDataWidgetMapper()
    mapper.setItemDelegate(delegate)
    mapper.setModel(model)
    mapper.addMapping(dataclassTabWidget, 0)

    modelIndex = model.index(0, 0)
    mapper.setCurrentModelIndex(modelIndex)
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) is None

    delegate.commitData.emit(dataclassTabWidget)
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) == dict(x=False)

    dataclassTabWidget.currentWidget().widget(0).click()
    delegate.commitData.emit(dataclassTabWidget)
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) == dict(x=True)

    dataclassTabWidget.currentWidget().widget(0).click()
    mapper.submit()
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) == dict(x=False)

    dataclassTabWidget.currentDataValueChanged.connect(mapper.submit)
    with qtbot.waitSignal(dataclassTabWidget.currentDataValueChanged):
        dataclassTabWidget.currentWidget().widget(0).click()
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) == dict(x=True)

    # data type change
    dataclassTabWidget.setCurrentIndex(0)
    mapper.submit()
    assert model.data(modelIndex, role=DataclassDelegate.TypeRole) is None
    dataclassTabWidget.setCurrentIndex(2)
    mapper.submit()
    assert model.data(modelIndex, role=DataclassDelegate.TypeRole) == DataClass2


def test_DataclassDelegate_setEditorData(qtbot):
    @dataclasses.dataclass
    class Dcls:
        x: int

    delegate = DataclassDelegate()
    model = QtGui.QStandardItemModel()

    for i in range(3):
        item = QtGui.QStandardItem()
        item.setData(Dcls, role=DataclassDelegate.TypeRole)
        model.appendRow(item)

    dataWidget = dataclass2Widget(Dcls)
    mapper = QtWidgets.QDataWidgetMapper()

    mapper.setModel(model)
    mapper.addMapping(dataWidget, 0)
    mapper.setItemDelegate(delegate)

    modelIndex0 = model.index(0, 0)
    model.setData(modelIndex0, dict(x=0), role=DataclassDelegate.DataRole)
    modelIndex1 = model.index(1, 0)
    model.setData(modelIndex1, dict(x=1), role=DataclassDelegate.DataRole)
    modelIndex2 = model.index(2, 0)
    model.setData(modelIndex2, dict(), role=DataclassDelegate.DataRole)

    assert dataWidget.dataValue() == dict(x=MISSING)
    assert dataWidget.widget(0).text() == ""

    mapper.setCurrentModelIndex(modelIndex0)
    assert dataWidget.dataValue() == dict(x=0)
    assert dataWidget.widget(0).text() == "0"

    mapper.setCurrentModelIndex(modelIndex1)
    assert dataWidget.dataValue() == dict(x=1)
    assert dataWidget.widget(0).text() == "1"

    mapper.setCurrentModelIndex(modelIndex2)
    assert dataWidget.dataValue() == dict(x=MISSING)
    assert dataWidget.widget(0).text() == ""

    model.setData(modelIndex2, dict(x=10), role=DataclassDelegate.DataRole)
    assert dataWidget.dataValue() == dict(x=10)
    assert dataWidget.widget(0).text() == "10"


def test_DataclassDelegate_setEditorData_dataclassStackWidget(
    qtbot, dataclassStackWidget
):
    model = QtGui.QStandardItemModel()
    for dcls in [DataClass1, DataClass2]:
        item = QtGui.QStandardItem()
        item.setData(dcls, role=DataclassDelegate.TypeRole)
        model.appendRow(item)

    delegate = DataclassDelegate()
    mapper = QtWidgets.QDataWidgetMapper()
    mapper.setItemDelegate(delegate)
    mapper.setModel(model)
    mapper.addMapping(dataclassStackWidget, 0)

    modelIndex0 = model.index(0, 0)
    model.setData(modelIndex0, dict(x=True), role=DataclassDelegate.DataRole)
    modelIndex1 = model.index(1, 0)
    model.setData(modelIndex1, dict(a=True, b=True), role=DataclassDelegate.DataRole)

    mapper.setCurrentModelIndex(modelIndex0)
    assert dataclassStackWidget.currentIndex() == 1
    assert dataclassStackWidget.currentWidget().dataValue() == dict(x=True)

    mapper.setCurrentModelIndex(modelIndex1)
    assert dataclassStackWidget.currentIndex() == 2
    assert dataclassStackWidget.currentWidget().dataValue() == dict(
        a=True, b=True, c=False, d=False, e=False
    )

    model.setData(modelIndex1, dict(a=True), role=DataclassDelegate.DataRole)
    assert dataclassStackWidget.currentWidget().dataValue() == dict(
        a=True, b=False, c=False, d=False, e=False
    )


def test_DataclassDelegate_setEditorData_dataclassTabWidget(qtbot, dataclassTabWidget):
    model = QtGui.QStandardItemModel()
    for dcls in [DataClass1, DataClass2]:
        item = QtGui.QStandardItem()
        item.setData(dcls, role=DataclassDelegate.TypeRole)
        model.appendRow(item)

    delegate = DataclassDelegate()
    mapper = QtWidgets.QDataWidgetMapper()
    mapper.setItemDelegate(delegate)
    mapper.setModel(model)
    mapper.addMapping(dataclassTabWidget, 0)

    modelIndex0 = model.index(0, 0)
    model.setData(modelIndex0, dict(x=True), role=DataclassDelegate.DataRole)
    modelIndex1 = model.index(1, 0)
    model.setData(modelIndex1, dict(a=True, b=True), role=DataclassDelegate.DataRole)

    mapper.setCurrentModelIndex(modelIndex0)
    assert dataclassTabWidget.currentIndex() == 1
    assert dataclassTabWidget.currentWidget().dataValue() == dict(x=True)

    mapper.setCurrentModelIndex(modelIndex1)
    assert dataclassTabWidget.currentIndex() == 2
    assert dataclassTabWidget.currentWidget().dataValue() == dict(
        a=True, b=True, c=False, d=False, e=False
    )

    model.setData(modelIndex1, dict(a=True), role=DataclassDelegate.DataRole)
    assert dataclassTabWidget.currentWidget().dataValue() == dict(
        a=True, b=False, c=False, d=False, e=False
    )


def test_DataclassMapper_addMapping_dataWidget(qtbot):
    @dataclasses.dataclass
    class Dcls:
        x: int
        y: bool

    delegate = DataclassDelegate()
    model = QtGui.QStandardItemModel()

    item = QtGui.QStandardItem()
    item.setData(Dcls, role=DataclassDelegate.TypeRole)
    model.appendRow(item)

    dataWidget = dataclass2Widget(Dcls)
    mapper = DataclassMapper()

    mapper.setModel(model)
    mapper.addMapping(dataWidget, 0)
    mapper.setItemDelegate(delegate)

    modelIndex = model.index(0, 0)
    mapper.setCurrentModelIndex(modelIndex)
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) is None  # IMPORTANT!

    dataWidget.widget(0).setText("0")
    qtbot.keyPress(dataWidget.widget(0), QtCore.Qt.Key.Key_Return)
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) == dict(x=0, y=False)

    dataWidget.widget(1).click()
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) == dict(x=0, y=True)


def test_DataclassMapper_addMapping_dataclassStackWidget(qtbot, dataclassStackWidget):
    model = QtGui.QStandardItemModel()
    item = QtGui.QStandardItem()
    item.setData(DataClass1, role=DataclassDelegate.TypeRole)
    model.appendRow(item)

    delegate = DataclassDelegate()
    mapper = DataclassMapper()
    mapper.setItemDelegate(delegate)
    mapper.setModel(model)
    mapper.addMapping(dataclassStackWidget, 0)

    modelIndex = model.index(0, 0)
    mapper.setCurrentModelIndex(modelIndex)
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) is None

    dataclassStackWidget.currentWidget().widget(0).click()
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) == dict(x=True)

    # data type change
    dataclassStackWidget.setCurrentIndex(0)
    assert model.data(modelIndex, role=DataclassDelegate.TypeRole) is None
    dataclassStackWidget.setCurrentIndex(2)
    assert model.data(modelIndex, role=DataclassDelegate.TypeRole) == DataClass2


def test_DataclassMapper_addMapping_dataclassTabWidget(qtbot, dataclassTabWidget):
    model = QtGui.QStandardItemModel()
    item = QtGui.QStandardItem()
    item.setData(DataClass1, role=DataclassDelegate.TypeRole)
    model.appendRow(item)

    delegate = DataclassDelegate()
    mapper = DataclassMapper()
    mapper.setItemDelegate(delegate)
    mapper.setModel(model)
    mapper.addMapping(dataclassTabWidget, 0)

    modelIndex = model.index(0, 0)
    mapper.setCurrentModelIndex(modelIndex)
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) is None

    dataclassTabWidget.currentWidget().widget(0).click()
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) == dict(x=True)

    # data type change
    dataclassTabWidget.setCurrentIndex(0)
    assert model.data(modelIndex, role=DataclassDelegate.TypeRole) is None
    dataclassTabWidget.setCurrentIndex(2)
    assert model.data(modelIndex, role=DataclassDelegate.TypeRole) == DataClass2


def test_DataclassMapper_removeMapping_dataWidget(qtbot):
    @dataclasses.dataclass
    class Dcls:
        x: int
        y: bool

    delegate = DataclassDelegate()
    model = QtGui.QStandardItemModel()

    item = QtGui.QStandardItem()
    item.setData(Dcls, role=DataclassDelegate.TypeRole)
    model.appendRow(item)

    dataWidget = dataclass2Widget(Dcls)
    mapper = DataclassMapper()

    mapper.setModel(model)
    mapper.addMapping(dataWidget, 0)
    mapper.setItemDelegate(delegate)

    mapper.removeMapping(dataWidget)

    modelIndex = model.index(0, 0)
    mapper.setCurrentModelIndex(modelIndex)
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) is None

    dataWidget.widget(0).setText("0")
    qtbot.keyPress(dataWidget.widget(0), QtCore.Qt.Key.Key_Return)
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) is None

    dataWidget.widget(1).click()
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) is None


def test_DataclassMapper_removeMapping_dataclassStackWidget(
    qtbot, dataclassStackWidget
):
    model = QtGui.QStandardItemModel()
    item = QtGui.QStandardItem()
    item.setData(DataClass1, role=DataclassDelegate.TypeRole)
    model.appendRow(item)

    delegate = DataclassDelegate()
    mapper = DataclassMapper()
    mapper.setItemDelegate(delegate)
    mapper.setModel(model)
    mapper.addMapping(dataclassStackWidget, 0)

    modelIndex = model.index(0, 0)
    mapper.setCurrentModelIndex(modelIndex)

    mapper.removeMapping(dataclassStackWidget)

    dataclassStackWidget.currentWidget().widget(0).click()
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) is None

    # data type change
    dataclassStackWidget.setCurrentIndex(0)
    assert model.data(modelIndex, role=DataclassDelegate.TypeRole) == DataClass1
    dataclassStackWidget.setCurrentIndex(2)
    assert model.data(modelIndex, role=DataclassDelegate.TypeRole) == DataClass1


def test_DataclassMapper_removeMapping_dataclassTabWidget(qtbot, dataclassTabWidget):
    model = QtGui.QStandardItemModel()
    item = QtGui.QStandardItem()
    item.setData(DataClass1, role=DataclassDelegate.TypeRole)
    model.appendRow(item)

    delegate = DataclassDelegate()
    mapper = DataclassMapper()
    mapper.setItemDelegate(delegate)
    mapper.setModel(model)
    mapper.addMapping(dataclassTabWidget, 0)

    modelIndex = model.index(0, 0)
    mapper.setCurrentModelIndex(modelIndex)

    mapper.removeMapping(dataclassTabWidget)

    dataclassTabWidget.currentWidget().widget(0).click()
    assert model.data(modelIndex, role=DataclassDelegate.DataRole) is None

    # data type change
    dataclassTabWidget.setCurrentIndex(0)
    assert model.data(modelIndex, role=DataclassDelegate.TypeRole) == DataClass1
    dataclassTabWidget.setCurrentIndex(2)
    assert model.data(modelIndex, role=DataclassDelegate.TypeRole) == DataClass1


def test_DataclassMapper_Tuple_setCurrentIndex_crash(qtbot):
    """Test that setting index to nested widget does not cause infinite loop."""

    @dataclasses.dataclass
    class DataClass:
        x: Tuple[int]

    delegate = DataclassDelegate()
    model = QtGui.QStandardItemModel()

    item = QtGui.QStandardItem()
    item.setData(DataClass, role=DataclassDelegate.TypeRole)
    model.appendRow(item)

    dataWidget = dataclass2Widget(DataClass)
    mapper = DataclassMapper()

    mapper.setModel(model)
    mapper.addMapping(dataWidget, 0)
    mapper.setItemDelegate(delegate)

    mapper.setCurrentIndex(0)  # must not crash


def test_DataclassMapper_default(qtbot):
    """Test that default value of dataclass is not applied to widget & model."""

    @dataclasses.dataclass
    class DataClass:
        x: int = 3

    delegate = DataclassDelegate()
    model = QtGui.QStandardItemModel()

    item = QtGui.QStandardItem()
    item.setData(DataClass, role=DataclassDelegate.TypeRole)
    model.appendRow(item)

    dataWidget = dataclass2Widget(DataClass)
    mapper = DataclassMapper()

    mapper.setModel(model)
    mapper.addMapping(dataWidget, 0)
    mapper.setItemDelegate(delegate)

    modelIndex = model.index(0, 0)
    mapper.setCurrentModelIndex(modelIndex)

    assert model.data(modelIndex, role=DataclassDelegate.DataRole) is None
    assert dataWidget.dataValue() == dict(x=MISSING)
