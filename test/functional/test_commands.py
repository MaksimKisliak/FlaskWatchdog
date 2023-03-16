import pytest
from click.testing import CliRunner
from app.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_check_status(runner):
    # Test that check-status command runs successfully and outputs the expected message
    result = runner.invoke(cli, ["check-status"])
    assert result.exit_code == 0
    assert 'Website status checked' in result.output


def test_send_test_email(runner):
    # Test that send-test-email command runs successfully and outputs the expected message
    email = "makskislyak@gmail.com"
    result = runner.invoke(cli, ["send-test-email", "--email", email])
    assert result.exit_code == 0
    assert 'Test email sent' in result.output


def test_create_admin(runner, init_test_db):
    # Test that create-admin command runs successfully and outputs the expected message
    email = "admin@example.com"
    password = "strongpassword"
    result = runner.invoke(cli, ["create-admin", "--email", email, "--password", password], input=f"{password}\n")
    assert result.exit_code == 0
    assert 'Admin user created successfully' in result.output


def test_list_users(runner, init_test_db):
    # Test that list-users command runs successfully
    result = runner.invoke(cli, ["list-users"])
    assert result.exit_code == 0


def test_list_websites(runner, init_test_db):
    # Test that list-websites command runs successfully
    result = runner.invoke(cli, ["list-websites"])
    assert result.exit_code == 0


def test_list_user_websites(runner, init_test_db):
    # Test that list-user-websites command runs successfully
    result = runner.invoke(cli, ["list-user-websites"])
    assert result.exit_code == 0


def test_create_user(runner, init_test_db):
    # Test that create-user command runs successfully and outputs the expected message
    email = "user@example.com"
    password = "strongpassword"
    result = runner.invoke(cli, ["create-user", "--email", email, "--password", password], input=f"{password}\n")
    assert result.exit_code == 0
    assert 'User created successfully' in result.output


def test_create_website(runner, init_test_db):
    # Test that create-website command runs successfully
    url = "https://example.com"
    result = runner.invoke(cli, ["create-website", "--url", url], input="1\n")
    assert result.exit_code == 0
