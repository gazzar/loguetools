import click
from click.testing import CliRunner
from ..explode import explode, sanitise_patchname
from pathlib import Path


runner = CliRunner()

def test_xd_patch_explode():
    result = runner.invoke(explode, "./loguetools/tests/xd_orig/2019-12-17.mnlgxdlib")
    assert result.exit_code == 0
    # assert result.output == "configure"

def test_sanitise():
    result1 = sanitise_patchname(Path("hello"))
    assert result1 == Path("hello")
    result1 = sanitise_patchname(Path("hello"))
    assert result1 == Path("hello-1")
    result1 = sanitise_patchname(Path("hello"))
    assert result1 == Path("hello-2")
    result1 = sanitise_patchname(Path("hello-1"))
    assert result1 == Path("hello-1-1")
    result1 = sanitise_patchname(Path("hello-1"))
    assert result1 == Path("hello-1-2")
    result1 = sanitise_patchname(Path("hello-3"))
    assert result1 == Path("hello-3")
    