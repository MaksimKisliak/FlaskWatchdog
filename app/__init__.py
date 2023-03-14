from flask import Flask
from flask_login import LoginManager
from app.extensions import mail, csrf, limiter, db, migrate, cli
from celery.schedules import crontab
from celery import Celery
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
from app.cli import cli


celery = Celery(__name__, broker=os.environ.get('CELERY_BROKER_URL'), backend=os.environ.get('CELERY_RESULT_BACKEND'))


def create_app(config_class=None):
    app = Flask(__name__, template_folder='templates')

    # Load environment variables from .env file
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '.env'))

    # Re-load configuration options from environment variables
    if config_class is None:
        config_class = os.environ.get('APP_SETTINGS')
    app.config.from_object(config_class)

    # Set up Celery
    app.celery = celery
    celery.conf.update(app.config)
    celery.conf.beat_schedule = {
        'check_website_status': {
            'task': 'app.main.routes.check_website_status',
            'schedule': crontab(minute='*/10')  # Run every 10 minutes
        }
    }

    # Set up logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')

        file_handler = RotatingFileHandler('logs/flask_app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask App startup')

    # Initialize Flask-Login
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    # Register user loader function
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    # cli.init_app(app)

    # Register blueprints
    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.errors import errors_bp
    app.register_blueprint(errors_bp)

    # Register custom commands
    cli.register_command(check_status)
    cli.register_command(send_test_email)
    cli.register_command(create_admin)
    cli.register_command(create_user)

    return app
