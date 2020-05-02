import click
from click.testing import CliRunner
from .. import dump as du
from ..dump import dump


runner = CliRunner()

def test_og_patch_dump():
    result = runner.invoke(
        dump, "./loguetools/tests/og_orig/Syn_Lead_1.mnlgprog"
    )
    assert result.exit_code == 0
    # assert result.output == "configure"


def test_og_patch_dump_by_ident():
    result = runner.invoke(
        dump, "./loguetools/tests/og_orig/Syn_Lead_1.mnlgprog -i 1"
    )
    assert result.exit_code == 0
    # assert result.output == "configure"


def test_og_patch_dump_by_name():
    result = runner.invoke(
        dump, "./loguetools/tests/og_orig/Syn_Lead_1.mnlgprog -n 'Syn Lead 1'"
    )
    assert result.exit_code == 0
    # assert result.output == "configure"


def test_xd_patch_dump():
    result = runner.invoke(
        dump, ["./loguetools/tests/xd_orig/LectroFlute.mnlgxdprog"]
    )
    assert result.exit_code == 0
    # assert result.output == "configure"

def test_xd_patch_dump_by_ident():
    result = runner.invoke(
        dump, "./loguetools/tests/xd_orig/LectroFlute.mnlgxdprog -i 1"
    )
    assert result.exit_code == 0
    # assert result.output == "configure"


def test_xd_patch_dump_by_name():
    result = runner.invoke(
        dump, "./loguetools/tests/xd_orig/LectroFlute.mnlgxdprog -n 'LectroFlute'"
    )
    assert result.exit_code == 0
    # assert result.output == "configure"


def test_xd_library_dump():
    result = runner.invoke(dump, "./loguetools/tests/xd_orig/2019-12-17.mnlgxdlib")
    assert result.exit_code == 0
    # assert result.output == "configure"
