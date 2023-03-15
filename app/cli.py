import click
from app.extensions import db
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
    send_email(args=['Test Website', True, email])
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
