import click
from click.testing import CliRunner
from .. import dump as du
from ..dump import dump


runner = CliRunner()

def test_og_patch_dump():
    result = runner.invoke(
        dump, "../../patches/my_individual_patches/MinilogueOGProg_000.zip"
    )
    assert result.exit_code == 0
    # assert result.output == "configure"


def test_og_patch_dump_by_ident():
    result = runner.invoke(
        dump, "../../patches/my_individual_patches/MinilogueOGProg_000.zip -i 1"
    )
    assert result.exit_code == 0
    # assert result.output == "configure"


def test_og_patch_dump_by_name():
    result = runner.invoke(
        dump, "../../patches/my_individual_patches/MinilogueOGProg_000.zip -n 'Syn Lead 1'"
    )
    assert result.exit_code == 0
    # assert result.output == "configure"


def test_xd_patch_dump():
    result = runner.invoke(
        dump, ["../../patches/my_individual_patches/LectroFlute.mnlgxdprog"]
    )
    assert result.exit_code == 0
    # assert result.output == "configure"

def test_xd_patch_dump_by_ident():
    result = runner.invoke(
        dump, "../../patches/my_individual_patches/LectroFlute.mnlgxdprog -i 1"
    )
    assert result.exit_code == 0
    # assert result.output == "configure"


def test_xd_patch_dump_by_name():
    result = runner.invoke(
        dump, "../../patches/my_individual_patches/LectroFlute.mnlgxdprog -n 'LectroFlute'"
    )
    assert result.exit_code == 0
    # assert result.output == "configure"


def test_xd_library_dump():
    result = runner.invoke(dump, "../../patches/2019-12-17.mnlgxdlib")
    assert result.exit_code == 0
    # assert result.output == "configure"
