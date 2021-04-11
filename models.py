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
        """Hash a user's credentials and return the user."""

        hashed_password = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed_password.decode('utf8')

        return cls(
            username = username, 
            password = hashed_utf8, 
            email = email, 
            first_name = first_name, 
            last_name = last_name
            )
    
    @classmethod
    def login(cls, username, password):
        """Authenticate a user, return the user if authenticated, and false otherwise."""

        user = cls.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Feedback(db.Model):
    """Represents feedback for a user."""

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'))

    user = db.relationship('User', backref="feedback")






