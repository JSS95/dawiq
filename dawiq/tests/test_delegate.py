import dataclasses
from dawiq.delegate import convertFromQt


def test_convertFromQt():
    class CustomField:
        def __init__(self, a, b):
            self.a = a
            self.b = b

        def __eq__(self, other):
            return type(self) == type(other) and (self.a, self.b) == (other.a, other.b)

    @dataclasses.dataclass
    class Cls1:
        x: int
        y: CustomField = dataclasses.field(
            metadata=dict(fromQt_converter=lambda args: CustomField(*args))
        )

    assert convertFromQt(Cls1, dict(x=1, y=(2, 3))) == dict(x=1, y=CustomField(2, 3))
