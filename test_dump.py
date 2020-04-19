import click
from click.testing import CliRunner
from dump import dump


def test_og_patch_dump():
    runner = CliRunner()
    result = runner.invoke(
        dump, ["../../patches/my_individual_patches/MinilogueOGProg_000.zip"]
    )
    assert result.exit_code == 0
    # assert result.output == "configure"


def test_xd_patch_dump():
    runner = CliRunner()
    result = runner.invoke(
        dump, ["../../patches/my_individual_patches/LectroFlute.mnlgxdprog"]
    )
    assert result.exit_code == 0
    # assert result.output == "configure"


def test_xd_library_dump():
    runner = CliRunner()
    result = runner.invoke(dump, ["../../patches/2019-12-17.mnlgxdlib"])
    assert result.exit_code == 0
    # assert result.output == "configure"
