from dotenv import load_dotenv
from flask.testing import FlaskClient
from config import TestingConfig
from click.testing import CliRunner
import pytest
from run import app as flask_app
from run import cli
import os
import sys


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


# Add the CliRunner fixture
@pytest.fixture
def runner():
    return CliRunner()
