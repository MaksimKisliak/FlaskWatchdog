import os
import sys

from dotenv import load_dotenv

# Check if running on local machine or cloud server
is_local = os.environ.get('ENVIRONMENT') == 'local' or os.environ.get('ENVIRONMENT') is None

if is_local:
    # Load environment variables from .env file
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '.env'))
else:
    # Assume environment variables are already set for cloud server providers
    pass

# Add project directory to system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "")))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    RATELIMIT_MESSAGE = 'Chill out, man!'
    TESTING = False
    LIMITER_STORAGE_URL = os.environ.get('LIMITER_STORAGE_URL', 'redis://redis:6379')
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")
    DEBUG = os.environ.get('FLASK_ENV')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'sqlite:///flaskwatchdog_dev.db'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'sqlite:///flaskwatchdog_test.db'
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI') or 'sqlite:///flaskwatchdog_prod.db'
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
