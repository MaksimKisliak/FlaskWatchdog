from pprint import pprint

import pytest
from app.main.routes import check_website_status
from unittest.mock import patch
import redis
from app import create_app
from config import TestingConfig


def test_redis_connection():
    """
    Test to verify that the connection to Redis is successful and basic operations are working.
    """
    # Create an instance of the Flask app with the testing configuration
    app = create_app(TestingConfig)

    # Get the Redis connection details from the app's configuration
    redis_url = app.config['CELERY_BROKER_URL']

    # Create a Redis connection
    r = redis.StrictRedis.from_url(redis_url)

    # Test basic Redis operations
    key = 'test_key'
    value = 'test_value'

    # Set the key-value pair in Redis
    r.set(key, value)

    # Get the value associated with the key from Redis
    result = r.get(key).decode('utf-8')

    # Delete the key-value pair from Redis
    r.delete(key)

    # Check if the value retrieved from Redis matches the expected value
    assert result == value


@pytest.fixture
def send_email_mock():
    """
    Fixture for mocking the send_email function.
    """
    with patch('app.main.routes.send_email') as mock:
        yield mock


@pytest.fixture(scope='function')
def celery_config(app):
    """
    Fixture for setting up the Celery configuration.
    """
    return {
        'broker_url': app.config['CELERY_BROKER_URL'],
        'result_backend': app.config['CELERY_RESULT_BACKEND'],
        'task_always_eager': True,
        'task_eager_propagates': True,
    }


@pytest.fixture(scope='module')
def celery_includes():
    """
    Fixture for specifying the Celery task modules to be included.
    """
    return ['app.main.routes']


@pytest.fixture(scope='module')
def celery_worker_parameters():
    """
    Fixture for setting up the Celery worker parameters.
    """
    return {
        'queues': ('celery',),
        'perform_ping_check': False,
    }


def test_check_website_status(celery_app, celery_worker, init_test_db, send_email_mock, client):
    """
    Test to verify that the check_website_status task is successful and that the send_email function is called.
    """
    # Call the Celery task
    with client.application.app_context():
        task = check_website_status.delay()

        # Check if the task was successful and if the send_email function was called
        assert send_email_mock.called
        assert task.status == 'SUCCESS'
