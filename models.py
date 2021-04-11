from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect to the database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Represents a user."""

    __tablename__ = 'users'

    username = db.Column(db.String(20), unique = True, primary_key = True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Authenticate a user's credentials."""

        hashed_password = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed_password.decode('utf8')

        return cls(
            username = username, 
            password = hashed_utf8, 
            email = email, 
            first_name = first_name, 
            last_name = last_name
            )






