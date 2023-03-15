from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter

from app.make_celery import make_celery
from config import Config
from flask_celeryext import FlaskCeleryExt

# Create instances of the extensions
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=Config.LIMITER_STORAGE_URL
)
ext_celery = FlaskCeleryExt(create_celery_app=make_celery)
