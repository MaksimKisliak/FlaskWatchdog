from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from app.games import games_bp
from app.extensions import db, limiter
from datetime import datetime


@games_bp.route('/')
@limiter.limit("100 per minute")
def index():
    """
    Games landing page showing available games.
    """
    games = [
        {
            'id': 'dino-runner',
            'name': 'Dino Runner',
            'description': 'Classic dinosaur running game with obstacles. Press Space to jump!',
            'difficulty': 'Easy',
            'icon': '🦖'
        },
        {
            'id': 'coming-soon',
            'name': 'More Games',
            'description': 'More exciting games coming soon!',
            'difficulty': 'TBA',
            'icon': '🎮'
        }
    ]
    return render_template('games/index.html', games=games)


@games_bp.route('/dino-runner')
@limiter.limit("100 per minute")
def dino_runner():
    """
    Enhanced dinosaur runner game with scoring and difficulty progression.
    """
    # Get user's high score if authenticated
    high_score = 0
    if current_user.is_authenticated:
        high_score = current_user.game_high_score if hasattr(current_user, 'game_high_score') else 0

    return render_template('games/dino_runner.html', high_score=high_score)


@games_bp.route('/api/save-score', methods=['POST'])
@login_required
@limiter.limit("10 per minute")
def save_score():
    """
    API endpoint to save user's game score.
    """
    try:
        data = request.get_json()
        score = data.get('score', 0)

        # Update user's high score if this is better
        if not hasattr(current_user, 'game_high_score'):
            # Add column if it doesn't exist (will be handled by migration)
            pass

        if hasattr(current_user, 'game_high_score'):
            if score > (current_user.game_high_score or 0):
                current_user.game_high_score = score
                db.session.commit()
                return jsonify({
                    'success': True,
                    'message': 'New high score!',
                    'high_score': score
                }), 200

        return jsonify({
            'success': True,
            'message': 'Score recorded',
            'high_score': current_user.game_high_score if hasattr(current_user, 'game_high_score') else 0
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@games_bp.route('/api/leaderboard')
@limiter.limit("30 per minute")
def leaderboard():
    """
    API endpoint to get top scores leaderboard.
    """
    try:
        # This will be implemented when game_high_score column is added to User model
        # For now, return empty leaderboard
        leaderboard_data = []

        return jsonify({
            'success': True,
            'leaderboard': leaderboard_data
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
