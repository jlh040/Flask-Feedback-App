from flask import Flask, session, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, Feedback, connect_db
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

app.config['SECRET_KEY'] = 'c8n1m9x3'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
# app.config['WTF_CSRF_ENABLED'] = False

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

        user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()

        session['username'] = username
        return redirect(f'/users/{username}')

    return render_template('register.html', form=form)

@app.route('/users/<username>', methods=['GET'])
def show_user_info(username):
    """Show the user's page."""
    user = User.query.get(username)
    if session.get('username'):
        return render_template('user.html', user=user)
    else:
        flash('Please login first')
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Log a user in."""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if User.login(username, password):
            session['username'] = username
            return redirect(f'/users/{username}')
        else:
            flash('Incorrect Credentials')
            return redirect('/login')

    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout_user():
    """Log a user out."""
    session.clear()
    flash('See you soon!')
    return redirect('/')

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Delete a user."""
    if session.get('username') == username:
        user = User.query.get(username)
        delete_feedback_and_user(user)
        session.clear()
        flash('Your account has been deleted!')
        return redirect('/')
    else:
        flash('Not authorized to delete this user!!')
        return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """Add feedback for a user."""
    form = FeedbackForm()
    user = User.query.get(username)

    if form.validate_on_submit():
        if session.get('username') == username:
            title = form.title.data
            content = form.content.data

            feedback = Feedback(title=title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()

            flash('Feedback added!!')
            return redirect(f'/users/{username}')
        else:
            flash('Not authorized to do this!')
            return redirect(f'/users/{username}')

    return render_template('add_feedback.html', form=form, user=user)

@app.route('/feedback/<int:feedback_id>/update')
def update_feedback(feedback_id):
    """Update a piece of feedback."""
    feedback = Feedback.query.get(feedback_id)
    form = FeedbackForm(obj=feedback)
    return render_template('update_feedback.html', form=form, feedback=feedback)

def delete_feedback_and_user(user):
    """Delete all of a user's feedback and then delete the user."""
    for feedback in user.feedback:
        db.session.delete(feedback)
    
    db.session.delete(user)
    db.session.commit()
