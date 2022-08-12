import dataclasses
from dawiq import dataclass2Widget, MISSING
from dawiq.delegate import (
    convertFromQt,
    convertToQt,
    DataclassDelegate,
    DataclassMapper,
)
from dawiq.qt_compat import QtGui, QtWidgets, QtCore


def test_convertFromQt():
    class CustomField:
        def __init__(self, a, b):
            self.a = a
            self.b = b

        def __eq__(self, other):
            return type(self) == type(other) and (self.a, self.b) == (other.a, other.b)

    @dataclasses.dataclass
    class Cls0:
        a: CustomField = dataclasses.field(
            metadata=dict(fromQt_converter=lambda args: CustomField(*args))
        )

    @dataclasses.dataclass
    class Cls1:
        x: int
        y: CustomField = dataclasses.field(
            metadata=dict(fromQt_converter=lambda args: CustomField(*args))
        )
        z: Cls0

    assert convertFromQt(Cls1, dict(x=1, y=(2, 3), z=dict(a=(3, 4)))) == dict(
        x=1, y=CustomField(2, 3), z=dict(a=CustomField(3, 4))
    )
    assert convertFromQt(Cls1, dict(x=MISSING, y=MISSING, z=MISSING)) == dict()


def test_convertToQt():
    class CustomField:
        def __init__(self, a):
            self.a = a

        def __eq__(self, other):
            return type(self) == type(other) and (self.a,) == (other.a,)

    @dataclasses.dataclass
    class Cls0:
        a: CustomField = dataclasses.field(metadata=dict(toQt_converter=lambda x: x.a))

    @dataclasses.dataclass
    class Cls1:
        x: int
        y: CustomField = dataclasses.field(metadata=dict(toQt_converter=lambda x: x.a))
        z: Cls0

    assert convertToQt(
        Cls1, dict(x=1, y=CustomField(2), z=dict(a=CustomField(3)))
    ) == dict(x=1, y=2, z=dict(a=3))
    assert convertToQt(Cls1, dict()) == dict(x=MISSING, y=MISSING, z=MISSING)


def test_DataclassDelegate_setModelData(qtbot):
    @dataclasses.dataclass
    class Dcls:
        x: int

    dataWidget = dataclass2Widget(Dcls)
    model = QtGui.QStandardItemModel()
    model.appendRow(QtGui.QStandardItem())
    mapper = QtWidgets.QDataWidgetMapper()
    delegate = DataclassDelegate()
    delegate.setDataclassType(Dcls)

    mapper.setModel(model)
    mapper.addMapping(dataWidget, 0)
    mapper.setItemDelegate(delegate)

    modelIndex = model.index(0, 0)
    mapper.setCurrentModelIndex(modelIndex)
    assert model.data(modelIndex) is None

    dataWidget.widget(0).setText("0")
    delegate.commitData.emit(dataWidget)
    assert model.data(modelIndex) == dict(x=0)

    dataWidget.widget(0).setText("1")
    mapper.submit()
    assert model.data(modelIndex) == dict(x=1)

    dataWidget.dataValueChanged.connect(mapper.submit)
    with qtbot.waitSignal(dataWidget.dataValueChanged):
        dataWidget.widget(0).setText("2")
        qtbot.keyPress(dataWidget.widget(0), QtCore.Qt.Key.Key_Return)
    assert model.data(modelIndex) == dict(x=2)


def test_DataclassMapper_addMapping(qtbot):
    @dataclasses.dataclass
    class Dcls:
        x: int
        y: bool

    dataWidget = dataclass2Widget(Dcls)
    model = QtGui.QStandardItemModel()
    model.appendRow(QtGui.QStandardItem())
    mapper = DataclassMapper()
    delegate = DataclassDelegate()
    delegate.setDataclassType(Dcls)

    mapper.setModel(model)
    mapper.addMapping(dataWidget, 0)
    mapper.setItemDelegate(delegate)

    modelIndex = model.index(0, 0)
    mapper.setCurrentModelIndex(modelIndex)
    assert model.data(modelIndex) is None

    dataWidget.widget(0).setText("0")
    qtbot.keyPress(dataWidget.widget(0), QtCore.Qt.Key.Key_Return)
    assert model.data(modelIndex) == dict(x=0, y=False)

    dataWidget.widget(1).click()
    assert model.data(modelIndex) == dict(x=0, y=True)


def test_DataclassMapper_removeMapping(qtbot):
    @dataclasses.dataclass
    class Dcls:
        x: int
        y: bool

    dataWidget = dataclass2Widget(Dcls)
    model = QtGui.QStandardItemModel()
    model.appendRow(QtGui.QStandardItem())
    mapper = DataclassMapper()
    delegate = DataclassDelegate()
    delegate.setDataclassType(Dcls)

    mapper.setModel(model)
    mapper.addMapping(dataWidget, 0)
    mapper.setItemDelegate(delegate)

    mapper.removeMapping(dataWidget)

    modelIndex = model.index(0, 0)
    mapper.setCurrentModelIndex(modelIndex)
    assert model.data(modelIndex) is None

    dataWidget.widget(0).setText("0")
    qtbot.keyPress(dataWidget.widget(0), QtCore.Qt.Key.Key_Return)
    assert model.data(modelIndex) is None

    dataWidget.widget(1).click()
    assert model.data(modelIndex) is None


def test_DataclassMapper_clearMapping(qtbot):
    @dataclasses.dataclass
    class Dcls:
        x: int
        y: bool

    dataWidget = dataclass2Widget(Dcls)
    model = QtGui.QStandardItemModel()
    model.appendRow(QtGui.QStandardItem())
    mapper = DataclassMapper()
    delegate = DataclassDelegate()
    delegate.setDataclassType(Dcls)

    mapper.setModel(model)
    mapper.addMapping(dataWidget, 0)
    mapper.setItemDelegate(delegate)

    mapper.clearMapping()

    modelIndex = model.index(0, 0)
    mapper.setCurrentModelIndex(modelIndex)
    assert model.data(modelIndex) is None

    dataWidget.widget(0).setText("0")
    qtbot.keyPress(dataWidget.widget(0), QtCore.Qt.Key.Key_Return)
    assert model.data(modelIndex) is None

    dataWidget.widget(1).click()
    assert model.data(modelIndex) is None
