import pytest
from click.testing import CliRunner
from bs4 import BeautifulSoup
from flask_login import current_user


@pytest.fixture
def runner():
    return CliRunner()


def test_home_page(client, init_test_db):
    # Get the login page
    assert isinstance(client, object)
    login_page_response = client.get('auth/login')
    assert login_page_response.status_code == 200

    # Retrieve the CSRF token from the login page
    csrf_token = get_csrf_token(login_page_response)

    # Log in a user
    login_response = client.post('auth/login',
                                 data=dict(email='user1@example.com', password='password1', csrf_token=csrf_token),
                                 content_type='application/x-www-form-urlencoded', follow_redirects=True)

    # Check if login is successful
    assert login_response.status_code == 200

    # Test the dashboard route
    response = client.get('/')
    assert response.status_code == 200


def get_csrf_token(response):
    soup = BeautifulSoup(response.data, 'html.parser')
    return soup.find("input", {"name": "csrf_token"})['value']


def test_login_page(client, init_test_db):
    with client.application.app_context():
        login_response = client.get('/auth/login')
        assert login_response.status_code == 200
        assert b"Log" in login_response.data


def test_registration_page(client):
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b"Register" in response.data


def test_register_user(client, init_test_db):
    with client.application.app_context():
        response = client.get('/auth/register')
        csrf_token = get_csrf_token(response)
        register_response = client.post('/auth/register',
                                        data=dict(email='newuser@example.com', password='newpassword',
                                                  password2='newpassword', csrf_token=csrf_token),
                                        content_type='application/x-www-form-urlencoded', follow_redirects=True)
        assert register_response.status_code == 200
        assert b"Logged in as: newuser@example.com" in register_response.data


def test_login_user(client, init_test_db):
    with client.application.app_context():
        response = client.get('/auth/login')
        csrf_token = get_csrf_token(response)
        login_response = client.post('/auth/login',
                                     data=dict(email='user1@example.com', password='password1', csrf_token=csrf_token),
                                     content_type='application/x-www-form-urlencoded', follow_redirects=True)
        assert login_response.status_code == 200
        assert b"Logged in as" in login_response.data


def test_logout_user(client, init_test_db):
    with client.application.app_context():
        # Get the login page
        response = client.get('/auth/login')
        assert response.status_code == 200

        # Retrieve the CSRF token from the login page
        csrf_token = get_csrf_token(response)

        # Log in a user
        login_response = client.post('/auth/login',
                                     data=dict(email='user1@example.com', password='password1', csrf_token=csrf_token),
                                     content_type='application/x-www-form-urlencoded', follow_redirects=True)

        # Check if login is successful
        assert login_response.status_code == 200
        assert b"Logged in as" in login_response.data

        # Check if current_user is authenticated after login
        with client.application.app_context():
            assert current_user.is_authenticated

        # Log out the user
        logout_response = client.get('/auth/logout', follow_redirects=True)

        # Check if logout is successful and user is redirected to the login page
        assert logout_response.status_code == 200
        assert b"Please log in to access this" in logout_response.data

        # Check if current_user is anonymous after logout
        with client.application.app_context():
            assert current_user.is_anonymous


def test_protected_route_not_logged_in(client):
    with client.application.app_context():
        # Access the protected route without logging in
        response = client.get('auth/update_email', follow_redirects=True)

        # Check if the user is redirected to the login page
        assert response.status_code == 200
        assert b"Please log in to access this" in response.data


def test_protected_route_logged_in(client, init_test_db):
    with client.application.app_context():
        # Get the login page
        response = client.get('auth/login')
        assert response.status_code == 200

        # Retrieve the CSRF token from the login page
        csrf_token = get_csrf_token(response)

        # Log in a user
        login_response = client.post('auth/login',
                                     data=dict(email='user1@example.com', password='password1', csrf_token=csrf_token),
                                     content_type='application/x-www-form-urlencoded', follow_redirects=True)

        # Check if login is successful
        assert login_response.status_code == 200
        assert b"Logged in as" in login_response.data

        # Access the protected route
        response = client.get('auth/admin', follow_redirects=True)

        # Check if the user cannot access the protected route
        assert response.status_code == 403
        assert b"Forbidden" in response.data
