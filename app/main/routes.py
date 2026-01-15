from flask_mail import Message
import requests
from datetime import datetime
import os
from urllib.parse import urlparse
from app.models.userwebsite import UserWebsite
from app.models.website import Website
from flask import render_template, redirect, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
from app.extensions import limiter, db, mail
from app.forms import WebsiteForm
from app.main import main_bp
from celery import shared_task
from flask import current_app
from werkzeug.local import LocalProxy

@shared_task
def check_website_status():
    """
    Celery task to check website status for all monitored websites.
    Updates database with current status and sends notifications on status changes.
    """
    # Access the current Flask application object in a more convenient way. Useful when dealing with contexts like
    # multithreading or when the application object is not directly available.
    app_proxy = LocalProxy(lambda: current_app._get_current_object())

    # Use the app context
    with app_proxy.app_context():
        try:
            current_app.logger.info(f"Checking website status at {datetime.utcnow()}")
            websites = Website.query.all()

            for website in websites:
                try:
                    current_app.logger.info(f"Checking website status for {website.url} at {datetime.utcnow()}")
                    status = check_url_status(website.url)
                    current_app.logger.info(f"Website status for {website.url} at {datetime.utcnow()} is {status}")

                    # Update the last checked field in the website model
                    website.last_checked = datetime.utcnow()

                    # Check if the website status has changed
                    if status != website.status:
                        website.status = status

                        # Get the users subscribed to this website
                        users = [user_website.user for user_website in website.website_users]

                        # For each user, update the last notified field in the UserWebsite model
                        for user in users:
                            try:
                                # Find the user_website relationship
                                user_website = next(
                                    (user_website for user_website in website.website_users if user_website.user_id == user.id),
                                    None)

                                # If there is no previous record for this user-website pair, create a new one
                                if not user_website:
                                    user_website = UserWebsite(user_id=user.id, website_id=website.id)
                                    db.session.add(user_website)

                                # Update the fields in the UserWebsite model
                                if user.has_remaining_notifications():
                                    send_email(website.url, status, user.email)
                                    user.decrement_notifications()
                                    user_website.last_notified = datetime.utcnow()
                            except Exception as e:
                                current_app.logger.error(f"Error notifying user {user.email} for website {website.url}: {str(e)}")
                                db.session.rollback()
                                continue

                    # Commit all changes for this website at once
                    db.session.commit()

                except Exception as e:
                    current_app.logger.error(f"Error checking website {website.url}: {str(e)}")
                    db.session.rollback()
                    continue

        except Exception as e:
            current_app.logger.error(f"Fatal error in check_website_status task: {str(e)}")
            db.session.rollback()
            raise


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
        current_app.logger.info(f"Requesting website status for {url} at {datetime.utcnow()}")
        response = session.get(url, timeout=timeout)
        current_app.logger.info(f"Status code for {url} is {response.status_code} at {datetime.utcnow()}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f'Request failed for website {url}: {str(e)}')
        return False


def send_email(website, status, user):
    """
    Send email notification about website status change.

    Args:
        website (str): Website URL
        status (bool): True if online, False if offline
        user (str): User email address
    """
    try:
        current_app.logger.info(
            f"Preparing e-mail for {website} with status {status} for user {user} at {datetime.utcnow()}")

        subject = f"FlaskWatchdog Alert: {website} is {'back online' if status else 'offline'}"

        # Create text and HTML body
        text_body = f"The website {website} is {'back online' if status else 'currently down'}.\n\n" \
                    f"Status checked at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"

        html_body = f"""
        <html>
          <body>
            <h2>FlaskWatchdog Alert</h2>
            <p>The website <strong>{website}</strong> is <strong>{'back online' if status else 'currently down'}</strong>.</p>
            <p><small>Status checked at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</small></p>
          </body>
        </html>
        """

        msg = Message(subject, sender=os.environ.get('MAIL_USERNAME'), recipients=[user])
        msg.body = text_body
        msg.html = html_body

        mail.send(msg)
        current_app.logger.info(f"Sent e-mail for {website} with status {status} for user {user} at {datetime.utcnow()}")

    except Exception as e:
        current_app.logger.error(f"Failed to send email for {website} to {user}: {str(e)}")
        raise


@main_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for Docker and monitoring tools.
    Returns 200 OK if the application is running and database is accessible.
    """
    try:
        # Check database connectivity
        db.session.execute(db.text('SELECT 1'))

        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'FlaskWatchdog',
            'database': 'connected'
        }), 200
    except Exception as e:
        current_app.logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'FlaskWatchdog',
            'error': 'Database connection failed'
        }), 503


@main_bp.route('/', methods=['GET', 'POST'])
@login_required
@limiter.limit("100 per minute")
def dashboard():
    form = WebsiteForm()
    if form.validate_on_submit():
        # check if website already exists in db
        url = urlparse(form.url.data)
        domain_name = url.netloc
        website_to_check = Website.query.filter_by(url=domain_name).first()

        if website_to_check:
            # add user to existing website
            user_website = UserWebsite.query.filter_by(user_id=current_user.id, website_id=website_to_check.id).first()
            if not user_website:
                user_website = UserWebsite(user_id=current_user.id, website_id=website_to_check.id)
                db.session.add(user_website)
                db.session.commit()
            flash('Website added successfully.')
            return redirect(url_for('main.dashboard'))
        else:
            # add new website to db and add current user to its users
            website = Website(url=domain_name)
            db.session.add(website)
            db.session.commit()

            user_website = UserWebsite(user_id=current_user.id, website_id=website.id)
            db.session.add(user_website)
            db.session.commit()

            flash('Website added successfully.')
            return redirect(url_for('main.dashboard'))

    websites = [user_website.website for user_website in current_user.user_websites]
    return render_template('dashboard.html', form=form, websites=websites)


@main_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@limiter.limit("100 per minute")
def delete_website(id):
    user_website = UserWebsite.query.filter_by(user_id=current_user.id, website_id=id).first()

    if not user_website:
        flash('You are not authorized to delete this website.')
        return redirect(url_for('main.dashboard'))

    db.session.delete(user_website)
    db.session.commit()

    website = Website.query.get(id)
    if len(website.website_users) == 0:
        # delete website if no users left
        db.session.delete(website)
        db.session.commit()

    flash('Website deleted successfully.')
    return redirect(url_for('main.dashboard'))
