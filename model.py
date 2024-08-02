from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

# Initialize the SQLAlchemy object
db = SQLAlchemy()

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'User(name = {self.username}, email = {self.email})'

    @validates('username')
    def validate_username(self, key, username):
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return username

    @validates('email')
    def validate_email(self, key, email):
        if not email or '@' not in email:
            raise ValueError("Invalid email address")
        return email
