import logging
from logging.handlers import RotatingFileHandler
import click
from flask.cli import FlaskGroup
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from celery import Celery
from celery.schedules import crontab
from flask import Flask, render_template, flash, redirect, url_for, abort
from flask_mail import Mail, Message
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, URL
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from flask import current_app
from urllib.parse import urlparse

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, template_folder='templates')
csrf = CSRFProtect(app)

app.app_context().push()

# Load configuration from environment variables
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT'))
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy()

# Initialize extensions
db.init_app(app)
mail = Mail(app)

migrate = Migrate(app, db)

# Configure Celery
celery = Celery(app.name, broker=os.environ.get('CELERY_BROKER_URL'),
                backend=os.environ.get('CELERY_RESULT_BACKEND'))
celery.conf.update(app.config)

# Set up beat scheduler
celery.conf.beat_schedule = {
    'check_website_status': {
        'task': 'app.check_website_status',
        'schedule': crontab(minute='*/1')  # Run every 2 minute
    }
}

# Set up logging for Celery
celery.conf.update(
    CELERY_LOG_FILE='logs/celery.log',
    CELERY_LOG_LEVEL='INFO'
)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
    app.logger.info('FlaskWatchdog startup')


# Define user model
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    remaining_notifications = db.Column(db.Integer, default=30)

    websites = db.relationship('Website', secondary='user_website', back_populates='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Define website model
class Website(db.Model):
    __tablename__ = "website"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False, unique=True)
    status = db.Column(db.Boolean, default=False)
    last_checked = db.Column(db.DateTime)

    users = db.relationship('User', secondary='user_website', back_populates='websites')


class UserWebsite(db.Model):
    __tablename__ = "user_website"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    website_id = db.Column(db.Integer, db.ForeignKey('website.id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_notified = db.Column(db.DateTime)

    user = db.relationship('User', backref="user_bref")
    website = db.relationship('Website', backref='website_bref')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'website_id'),
    )


class WebsiteForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(), URL(require_tld=False)])
    submit = SubmitField('Add Website')


class AdminUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    is_admin = BooleanField('Admin User')
    submit = SubmitField('Add User')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')


class UpdateEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Update')


@celery.task
def check_website_status():
    with current_app.app_context():
        app.logger.info(f"Checking website status at {datetime.utcnow()}")
        websites = Website.query.all()

        for website in websites:
            app.logger.info(f"Checking website status for {website.url} at {datetime.utcnow()}")
            status = check_url_status(website.url)
            app.logger.info(f"Website status for {website.url} at {datetime.utcnow()} is {status}")

            # Update the last checked field in the website model
            website.last_checked = datetime.utcnow()
            db.session.commit()

            # Check if the website status has changed
            if status != website.status:
                website.status = status
                db.session.commit()

                # Get the users subscribed to this website
                users = website.users

                # For each user, update the last notified field in the UserWebsite model
                for user in users:
                    user_website = UserWebsite.query.filter_by(user_id=user.id, website_id=website.id).first()

                    # If there is no previous record for this user-website pair, create a new one
                    if not user_website:
                        user_website = UserWebsite(user_id=user.id, website_id=website.id)
                        db.session.add(user_website)

                    # Update the fields in the UserWebsite model
                    if user_website.user.remaining_notifications > 0:
                        user_website.user.remaining_notifications -= 1
                        send_email.delay(website, status, user)
                        user_website.last_notified = datetime.utcnow()
                        db.session.commit()


