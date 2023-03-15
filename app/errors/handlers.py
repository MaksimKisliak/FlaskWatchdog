from app.extensions import db
from flask import render_template
from . import errors_bp


@errors_bp.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html', error=error), 403


@errors_bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors.404.html', error=error), 404


@errors_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html', error=error), 500
