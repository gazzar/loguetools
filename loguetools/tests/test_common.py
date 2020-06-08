import loguetools.common as common
import version
from pathlib import Path


def test_signed_shift():
    assert common.signed_shift(1, 0) == 1
    assert common.signed_shift(1, 1) == 2
    assert common.signed_shift(2, -1) == 1

def test_sanitise():
    sanitise = common.sanitise_patchname()
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

def test_is_init_patch():
    init_program_hashes = {
        'og': '9d2fd7e2e97edc87306d8360eb881534',
        'xd': 'fd6940f683f8b69966fc3fd08bbb5ee3',
        'prologue': 'a4fa5be24cb09c35a91e81ef2bbf71af',
    }
    flavour = "xd"
    hash = init_program_hashes["xd"]
    assert common.is_init_patch(flavour, hash) 

    flavour = "og"
    hash = init_program_hashes["og"]
    assert common.is_init_patch(flavour, hash)

    flavour = "prologue"
    hash = init_program_hashes["prologue"]
    assert common.is_init_patch(flavour, hash)

    flavour = "xd"
    hash = init_program_hashes["og"]
    assert common.is_init_patch(flavour, hash) == False

    flavour = "xd"
    hash = init_program_hashes["prologue"]
    assert common.is_init_patch(flavour, hash) == False

def test_file_type():
    logue_type, collection = common.file_type(".mnlgxdlib")
    assert logue_type == 'xd'
    assert collection

    logue_type, collection = common.file_type(".mnlgprog")
    assert logue_type == 'og'
    assert collection == False

def test_version():
    assert len(version.__version__.split('.')) == 3
