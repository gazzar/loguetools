import click
from click.testing import CliRunner
from ..explode import click_explode


runner = CliRunner()

def test_xd_patch_explode():
    result = runner.invoke(click_explode, "./loguetools/tests/xd_orig/2019-12-17.mnlgxdlib")
    assert result.exit_code == 0
    # assert result.output == "configure"
