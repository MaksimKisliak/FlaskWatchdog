import pytest
from click.testing import CliRunner
from bs4 import BeautifulSoup
from flask_login import current_user

# app_context helps to isolate the tests from each other and prevent the side effects from affecting the other tests.

# Set up a fixture for CliRunner
@pytest.fixture
def runner():
    return CliRunner()


# Test home page view
def test_home_page(client, init_test_db):
    # Get the login page
    assert isinstance(client, object)  # Ensure the client exists
    login_page_response = client.get('auth/login')  # Get the login page
    assert login_page_response.status_code == 200  # Check if the response status code is OK (200)

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


# Helper function to retrieve CSRF token from login page
def get_csrf_token(response):
    soup = BeautifulSoup(response.data, 'html.parser')
    return soup.find("input", {"name": "csrf_token"})['value']


# Test login page view
def test_login_page(client, init_test_db):
    login_response = client.get('/auth/login')  # Get the login page
    assert login_response.status_code == 200  # Check if the response status code is OK (200)
    assert b"Log" in login_response.data  # Check if the page contains the login form


# Test registration page view
def test_registration_page(client):
    response = client.get('/auth/register')  # Get the registration page
    assert response.status_code == 200  # Check if the response status code is OK (200)
    assert b"Register" in response.data  # Check if the page contains the registration form


# Test user registration functionality
def test_register_user(client, init_test_db):
    response = client.get('/auth/register')  # Get the registration page
    csrf_token = get_csrf_token(response)  # Get the CSRF token from the registration page

    # Register a new user
    register_response = client.post('/auth/register',
                                    data=dict(email='newuser@example.com', password='newpassword',
                                              password2='newpassword', csrf_token=csrf_token),
                                    content_type='application/x-www-form-urlencoded', follow_redirects=True)

    # Check if registration is successful
    assert register_response.status_code == 200
    assert b"Logged in as: newuser@example.com" in register_response.data


# Test user login functionality
def test_login_user(client, init_test_db):
    response = client.get('/auth/login')  # Get the login page
    csrf_token = get_csrf_token(response)  # Get the CSRF token from the login page

    # Log in an existing user
    login_response = client.post('/auth/login',
                                 data=dict(email='user1@example.com', password='password1', csrf_token=csrf_token),
                                 content_type='application/x-www-form-urlencoded', follow_redirects=True)

    # Check if login is successful
    assert login_response.status_code == 200
    assert b"Logged in as" in login_response.data


# Test user logout functionality
def test_logout_user(client, init_test_db):
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
    assert current_user.is_authenticated

    # Log out the user
    logout_response = client.get('/auth/logout', follow_redirects=True)

    # Check if logout is successful and user is redirected to the login page
    assert logout_response.status_code == 200
    assert b"Please log in to access this" in logout_response.data

    # Check if current_user is anonymous after logout
    assert current_user.is_anonymous


def test_protected_route_not_logged_in(client):
    # Access the protected route without logging in
    response = client.get('/auth/update_email', follow_redirects=True)

    # Check if the user is redirected to the login page
    assert response.status_code == 200
    assert b"Please log in to access this" in response.data


def test_protected_route_logged_in(client, init_test_db):
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

    # Access the protected route
    response = client.get('/auth/admin', follow_redirects=True)

    # Check if the user cannot access the protected route
    assert response.status_code == 403
    assert b"Forbidden" in response.data
