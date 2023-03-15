import click
from app.extensions import db
from app.models.website import Website
from app.models.userwebsite import UserWebsite
from app.models.user import User
from app.main.routes import check_website_status, send_email
from flask.cli import FlaskGroup

cli = FlaskGroup()


@cli.command('check-status')
def check_status():
    check_website_status.apply_async()
    click.echo('Website status checked')


@cli.command('send-test-email')
@click.option('--email', prompt=True, help='The email address to send the test email to')
def send_test_email(email):
    send_email('Test Website', True, email)
    click.echo('Test email sent')


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


@cli.command('list-users')
def list_users():
    users = User.query.all()
    for user in users:
        click.echo(f"User ID: {user.id}, Email: {user.email}, Is Admin: {user.is_admin}")


@cli.command('list-websites')
def list_websites():
    websites = Website.query.all()
    for website in websites:
        click.echo(f"Website ID: {website.id}, URL: {website.url}, Status: {website.status}")


@cli.command('list-user-websites')
def list_user_websites():
    user_websites = UserWebsite.query.all()
    for user_website in user_websites:
        click.echo(f"User ID: {user_website.user_id}, Website ID: {user_website.website_id}, "
                   f"Last Notified: {user_website.last_notified}, Created At: {user_website.last_notified}")


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


@cli.command('create-website')
@click.option('--url', prompt=True, help='The URL of the website to be added')
def create_website(url):
    # Ensure the URL has a scheme (http or https)
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "http://" + url

    # Parse the URL and extract the domain name
    from urllib.parse import urlparse
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc

    if not domain_name:
        click.echo("Invalid URL. Please provide a valid URL, e.g. domain name only.")
        return

    website = Website.query.filter_by(url=domain_name).first()

    if not website:
        website = Website(url=domain_name, status=False)
        db.session.add(website)
        db.session.commit()
        click.echo('Website created successfully')
    else:
        click.echo('A website with that URL already exists')

    users = User.query.all()
    if users:
        click.echo("Select a user to create a new UserWebsite relationship:")
        for idx, user in enumerate(users, start=1):
            click.echo(f"{idx}. User ID: {user.id}, Email: {user.email}, Is Admin: {user.is_admin}")

        selected_user = click.prompt("Enter the number of the user you want to associate with the website",
                                     type=click.IntRange(1, len(users)))

        user = users[selected_user - 1]

        user_website_exists = UserWebsite.query.filter_by(user_id=user.id, website_id=website.id).first()
        if user_website_exists:
            click.echo('A relationship between this user and website already exists')
        else:
            user_website = UserWebsite(user_id=user.id, website_id=website.id)
            db.session.add(user_website)
            db.session.commit()
            click.echo('User-website relationship created successfully')
    else:
        click.echo("No users available in the database")




if __name__ == '__main__':
    cli()
