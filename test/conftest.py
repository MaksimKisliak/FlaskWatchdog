from dotenv import load_dotenv
from config import TestingConfig
from click.testing import CliRunner
import pytest
from run import app as flask_app
import os
import sys
from app import db, ext_celery
from app.models.user import User
from app.models.website import Website
from app.models.userwebsite import UserWebsite
import datetime

"""The app fixture creates a Flask application instance that is used by other test functions. Similarly, the client 
fixture initializes a test client that is used to make HTTP requests to the Flask application, and the init_test_db 
fixture initializes the test database. By defining these fixtures, we can reuse the same objects across multiple tests,
 which helps to reduce code duplication and make the tests more modular."""


# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, ".env"))

# Add project directory to system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



# Define a fixture for the Flask application
@pytest.fixture(scope="module")
def app():
    # Set configuration for testing environment
    flask_app.config.from_object(TestingConfig)

    # Create and configure the Celery instance for testing
    from app.extensions import make_celery
    with flask_app.app_context():
        test_celery = make_celery(flask_app)
        ext_celery.celery = test_celery

    return flask_app


# Define a fixture for the test client
@pytest.fixture
def client(app):
    with app.test_client() as test_client:
        yield test_client


# Define a fixture to initialize test database
@pytest.fixture
def init_test_db(app):
    # Create the tables
    with app.app_context():
        db.create_all()

        # Add initial data
        user1 = User(email='user1@example.com')
        user1.set_password('password1')
        user2 = User(email='user2@example.com')
        user2.set_password('password2')
        db.session.add(user1)
        db.session.add(user2)

        db.session.commit()

        website1 = Website(url='https://example1.com')
        website2 = Website(url='https://example2.com')
        db.session.add(website1)
        db.session.add(website2)

        db.session.commit()

        user_website1 = UserWebsite(user_id=user1.id, website_id=website1.id, created_at=datetime.datetime.utcnow())
        user_website2 = UserWebsite(user_id=user2.id, website_id=website2.id, created_at=datetime.datetime.utcnow())
        db.session.add(user_website1)
        db.session.add(user_website2)

        db.session.commit()

    yield

    # Tear down the tables
    with app.app_context():
        db.drop_all()


# Define a fixture for CliRunner
@pytest.fixture
def runner():
    return CliRunner()
