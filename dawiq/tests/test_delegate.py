import dataclasses
from dawiq import dataclass2Widget, MISSING
from dawiq.delegate import (
    convertFromQt,
    convertToQt,
    DataclassDelegate,
    DataclassMapper,
)
from dawiq.qt_compat import QtGui, QtWidgets, QtCore
from typing import Tuple


def test_convertFromQt():
    class CustomField:
        def __init__(self, x):
            self.x = x

        def __eq__(self, other):
            return type(self) == type(other) and self.x == other.x

    def converter(arg):
        if isinstance(arg, CustomField):
            return arg
        return CustomField(arg)

    @dataclasses.dataclass
    class Cls0:
        a: CustomField = dataclasses.field(metadata=dict(fromQt_converter=converter))

    @dataclasses.dataclass
    class Cls1:
        x: int
        y: CustomField = dataclasses.field(metadata=dict(fromQt_converter=converter))
        z: Cls0

    assert convertFromQt(Cls1, dict(x=1, y=2, z=dict(a=3))) == dict(
        x=1, y=CustomField(2), z=dict(a=CustomField(3))
    )
    assert convertFromQt(Cls1, dict(x=MISSING, y=MISSING, z=MISSING)) == dict()


def test_convertFromQt_defaultvalue():
    class CustomField:
        def __init__(self, x):
            self.x = x

        def __eq__(self, other):
            return type(self) == type(other) and self.x == other.x

    def converter(arg):
        if isinstance(arg, CustomField):
            return arg
        return CustomField(arg)

    @dataclasses.dataclass
    class Cls0:
        x: CustomField = dataclasses.field(metadata=dict(fromQt_converter=converter))
        y: CustomField = dataclasses.field(
            default=CustomField(0),
            metadata=dict(fromQt_converter=converter),
        )
        z: int = 3

    assert convertFromQt(Cls0, dict(x=3, y=2, z=1)) == dict(
        x=CustomField(3), y=CustomField(2), z=1
    )
    assert convertFromQt(Cls0, dict()) == dict(y=CustomField(0), z=3)

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
    assert convertFromQt(Cls1, dict()) == dict(
        b=dict(x=CustomField(1), y=CustomField(0), z=3)
    )

    @dataclasses.dataclass
    class Cls2:
        c: Cls1
        d: Cls1 = Cls1(Cls0(CustomField(10)))

    assert convertFromQt(Cls2, dict()) == dict(
        d=dict(
            a=dict(x=CustomField(10), y=CustomField(0), z=3),
            b=dict(x=CustomField(1), y=CustomField(0), z=3),
        )
    )


def test_convertToQt():
    class CustomField:
        def __init__(self, x):
            self.x = x

        def __eq__(self, other):
            return type(self) == type(other) and self.x == other.x

    def converter(val):
        return val.x

    @dataclasses.dataclass
    class Cls0:
        a: CustomField = dataclasses.field(metadata=dict(toQt_converter=converter))

    @dataclasses.dataclass
    class Cls1:
        x: int
        y: CustomField = dataclasses.field(metadata=dict(toQt_converter=converter))
        z: Cls0

    assert convertToQt(
        Cls1, dict(x=1, y=CustomField(2), z=dict(a=CustomField(3)))
    ) == dict(x=1, y=2, z=dict(a=3))
    assert convertToQt(Cls1, dict()) == dict(x=MISSING, y=MISSING, z=MISSING)


