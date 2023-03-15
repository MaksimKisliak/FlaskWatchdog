from dotenv import load_dotenv
import os
from app import create_app, cli, ext_celery


# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app = create_app()
celery = ext_celery.celery

if __name__ == '__main__':
    cli()
