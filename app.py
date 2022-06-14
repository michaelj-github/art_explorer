from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User, Artwork, UserArtwork
from sqlalchemy.exc import IntegrityError
from forms import LoginForm, RegisterForm
import os
import pydash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'orstealthissecrettoo')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = (os.environ.get('DATABASE_URL', 'postgresql:///art_explorer_db').replace('postgres://', 'postgresql://'))

connect_db(app)
db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """A new user can register an account."""
    if "username" not in session:
        form = RegisterForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            new_user = User.register(username, password, first_name, last_name)
            db.session.add(new_user)
            try:
                db.session.commit()
            except IntegrityError:
                form.username.errors.append('There is already an account with that username. Choose another user name or log in if you already have an account.')
                return render_template('register.html', form=form)
            session['username'] = new_user.username
            session['share'] = new_user.share
            flash('Successfully Created Your Account! Now you can find some art or check out the shared collections.', "success")
            return redirect(f"/user/{new_user.username}")
        return render_template('login_register.html', form=form, display='register')
    else:
        return redirect(f"/user/{session['username']}")

@app.route('/')
def home_page():
    """Reroute to display the user's information."""
    if "username" not in session:        
        return render_template('index.html')
    else:
        return redirect(f"/user/{session['username']}")

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """A user can login to an account."""
    if "username" not in session:
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.authenticate(username, password)
            if user:                
                flash(f"Welcome Back {user.first_name} {user.last_name}!", "primary")
                session['username'] = user.username
                session['share'] = user.share
                return redirect(f"/user/{user.username}")
            else:
                form.username.errors = ['Invalid username or password.']
        return render_template('login_register.html', form=form, display='login')
    else:
        return redirect(f"/user/{session['username']}")

@app.route('/logout')
def logout_user():
    """A logged in user can log out."""
    session.pop('username', None)
    session.pop('share', None)    
    flash("Goodbye!", "info")
    return redirect('/')

@app.route('/user/<username>')
def display_page(username):
    """Display the user's information."""
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:        
        user = User.query.get(session['username'])
        user_art = UserArtwork.query.filter_by(username=session['username']).all()
        return render_template('display.html', user=user, user_art=user_art)