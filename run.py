from dotenv import load_dotenv
import os
from app import create_app, cli
from app.extensions import ext_celery


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app = create_app()
celery = ext_celery.celery

if __name__ == '__main__':
    cli()
