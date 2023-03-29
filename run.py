from dotenv import load_dotenv
import os
from app import create_app
from app.cli import cli

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app, celery = create_app()

if __name__ == '__main__':
    cli()
