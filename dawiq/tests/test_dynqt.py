def test_import_QtCore():
    from dawiq.dynqt import QtCore

    assert hasattr(QtCore, "Qt")
    assert hasattr(QtCore, "Signal")
    assert hasattr(QtCore, "Slot")


def test_import_QtWidgets():
    from dawiq.dynqt import QtWidgets

    assert hasattr(QtWidgets, "QWidget")
