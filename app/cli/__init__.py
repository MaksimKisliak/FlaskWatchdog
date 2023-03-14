from flask import Blueprint

cli_bp = Blueprint('cli', __name__)

from app.cli import routes