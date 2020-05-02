import click
from click.testing import CliRunner
from ..explode import explode


runner = CliRunner()

def test_xd_patch_explode():
    result = runner.invoke(explode, "./loguetools/tests/xd_orig/2019-12-17.mnlgxdlib")
    assert result.exit_code == 0
    # assert result.output == "configure"
