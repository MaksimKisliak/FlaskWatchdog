from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db

class UserWebsite(db.Model):
    """Model for representing the relationship between a user and a website."""
    __tablename__ = "user_website"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), index=True, nullable=False)
    website_id = db.Column(db.Integer, db.ForeignKey('website.id', ondelete='CASCADE'), index=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    last_notified = db.Column(db.DateTime(timezone=True), nullable=True)

    user = db.relationship('User', back_populates='user_websites')
    website = db.relationship('Website', back_populates='website_users')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'website_id'),
    )
