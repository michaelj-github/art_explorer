from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True, nullable=False,  unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    share = db.Column(db.Text, default='No', nullable=False)

    @classmethod
    def register(cls, username, password, first_name, last_name):
        """Register user."""
        # this code is based on our flask-feedback project
        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")
        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct."""
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # return user instance
            return user
        else:
            return False

class Artwork(db.Model):
    """Artwork."""
    __tablename__ = 'artworks'

    id = db.Column(db.Integer, primary_key=True, nullable=False,  unique=True)
    title = db.Column(db.Text, nullable=False)
    artist = db.Column(db.Text, nullable=False)
    image_link = db.Column(db.Text, nullable=False)

    users = db.relationship('User', secondary="users_artworks", backref="artworks")

class UserArtwork(db.Model):
    """Mapping of an artwork to a user."""
    __tablename__ = 'users_artworks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, db.ForeignKey('users.username'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artworks.id'), nullable=False)
    comment = db.Column(db.Text, nullable=True)

