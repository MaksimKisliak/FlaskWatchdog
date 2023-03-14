from app.extensions import db, cli
import click
import os
from app.models.user import User
from app.main.routes import check_website_status



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
