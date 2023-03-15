from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db


# Define user model
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    _remaining_notifications = db.Column(db.Integer, default=30)
    last_login = db.Column(db.DateTime, nullable=True)

    user_websites = db.relationship('UserWebsite', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_administrator(self):
        return self.is_admin

    def grant_admin_privileges(self):
        self.is_admin = True

    def revoke_admin_privileges(self):
        self.is_admin = False

    @property
    def remaining_notifications(self):
        # calculate remaining notifications based on user's plan
        return self._remaining_notifications

    @remaining_notifications.setter
    def remaining_notifications(self, value):
        self._remaining_notifications = value

    def has_remaining_notifications(self):
        return self._remaining_notifications > 0

    def decrement_notifications(self):
        self._remaining_notifications -= 1
