import click
from click.testing import CliRunner
from .. import translate as tr
from ..translate import translate

runner = CliRunner()

def test_og_patch_translate():
    result = runner.invoke(
        translate, "../../patches/my_individual_patches/MinilogueOGProg_000.zip"
    )
    assert result.exit_code == 0
    # assert result.output == "configure"

def test_signed_shift():
    assert tr.signed_shift(1, 0) == 1
    assert tr.signed_shift(1, 1) == 2
    assert tr.signed_shift(2, -1) == 1
