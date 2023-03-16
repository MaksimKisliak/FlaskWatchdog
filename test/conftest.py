from dotenv import load_dotenv
from config import TestingConfig
from click.testing import CliRunner
import pytest
from run import app as flask_app
import os
import sys
from app import db
from app.models.user import User
from app.models.website import Website
from app.models.userwebsite import UserWebsite
import datetime

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, ".env"))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def app():
    flask_app.config.from_object(TestingConfig)
    return flask_app


@pytest.fixture
def client(app):
    with app.test_client() as test_client:
        yield test_client


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


# Add the CliRunner fixture
@pytest.fixture
def runner():
    return CliRunner()
