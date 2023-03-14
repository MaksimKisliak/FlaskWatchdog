from flask import url_for


def test_login_valid_credentials(client, user):
    """
    Test logging in with valid credentials.
    """
    response = client.post(url_for('login'), data={'email': user.email, 'password': 'test1234'})
    assert response.status_code == 302
    assert response.location == url_for('homepage', _external=True)


def test_login_invalid_credentials(client, user):
    """
    Test logging in with invalid credentials.
    """
    response = client.post(url_for('login'), data={'email': user.email, 'password': 'wrongpassword'})
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data


def test_logout(client, user):
    """
    Test logging out.
    """
    client.login(user)
    response = client.get(url_for('logout'))
    assert response.status_code == 302
    assert response.location == url_for('homepage', _external=True)


def test_register(client):
    """
    Test user registration.
    """
    response = client.post(url_for('register'), data={'email': 'test@test.com', 'password': 'test1234'})
    assert response.status_code == 302
    assert response.location == url_for('homepage', _external=True)


def test_register_existing_email(client, user):
    """
    Test registering with an existing email.
    """
    response = client.post(url_for('register'), data={'email': user.email, 'password': 'test1234'})
    assert response.status_code == 200
    assert b'An account already exists with that email' in response.data