def test_convertToQt_defaultvalue():
    class CustomField:
        def __init__(self, x):
            self.x = x

        def __eq__(self, other):
            return type(self) == type(other) and self.x == other.x

    def converter(val):
        return val.x

    @dataclasses.dataclass
    class Cls0:
        x: CustomField = dataclasses.field(metadata=dict(toQt_converter=converter))
        y: CustomField = dataclasses.field(
            default=CustomField(0),
            metadata=dict(toQt_converter=converter),
        )
        z: int = 3

    assert convertToQt(Cls0, dict(x=CustomField(3), y=CustomField(2), z=1)) == dict(
        x=3, y=2, z=1
    )
    assert convertToQt(Cls0, dict(y=CustomField(0), z=3)) == dict(x=MISSING, y=0, z=3)

    @dataclasses.dataclass
    class Cls1:
        a: Cls0
        b: Cls0 = Cls0(x=CustomField(1))

    assert convertToQt(
        Cls1,
        dict(
            a=dict(x=CustomField(1), y=CustomField(2), z=5),
            b=dict(x=CustomField(3), y=CustomField(2), z=1),
        ),
    ) == dict(a=dict(x=1, y=2, z=5), b=dict(x=3, y=2, z=1))
    assert convertToQt(
        Cls1, dict(b=dict(x=CustomField(1), y=CustomField(0), z=3))
    ) == dict(a=MISSING, b=dict(x=1, y=0, z=3))

    @dataclasses.dataclass
    class Cls2:
        c: Cls1
        d: Cls1 = Cls1(Cls0(CustomField(10)))

    assert convertToQt(
        Cls2,
        dict(
            d=dict(
                a=dict(x=CustomField(10), y=CustomField(0), z=3),
                b=dict(x=CustomField(1), y=CustomField(0), z=3),
            )
        ),
    ) == dict(c=MISSING, d=dict(a=dict(x=10, y=0, z=3), b=dict(x=1, y=0, z=3)))


def test_DataclassDelegate_setModelData(qtbot):
    model = QtGui.QStandardItemModel()
    model.appendRow(QtGui.QStandardItem())

    @dataclasses.dataclass
    class Dcls:
        x: int

    dataWidget = dataclass2Widget(Dcls)
    mapper = QtWidgets.QDataWidgetMapper()
    delegate = DataclassDelegate()
    delegate.setDataclassType(Dcls)

    mapper.setModel(model)
    mapper.addMapping(dataWidget, 0)
    mapper.setItemDelegate(delegate)

    modelIndex = model.index(0, 0)
    mapper.setCurrentModelIndex(modelIndex)
    assert model.data(modelIndex) is None

    delegate.commitData.emit(dataWidget)
    assert model.data(modelIndex) == dict()

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


def test_DataclassDelegate_setEditorData(qtbot):
    model = QtGui.QStandardItemModel()
    for i in range(3):
        model.appendRow(QtGui.QStandardItem())

    @dataclasses.dataclass
    class Dcls:
        x: int

    dataWidget = dataclass2Widget(Dcls)
    mapper = QtWidgets.QDataWidgetMapper()
    delegate = DataclassDelegate()
    delegate.setDataclassType(Dcls)

    mapper.setModel(model)
    mapper.addMapping(dataWidget, 0)
    mapper.setItemDelegate(delegate)

    modelIndex0 = model.index(0, 0)
    model.setData(modelIndex0, dict(x=0))
    modelIndex1 = model.index(1, 0)
    model.setData(modelIndex1, dict(x=1))
    modelIndex2 = model.index(2, 0)
    model.setData(modelIndex2, dict())

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

    model.setData(modelIndex2, dict(x=10))
    assert dataWidget.dataValue() == dict(x=10)
    assert dataWidget.widget(0).text() == "10"


def test_DataclassMapper_addMapping(qtbot):
    model = QtGui.QStandardItemModel()
    model.appendRow(QtGui.QStandardItem())

    @dataclasses.dataclass
    class Dcls:
        x: int
        y: bool

    dataWidget = dataclass2Widget(Dcls)
    mapper = DataclassMapper()
    delegate = DataclassDelegate()
    delegate.setDataclassType(Dcls)

    mapper.setModel(model)
    mapper.addMapping(dataWidget, 0)
    mapper.setItemDelegate(delegate)

    modelIndex = model.index(0, 0)
    mapper.setCurrentModelIndex(modelIndex)
    # assert model.data(modelIndex) == dict(y=False)

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


def test_DataclassMapper_Tuple_setCurrentIndex_crash(qtbot):
    """Test that setting index to nested widget does not cause infinite loop."""
    @dataclasses.dataclass
    class DataClass:
        x: Tuple[int]

    delegate = DataclassDelegate()
    delegate.setDataclassType(DataClass)
    mapper = DataclassMapper()
    mapper.setItemDelegate(delegate)

    model = QtGui.QStandardItemModel()
    model.appendRow(QtGui.QStandardItem())
    mapper.setModel(model)

    dataWidget = dataclass2Widget(DataClass)
    mapper.addMapping(dataWidget, 0)
    mapper.setCurrentIndex(0)
