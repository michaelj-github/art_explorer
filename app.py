from flask import Flask, render_template, redirect, session, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Artwork, UserArtwork
from sqlalchemy.exc import IntegrityError
from forms import LoginForm, RegisterForm, UpdateForm, UpdateComments, ChangePasswordForm
import os
import requests
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

toolbar = DebugToolbarExtension(app)

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
    """Display the user's collection information."""
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:        
        user = User.query.get(session['username'])
        user_art = UserArtwork.query.filter_by(username=session['username']).all()
        return render_template('display.html', user=user, user_art=user_art)

@app.route('/user/<username>/update', methods=['GET', 'POST'])
def update_user(username):
    """A user can update their account information."""
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        user = User.query.get(session['username'])
        form = UpdateForm(obj=user)
        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.share = form.share.data
            db.session.commit()
            flash('Successfully Updated Your Account!', "success")
            return redirect(f"/user/{user.username}")
        return render_template('update.html', form=form, user=user)

@app.route('/user/<username>/changepassword', methods=['GET', 'POST'])
def change_password(username):
    """A user can change their password."""
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        user = User.query.get(session['username'])
        form = ChangePasswordForm(obj=user)
        if form.validate_on_submit():
            hashed = bcrypt.generate_password_hash(form.password.data)
            hashed_utf8 = hashed.decode("utf8")
            user.password = hashed_utf8
            db.session.commit()
            flash('Successfully Changed Your Password!', "success")
            return redirect(f"/user/{user.username}")
        return render_template('changepassword.html', form=form, user=user)     

@app.route('/collection/share', methods=['GET', 'POST'])
def update_share():
    """A user can share or stop sharing their colleciton."""
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        share = request.args.get('share')
        user = User.query.get(session['username'])
        if share == "Yes":
            user.share = "Yes"
            flash('Sharing your collection!', "success")
        else:
            user.share = "No"
            flash('Stopped sharing your collection!', "success")
        db.session.commit()
        return redirect(f"/user/{user.username}")

@app.route("/user/<username>/delete", methods=["POST"])
def delete_user(username):
    """ Delete this user """
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        user = User.query.get(session['username'])
        db.session.delete(user)
        db.session.commit()
        session.pop('username', None)
        session.pop('share', None)
    return redirect('/')

@app.route("/artwork/add", methods=["GET", "POST"])
def add_artwork():
    """Render new_artwork form to search for artworks"""
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        user = User.query.get(session['username'])
        return render_template('new_artwork.html', user=user)

@app.route("/artworks/search")
def search_for_artworks():
    """Search for art works."""

    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        search_for = request.args.get('search_for').strip()
        if len(search_for) < 2:
            flash("Please enter at least 2 characters to search!", "danger")
            return redirect('/artwork/add')
        else:
            res = requests.get(f'https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&q={search_for}')
            data = res.json()
            if data['total'] == 0:
                flash("No artworks were found for that search! Please try again with a different search term.", "danger")
                return redirect('/artwork/add')
            else:
                user = User.query.get(session['username'])
                small_images = []
                data_selection = pydash.sample_size(data['objectIDs'], 16)
                for object in data_selection:
                    user_art = UserArtwork.query.filter_by(username=session['username'], artwork_id=object).first()
                    if not user_art and object > 0:
                        art = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object}")
                        if art.status_code == 200:
                            jart = art.json()
                            if len(jart['primaryImageSmall']) > 0 and len(small_images) < 16:
                                small_images.append([jart['primaryImageSmall'], object])
                            if len(small_images) >= 8:
                                break
                return render_template("found_artworks.html", art=small_images, search_for=search_for, user=user)

@app.route("/artwork/addtocollection/<int:artwork_id>")
def add_to_collection(artwork_id):
    """add to collection."""
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        art = Artwork.query.get(artwork_id)
        if art == None:
            title=session['title']
            artist=session['artist']
            image=session['image_link']
            new_art = Artwork(id=artwork_id, title=title, artist=artist, image_link=image)
            db.session.add(new_art)
            db.session.commit()
            new_user_art = UserArtwork(username=session['username'], artwork_id=artwork_id)
            db.session.add(new_user_art)
            db.session.commit()
        else:
            user_art = UserArtwork.query.filter_by(username=session['username'], artwork_id=artwork_id).first()
            if user_art == None:
                new_user_art = UserArtwork(username=session['username'], artwork_id=artwork_id)
                db.session.add(new_user_art)
                db.session.commit()
        return redirect(f"/user/{session['username']}")

@app.route("/artwork/detail/<int:artwork_id>")
def show_artwork_detail(artwork_id):
    """Show details for an art work."""
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        art = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{artwork_id}")
        jart = art.json()
        user_art = UserArtwork.query.filter_by(username=session['username'], artwork_id=artwork_id).first()
        art = Artwork.query.get(artwork_id)
        if art == None:
            session['title'] = jart['title']
            session['artist'] = jart['artistDisplayName']
            session['image_link'] = jart['primaryImageSmall']
        user = User.query.get(session['username'])
        return render_template("artwork_detail.html", artwork_id=artwork_id, jart=jart, user_art=user_art, user=user)

@app.route("/artwork/fullscreen/<int:artwork_id>")
def show_artwork_fullscreen(artwork_id):
    """Show fullscreen view of an art work."""
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        art = Artwork.query.get(artwork_id)
        return render_template("artwork_fullscreen.html", artwork_id=artwork_id, art=art)

@app.route("/artwork/removefromcollection/<int:artwork_id>", methods=["POST"])
def delete_artwork(artwork_id):
    """ Delete this artwork from collection """
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        user_art = UserArtwork.query.filter_by(username=session['username'], artwork_id=artwork_id).first()
        db.session.delete(user_art)
        db.session.commit()
    return redirect(f"/user/{session['username']}")

@app.route("/artwork/editcomments/<user_art_id>", methods=['GET', 'POST'])
def update_comments(user_art_id):
    """A user can update their comments on an artwork."""
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        user = User.query.get(session['username'])
        user_art = UserArtwork.query.get(user_art_id)
        art = Artwork.query.get(user_art.artwork_id)
        form = UpdateComments(obj=user_art)
        if form.validate_on_submit():
            user_art.comment = form.comment.data
            db.session.commit()
            flash('Successfully Updated Your Comments!', "success")
            return redirect(f"/artwork/detail/{user_art.artwork_id}")
        return render_template('update_comments.html', form=form, user=user, art=art)

@app.route("/sharedcollections")
def list_shared_collections():
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        user = User.query.get(session['username'])        
        users = User.query.filter_by(share="Yes").all()
        user_art_collections = UserArtwork.query.order_by(UserArtwork.username).all()
        return render_template('list_shared_collections.html', user=user, users=users, user_art_collections=user_art_collections)

@app.route("/sharedcollection/<username>")
def list_a_shared_collection(username):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        user = User.query.get(session['username'])
        other_user = User.query.get(username)
        if other_user.share == "Yes":
            other_user_art = UserArtwork.query.filter_by(username=username).all()
            return render_template('display_collection.html', user=user, other_user_art=other_user_art, other_user=other_user)
        return redirect('/sharedcollections')        