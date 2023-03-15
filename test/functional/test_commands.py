from click.testing import CliRunner
from app.cli import cli


def test_check_status():
    runner = CliRunner()
    result = runner.invoke(cli, ['check-status'])
    assert result.exit_code == 0
    assert 'Website status checked' in result.output


# Add more functional tests for other CLI commands