def check_url_status(url, timeout=10):
    """
    Check website status and return True if it's online, False otherwise
    """
    if not url.startswith('http'):
        url = 'https://' + url
    headers = {'User-Agent': 'Custom user agent'}
    session = requests.Session()
    session.headers.update(headers)
    try:
        app.logger.info(f"Requesting website status for {url} at {datetime.utcnow()}")
        response = session.get(url, timeout=timeout)
        app.logger.info(f"Status code for {url} is {response.status_code} at {datetime.utcnow()}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        app.logger.error(f'Request failed for website {url}: {str(e)}')
        return False


@celery.task
def send_email(website, status, user):
    if status:
        subject = 'Website back online'
        body = 'The website %s is back online' % website.url
    else:
        subject = 'Website offline'
        body = 'The website %s is currently down' % website.url

    msg = Message(subject, sender=os.environ.get('MAIL_USERNAME'), recipients=[user.email])
    msg.body = body
    mail.send(msg)


@celery.task
def send_email(website, status):
    for user in website.users:
        if status:
            subject = 'Website back online'
            body = 'The website %s is back online' % website.url
        else:
            subject = 'Website offline'
            body = 'The website %s is currently down' % website.url

        msg = Message(subject, sender=os.environ.get('MAIL_USERNAME'), recipients=[user.email])
        msg.body = body
        mail.send(msg)


@app.route('/', methods=['GET', 'POST'])
@login_required
def homepage():
    form = WebsiteForm()
    if form.validate_on_submit():
        # check if website already exists in db
        url = urlparse(form.url.data)
        domain_name = url.netloc
        website_to_check = Website.query.filter(Website.url.contains(domain_name)).first()

        if website_to_check:
            # add user to existing website
            if current_user not in website_to_check.users:
                website_to_check.users.append(current_user)
                db.session.commit()
            flash('Website added successfully.')
            return redirect(url_for('homepage'))
        else:
            # add new website to db and add current user to its users
            website = Website(url=domain_name)
            website.users.append(current_user)
            db.session.add(website)
            db.session.commit()

            flash('Website added successfully.')
            return redirect(url_for('homepage'))
    websites = Website.query.join(UserWebsite).filter_by(user_id=current_user.id).all()
    return render_template('index.html', form=form, websites=websites)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('homepage'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    is_admin = False
    if current_user.is_authenticated and current_user.is_admin:
        is_admin = True

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('An account already exists with that email')
            return redirect(url_for('register'))
        else:
            user = User(email=email, is_admin=is_admin)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('homepage'))

    return render_template('register.html', is_admin=is_admin, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)

    form = AdminUserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('An account already exists with that email')
        else:
            is_admin = form.is_admin.data
            user = User(email=email, is_admin=is_admin)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('User added successfully')
        return redirect(url_for('admin'))

    users = User.query.all()
    return render_template('admin.html', users=users, form=form)


@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_website(id):
    website = Website.query.get_or_404(id)
    if current_user not in website.users:
        abort(403)

    website.users.remove(current_user)
    db.session.commit()

    if len(website.users) == 0:
        # delete website if no users left
        db.session.delete(website)
        db.session.commit()

    flash('Website deleted successfully.')
    return redirect(url_for('homepage'))


@app.route('/update_email', methods=['GET', 'POST'])
@login_required
def update_email():
    form = UpdateEmailForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            current_user.email = form.email.data
            db.session.commit()
            flash('Your email has been updated.', 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Invalid password.', 'danger')
    return render_template('update_email.html', form=form)


@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html', error=error)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html', error=error)


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html', error=error), 500


cli = FlaskGroup()


@cli.command('init-db')
def init_db():
    db.create_all()
    click.echo('Database initialized')


@cli.command('check-status')
def check_status():
    check_website_status()
    click.echo('Website status checked')


@cli.command('clear-logs')
def clear_logs():
    """Clear all log files."""
    if os.path.exists('logs'):
        for filename in os.listdir('logs'):
            os.remove(os.path.join('logs', filename))
        click.echo('Logs cleared')
    else:
        click.echo('No logs to clear')


@cli.command('create-admin')
@click.option('--email', prompt=True, help='The email address of the admin user')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True,
              help='The password of the admin user')
def create_admin(email, password):
    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        click.echo('An account already exists with that email')
    else:
        user = User(email=email, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo('Admin user created successfully')


@cli.command('create-user')
@click.option('--email', prompt=True, help='The email address of the user')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True,
              help='The password of the user')
def create_user(email, password):
    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        click.echo('An account already exists with that email')
    else:
        user = User(email=email, is_admin=False)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo('User created successfully')


if __name__ == '__main__':
    cli()
