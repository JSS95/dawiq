from typing import Protocol, Dict, Any


__all__ = ["DataclassProtocol", "DataWidgetProtocol"]


class DataclassProtocol(Protocol):
    """Type annotation for dataclass type object."""

    # https://stackoverflow.com/a/55240861/11501976
    __dataclass_fields__: Dict


class DataWidgetProtocol(Protocol):
    """Type annotation for data widget object."""

    def dataValue(self) -> Any:
        ...

    def setDataValue(self, value: Any):
        ...

    def dataName(self) -> str:
        ...

    def setDataName(self, name: str):
        ...
