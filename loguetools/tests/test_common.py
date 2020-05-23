from ..common import signed_shift, sanitise_patchname
from pathlib import Path


def test_signed_shift():
    assert signed_shift(1, 0) == 1
    assert signed_shift(1, 1) == 2
    assert signed_shift(2, -1) == 1

def test_sanitise():
    sanitise = sanitise_patchname()
    result1 = sanitise(Path("hello"))
    assert result1 == "hello"
    result1 = sanitise("hello")
    assert result1 == "hello-1"
    result1 = sanitise(Path("hello"))
    assert result1 == "hello-2"
    result1 = sanitise(Path("hello-1"))
    assert result1 == "hello-1-1"
    result1 = sanitise(Path("hello-1"))
    assert result1 == "hello-1-2"
    result1 = sanitise(Path("hello-3"))
    assert result1 == "hello-3"
