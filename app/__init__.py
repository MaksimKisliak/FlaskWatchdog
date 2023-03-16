from flask import Flask
from flask_login import LoginManager
from app.extensions import mail, csrf, limiter, db, migrate, ext_celery
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
from app.cli import check_status, send_test_email, create_admin, create_user, list_users, list_websites, \
    list_user_websites, create_website
from celery.schedules import crontab


# Define a function that creates and returns a Flask application instance.
def create_app(config_class=None):
    # Load environment variables from .env file
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '.env'))

    # Create Flask app instance
    app = Flask(__name__, template_folder='templates')
    app.app_context().push()

    # Re-load configuration options from environment variables
    if config_class is None:
        config_class = os.environ.get('FLASK_CONFIG')
    app.config.from_object(config_class)  # Loads configuration options from the specified configuration class.

    # Initialize Flask-Login
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    # Register user loader function
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # loads a user from the database based on the user ID.

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    ext_celery.init_app(app)

    # Schedule periodic task for Celery beat
    if not app.config['TESTING']:
        ext_celery.celery.conf.beat_schedule = {
            'check_website_status': {
                'task': 'app.main.routes.check_website_status',
                'schedule': crontab(minute='*/10')  # Run every 10 minute
            }
        }
    # Set up logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')

        file_handler = RotatingFileHandler('logs/FlaskWatchdog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('FlaskWatchdog')  # Sets up logging for the Flask application.

    # Register custom commands
    app.cli.add_command(check_status)
    app.cli.add_command(send_test_email)
    app.cli.add_command(create_admin)
    app.cli.add_command(create_user)
    app.cli.add_command(list_users)
    app.cli.add_command(list_websites)
    app.cli.add_command(list_user_websites)
    app.cli.add_command(create_website)

    # Register blueprints
    from app.errors import errors_bp
    app.register_blueprint(errors_bp)

    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    # Add objects to Flask shell context shell context for flask cli
    # Therefore there's no need to import db via from app import db in Flask shell? Those are added to the
    # shell context with shell_context_processor in the create_app function.
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
