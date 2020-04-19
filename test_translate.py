import click
from click.testing import CliRunner
from translate import translate


def test_og_patch_translate():
    runner = CliRunner()
    result = runner.invoke(
        translate, ["../../patches/my_individual_patches/MinilogueOGProg_000.zip"]
    )
    assert result.exit_code == 0
    # assert result.output == "configure"
