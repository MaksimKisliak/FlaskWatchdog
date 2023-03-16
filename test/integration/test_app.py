# import pytest
# from app import create_app, db
# from app.models.user import User
# from app.models.website import Website
# from app.models.userwebsite import UserWebsite
# from app.cli import create_user, create_admin, create_website
#
#
# @pytest.fixture(scope='module')
# def test_client():
#     app = create_app()
#     app.config.from_object('config.TestingConfig')
#
#     with app.test_client() as testing_client:
#         with app.app_context():
#             db.create_all()
#             yield testing_client
#             db.session.remove()
#             db.drop_all()
#
#
# def test_user_creation(test_client):
#     runner = test_client.command_runner()
#     result = runner.invoke(create_user, ['--email', 'test@example.com', '--password', 'password'])
#     assert result.exit_code == 0
#     assert 'User created successfully' in result.output
#
#     user = User.query.filter_by(email='test@example.com').first()
#     assert user is not None
#     assert user.email == 'test@example.com'
#     assert not user.is_admin
#
#     # Add more integration tests for user creation, admin creation, website creation, etc.
