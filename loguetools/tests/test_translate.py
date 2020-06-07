import click
from click.testing import CliRunner
from loguetools.translate import click_translate


runner = CliRunner()

def test_og_patch_translate():
    result = runner.invoke(click_translate, "./loguetools/tests/og_orig/Syn_Lead_1.mnlgprog")
    assert result.exit_code == 0
    # assert result.output == "configure"

def test_og_library_translate():
    result = runner.invoke(click_translate, "./loguetools/tests/og_orig/AnalogueVintage.mnlgpreset")
    assert result.exit_code == 0
    # assert result.output == "configure"
