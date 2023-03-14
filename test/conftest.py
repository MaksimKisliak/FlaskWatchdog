import pytest
from app import create_app, db
from app.models.models import User

@pytest.fixture(scope='module')
def client():
    app = create_app('testing')
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    # Create a test user
    user = User(email='test@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    # Use Flask's test client
    with app.test_client() as client:
        yield client

    db.session.remove()
    db.drop_all()
    app_context.pop()
