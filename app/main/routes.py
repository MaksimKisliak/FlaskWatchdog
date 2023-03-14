from flask_mail import Message
import requests
from datetime import datetime
import os
from flask import current_app
from urllib.parse import urlparse
from app.models.website import Website
from app.models.userwebsite import UserWebsite
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import limiter, db, celery, mail
from app.forms import WebsiteForm
from app.main import main_bp
from app import create_app

app = create_app()

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
                users = [user_website.user for user_website in website.website_users]

                # For each user, update the last notified field in the UserWebsite model
                for user in users:
                    # next() is used to find the first item in a list that satisfies a particular condition, allowing
                    # the code to exit the loop as soon as a match is found. This is more efficient than using a for
                    # loop to iterate over the entire list, especially for large lists. next() is also used with
                    # a default value of None to gracefully handle cases where no matching item is found.
                    user_website = next(
                        (user_website for user_website in website.website_users if user_website.user_id == user.id),
                        None)

                    # If there is no previous record for this user-website pair, create a new one
                    if not user_website:
                        user_website = UserWebsite(user_id=user.id, website_id=website.id)
                        db.session.add(user_website)

                    # Update the fields in the UserWebsite model
                    if user.has_remaining_notifications():
                        # The delay() method is used to defer the execution of a function or method call to a
                        # background worker in a task queue, which allows the main application to continue processing
                        # without blocking.
                        send_email.delay(website.url, status, user.email)
                        user.decrement_notifications()
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
    app.logger.info(f"Preparing e-mail for {website} with status {status} for user {user} at {datetime.utcnow()}")
    subject = 'Website back online' if status else 'Website offline'
    body = 'The website %s is back online' % website \
        if status else 'The website %s is currently down' % website

    msg = Message(subject, sender=os.environ.get('MAIL_USERNAME'), recipients=[user])
    msg.body = body
    mail.send(msg)
    app.logger.info(f"Sent e-mail for {website} with status {status} for user {user} at {datetime.utcnow()}")


@main_bp.route('/', methods=['GET', 'POST'])
@login_required
@limiter.limit("5 per minute")
def homepage():
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
            return redirect(url_for('homepage'))
        else:
            # add new website to db and add current user to its users
            website = Website(url=domain_name)
            db.session.add(website)
            db.session.commit()

            user_website = UserWebsite(user_id=current_user.id, website_id=website.id)
            db.session.add(user_website)
            db.session.commit()

            flash('Website added successfully.')
            return redirect(url_for('homepage'))

    websites = [user_website.website for user_website in current_user.user_websites]
    return render_template('index.html', form=form, websites=websites)

@main_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_website(id):
    user_website = UserWebsite.query.filter_by(user_id=current_user.id, website_id=id).first()

    if not user_website:
        flash('You are not authorized to delete this website.')
        return redirect(url_for('homepage'))

    db.session.delete(user_website)
    db.session.commit()

    website = Website.query.get(id)
    if len(website.website_users) == 0:
        # delete website if no users left
        db.session.delete(website)
        db.session.commit()

    flash('Website deleted successfully.')
    return redirect(url_for('homepage'))
