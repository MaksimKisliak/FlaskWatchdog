from flask.cli import FlaskGroup
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from celery import Celery
from config import Config

# Create instances of the extensions
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
csrf = CSRFProtect()
celery = Celery()
cli = FlaskGroup()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10 per minute", "100 per day", "10 per hour"],
    storage_uri=Config.LIMITER_STORAGE_URL
)
