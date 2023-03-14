from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Define website model
class Website(db.Model):
    __tablename__ = "website"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False, unique=True, index=True)
    status = db.Column(db.Boolean, default=False)
    last_checked = db.Column(db.DateTime)

    website_users = db.relationship('UserWebsite', back_populates='website')

    def __str__(self):
        return f'<Website id={self.id}, url="{self.url}">'
