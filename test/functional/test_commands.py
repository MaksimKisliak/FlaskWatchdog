import pytest
from click.testing import CliRunner
from app.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_check_status(runner):
    result = runner.invoke(cli, ["check-status"])
    assert result.exit_code == 0
    assert 'Website status checked' in result.output


def test_send_test_email(runner):
    email = "test@example.com"
    result = runner.invoke(cli, ["send-test-email", "--email", email])
    assert result.exit_code == 0
    assert 'Test email sent' in result.output


def test_create_admin(runner, init_test_db):
    email = "admin@example.com"
    password = "strongpassword"
    result = runner.invoke(cli, ["create-admin", "--email", email, "--password", password], input=f"{password}\n")
    assert result.exit_code == 0
    assert 'Admin user created successfully' in result.output


def test_list_users(runner, init_test_db):
    result = runner.invoke(cli, ["list-users"])
    assert result.exit_code == 0


def test_list_websites(runner, init_test_db):
    result = runner.invoke(cli, ["list-websites"])
    assert result.exit_code == 0


def test_list_user_websites(runner, init_test_db):
    result = runner.invoke(cli, ["list-user-websites"])
    assert result.exit_code == 0


def test_create_user(runner, init_test_db):
    email = "user@example.com"
    password = "strongpassword"
    result = runner.invoke(cli, ["create-user", "--email", email, "--password", password], input=f"{password}\n")
    assert result.exit_code == 0
    assert 'User created successfully' in result.output


def test_create_website(runner, init_test_db):
    url = "https://example.com"
    result = runner.invoke(cli, ["create-website", "--url", url], input="1\n")
    assert result.exit_code == 0

