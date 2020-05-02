from ..common import signed_shift

def test_signed_shift():
    assert signed_shift(1, 0) == 1
    assert signed_shift(1, 1) == 2
    assert signed_shift(2, -1) == 1
