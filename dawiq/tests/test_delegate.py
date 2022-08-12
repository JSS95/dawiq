import dataclasses
from dawiq.datawidget import dataclass2Widget
from dawiq.delegate import convertFromQt, DataclassDelegate
from dawiq.qt_compat import QtGui, QtWidgets


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

    # set widget
    dataWidget.widget(0).setText("1")
    mapper.submit()
    assert model.data(modelIndex) == dict(x=1)
