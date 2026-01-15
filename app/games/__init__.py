from flask import Blueprint

games_bp = Blueprint('games', __name__, url_prefix='/games')

from app.games import routes
