from flask import Flask, session, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, connect_db
from forms import RegisterForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

app.config['SECRET_KEY'] = 'c8n1m9x3'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/', methods=['GET'])
def redirect_route():
    """Redirect user to /register."""
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Register a user."""
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()
        return redirect('/secret')

    return render_template('register.html', form=form)

@app.route('/secret', methods=['GET'])
def show_secret():
    """Show the secret page."""
    return render_template('secret.html')