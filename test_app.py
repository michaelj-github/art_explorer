#  python -m unittest test_app.py
from flask import session

from unittest import TestCase
from models import db, User, Artwork, UserArtwork
import os

os.environ['DATABASE_URL'] = "postgresql:///art_explorer_test_db"

from app import app

app.config['TESTING'] = True
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False

class TestAppTestCase(TestCase):
    def setUp(self):
        """Drop and recreate the db before each test"""
        db.drop_all()
        db.create_all()

    def test_home_page_route(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Log in to your account', html)
            
########################################################################
# User register, login, logout, display, update, change password, delete
########################################################################

    def test_register_user_route(self):
        """Register a new user"""
        with app.test_client() as client:
            res = client.post('/register', data={'username': 'testuser'})
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Art Explorer', html)

    def test_logout_redirect(self):
        """Log out and redirect to root"""
        with app.test_client() as client:
            res = client.get('/logout')            
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/')
            
    def test_logout_redirect_followed(self):
        """Log out and check the redirect to root"""
        with app.test_client() as client:
            res = client.get('/logout', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Log in to your account', html)

    def test_login(self):
        with app.test_client() as client:
            """Login page"""
            res = client.post('/login')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<button class="btn btn-primary btn-block btn-lg">Login</button>', html)

    def test_display(self):
        with app.test_client() as client:
            """Display the user's main page with their art collection"""
            with client.session_transaction() as change_session:
                username1='user1'
                change_session['username'] = username1
            res = client.get('/user/username1')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<button class="btn btn-primary" type="submit" >Find some art!</button>', html)

    def test_update(self):
        with app.test_client() as client:
            """Update page for user account information"""
            with client.session_transaction() as change_session:
                username1='user1'
                change_session['username'] = username1
            res = client.get('/user/username1/update')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2 class="join-message">Update your account information.</h2>', html)
    
    def test_change_password(self):
        with app.test_client() as client:
            """Separate page for password update"""
            with client.session_transaction() as change_session:
                username1='user1'
                change_session['username'] = username1
            res = client.get('/user/username1/changepassword')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2 class="join-message">Change your password.</h2>', html)

    def test_delete(self):
        with app.test_client() as client:
            """Delete the user's account"""
            with client.session_transaction() as change_session:
                username1='user1'
                change_session['username'] = username1
            user1 = User(username='user1', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="One", share='No', collection=1)
            db.session.add(user1)
            db.session.commit()
            res = client.post('/user/username1/delete', data={'username': 'user1'})
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/')       

    def test_delete_redirect(self):
        with app.test_client() as client:
            """Check the redirect"""
            with client.session_transaction() as change_session:
                username1='user1'
                change_session['username'] = username1
            user1 = User(username='user1', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="One", share='No', collection=1)
            db.session.add(user1)
            db.session.commit()
            res = client.post('/user/username1/delete', data={'username': 'user1'}, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Log in to your account', html)

############################################
# 404 errors
############################################

    def test_page_not_found(self):
        with app.test_client() as client:
                res = client.get('/abcde')
                html = res.get_data(as_text=True)
                self.assertEqual(res.status_code, 200)
                self.assertIn('Oops! That page was not found. Click here to go to your home page.', html)

########################################################################
# Artwork add to or remove from collection, view, edit comments
########################################################################

    def test_artwork_add(self):
        with app.test_client() as client:
            """A logged in user can search for artworks"""
            with client.session_transaction() as change_session:                
                change_session['username'] = 'user1'
            user1 = User(username='user1', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="One", share='No', collection=1)
            db.session.add(user1)
            db.session.commit()
            res = client.get('/artwork/add')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Search The Metropolitan Museum of Art Collection</h1>', html)

    def test_artwork_add_to_collection(self):
        with app.test_client() as client:
            """User can add art to collection"""
            with client.session_transaction() as change_session:                  
                change_session['username'] = 'user1'
                change_session['title'] = 'title'
                change_session['artist'] = 'artist'
                change_session['department'] = 'department'
                change_session['creditLine'] = 'creditLine'
                change_session['image_link'] = ''
                change_session['image_link_full'] = ''
            user1 = User(username='user1', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="One", share='No', collection=1)
            db.session.add(user1)
            db.session.commit()
            res = client.get('/artwork/addtocollection/12345')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/user/user1')
            
    def test_artwork_add_to_collection_redirect(self):
        with app.test_client() as client:
            """Check the redirect"""
            with client.session_transaction() as change_session:                
                change_session['username'] = 'user1'
                change_session['title'] = 'title'
                change_session['artist'] = 'artist'
                change_session['department'] = 'department'
                change_session['creditLine'] = 'creditLine'
                change_session['image_link'] = ''
                change_session['image_link_full'] = ''
            user1 = User(username='user1', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="One", share='No', collection=1)
            db.session.add(user1)
            db.session.commit()
            res = client.get('/artwork/addtocollection/12345', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("<h4>Here's your current collection. Your collection is # 1</h4>", html)

    def test_artwork_detail(self):
        with app.test_client() as client:
            """Display artwork image and details"""
            with client.session_transaction() as change_session:    
                change_session['username'] = 'user1'
            user1 = User(username='user1', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="One", share='No', collection=1)
            db.session.add(user1)
            db.session.commit()
            res = client.get('/artwork/detail/10159')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<p><a class="btn btn-primary btn-sm" href="/artwork/addtocollection/10159">Add to your collection</a></p>', html)          

    def test_editcomments(self):
        with app.test_client() as client:
            """User can add or edit comments"""
            with client.session_transaction() as change_session: 
                username1='user1'
                change_session['username'] = username1                
            user1 = User(username='user1', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="One", share='No', collection=1)
            art1 = Artwork(id=10159, title='title', artist='artist', image_link='https://images.metmuseum.org/CRDImages/eg/web-large/Images-Restricted.jpg')
            db.session.add_all([user1, art1])
            db.session.commit()
            userart1 = UserArtwork(username='user1', artwork_id=10159)
            db.session.add(userart1)
            db.session.commit()
            res = client.get('/artwork/editcomments/1')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2 class="join-message">Add or update your comments about this artwork.</h2>', html)

    def test_delete_artwork(self):
        with app.test_client() as client:
            """Remove art from collection"""
            with client.session_transaction() as change_session:                
                change_session['username'] = 'user1'
            user1 = User(username='user1', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="One", share='No', collection=1)
            art1 = Artwork(id=10159, title='title', artist='artist', image_link='https://images.metmuseum.org/CRDImages/eg/web-large/Images-Restricted.jpg')
            db.session.add_all([user1, art1])
            db.session.commit()
            userart1 = UserArtwork(username='user1', artwork_id=10159)
            db.session.add(userart1)
            db.session.commit()
            res = client.post('/artwork/removefromcollection/10159', data={'username': 'user1', 'artwork_id': 10159})
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/user/user1')

    def test_delete_artwork_redirect(self):
        with app.test_client() as client:
            """Check the redirect"""
            with client.session_transaction() as change_session:                
                change_session['username'] = 'user1'
            user1 = User(username='user1', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="One", share='No', collection=1)
            art1 = Artwork(id=10159, title='title', artist='artist', image_link='https://images.metmuseum.org/CRDImages/eg/web-large/Images-Restricted.jpg')
            db.session.add_all([user1, art1])
            db.session.commit()
            userart1 = UserArtwork(username='user1', artwork_id=10159)
            db.session.add(userart1)
            db.session.commit()
            res = client.post('/artwork/removefromcollection/10159', data={'username': 'user1', 'artwork_id': 10159}, follow_redirects=True)            
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<button class="btn btn-primary" type="submit" >Find some art!</button>', html)

########################################################################
# View and share collections
########################################################################

    def test_sharedcollection_no(self):
        with app.test_client() as client:
            """A user may have shared a collection with no artworks in it"""
            with client.session_transaction() as change_session:                
                change_session['username'] = 'user1'
            user1 = User(username='user1', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="One", share='No', collection=1)
            user2 = User(username='user2', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="Two", share='Yes', collection=2)
            db.session.add_all([user1, user2])
            db.session.commit()
            res = client.get('/sharedcollection/user2')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h4>U. T. has not added any artworks to a collection yet.</h4>', html)

    def test_sharedcollection_yes(self):
        with app.test_client() as client:
            """A user may have shared a collection with artworks in it"""
            with client.session_transaction() as change_session:                
                change_session['username'] = 'user1'
            user1 = User(username='user1', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="One", share='No', collection=1)
            user2 = User(username='user2', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="Two", share='Yes', collection=2)
            art1 = Artwork(id=10159, title='title', artist='artist', image_link='https://images.metmuseum.org/CRDImages/eg/web-large/Images-Restricted.jpg')
            db.session.add_all([user1, user2, art1])
            db.session.commit()
            userart1 = UserArtwork(username='user2', artwork_id=10159)
            db.session.add(userart1)
            db.session.commit()
            res = client.get('/sharedcollection/user2')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("<h4>Here's the artworks in collection # 2 by U. T.</h4>", html)

    def test_sharedcollections_both_shared(self):
        with app.test_client() as client:
            """The logged in user and at least one other user have shared their collections"""
            with client.session_transaction() as change_session:                
                change_session['username'] = 'user1'
            user1 = User(username='user1', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="One", share='Yes', collection=1)
            user2 = User(username='user2', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="Two", share='Yes', collection=2)
            art1 = Artwork(id=10159, title='title', artist='artist', image_link='https://images.metmuseum.org/CRDImages/eg/web-large/Images-Restricted.jpg')
            db.session.add_all([user1, user2, art1])
            db.session.commit()
            userart1 = UserArtwork(username='user1', artwork_id=10159)
            userart2 = UserArtwork(username='user2', artwork_id=10159)
            db.session.add(userart1, userart2)
            db.session.commit()
            res = client.get('/sharedcollections')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("<h3>Check out these shared collections:</h3>", html)
            self.assertIn('<span style="font-weight: bold">Collection # 2 by U. T.</span>', html)
            self.assertIn("Your shared collection # 1", html)
            
    def test_sharedcollections_you_shared(self):
        with app.test_client() as client:
            """The logged in user has shared their collection but no one else has"""
            with client.session_transaction() as change_session:                
                change_session['username'] = 'user1'
            user1 = User(username='user1', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="One", share='Yes', collection=1)
            user2 = User(username='user2', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="Two", share='No', collection=2)
            art1 = Artwork(id=10159, title='title', artist='artist', image_link='https://images.metmuseum.org/CRDImages/eg/web-large/Images-Restricted.jpg')
            db.session.add_all([user1, user2, art1])
            db.session.commit()
            userart1 = UserArtwork(username='user1', artwork_id=10159)            
            userart2 = UserArtwork(username='user2', artwork_id=10159)
            db.session.add(userart1, userart2)
            db.session.commit()
            res = client.get('/sharedcollections')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertNotIn("<h3>Check out these shared collections:</h3>", html)
            self.assertNotIn('<span style="font-weight: bold">Collection # 2 by U. T.</span>', html)
            self.assertIn("<h3>No one else has shared a collection yet.</h3>", html)
            self.assertIn("Your collection is shared # 1", html)

    def test_sharedcollections_they_shared(self):
        with app.test_client() as client:
            """The logged in user has not shared their collection but at least one other user has"""
            with client.session_transaction() as change_session:                
                change_session['username'] = 'user1'
            user1 = User(username='user1', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="One", share='No', collection=1)
            user2 = User(username='user2', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="Two", share='Yes', collection=2)
            art1 = Artwork(id=10159, title='title', artist='artist', image_link='https://images.metmuseum.org/CRDImages/eg/web-large/Images-Restricted.jpg')
            db.session.add_all([user1, user2, art1])
            db.session.commit()
            userart1 = UserArtwork(username='user1', artwork_id=10159)            
            userart2 = UserArtwork(username='user2', artwork_id=10159)
            db.session.add(userart1, userart2)
            db.session.commit()
            res = client.get('/sharedcollections')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("<h3>Check out these shared collections:</h3>", html)
            self.assertIn('<span style="font-weight: bold">Collection # 2 by U. T.</span>', html)
            self.assertNotIn("<h3>No one else has shared a collection yet.</h3>", html)
            self.assertNotIn("Your collection is shared # 1", html)

    def test_sharedcollections_neither_shared(self):
        with app.test_client() as client:
            """No users have shared their collections"""
            with client.session_transaction() as change_session:                
                change_session['username'] = 'user1'
            user1 = User(username='user1', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="One", share='No', collection=1)
            user2 = User(username='user2', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="Two", share='No', collection=2)
            art1 = Artwork(id=10159, title='title', artist='artist', image_link='https://images.metmuseum.org/CRDImages/eg/web-large/Images-Restricted.jpg')
            db.session.add_all([user1, user2, art1])
            db.session.commit()
            userart1 = UserArtwork(username='user1', artwork_id=10159)            
            userart2 = UserArtwork(username='user2', artwork_id=10159)
            db.session.add(userart1, userart2)
            db.session.commit()
            res = client.get('/sharedcollections')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertNotIn("<h3>Check out these shared collections:</h3>", html)
            self.assertNotIn('<span style="font-weight: bold">Collection # 2 of U. T.</span>', html)
            self.assertIn("<h3>No one else has shared a collection yet.</h3>", html)
            self.assertNotIn("Your collection is shared # 1", html)
            self.assertIn("Your collection is not shared", html)
            self.assertIn('<button class="btn btn-primary btn-sm btn-block" type="submit"> Share your collection</button>', html)

    def test_sharedcollections_you_have_no_art(self):
        with app.test_client() as client:
            """The logged in user has no art in their collection"""
            with client.session_transaction() as change_session:                
                change_session['username'] = 'user1'
            user1 = User(username='user1', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="One", share='No', collection=1)
            user2 = User(username='user2', password="$2b$12$It03ox3R80KNrj1FL3tJf.0aWmNAy93xnp4DG2ZgjipFE.t3vlAH2", first_name="User", last_name="Two", share='No', collection=2)
            art1 = Artwork(id=10159, title='title', artist='artist', image_link='https://images.metmuseum.org/CRDImages/eg/web-large/Images-Restricted.jpg')
            db.session.add_all([user1, user2, art1])
            db.session.commit()            
            userart2 = UserArtwork(username='user2', artwork_id=10159)
            db.session.add(userart2)
            db.session.commit()
            res = client.get('/sharedcollections')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertNotIn("<h3>Check out these shared collections:</h3>", html)
            self.assertNotIn('<span style="font-weight: bold">Collection # 2 of U. T.</span>', html)
            self.assertIn("<h3>No one else has shared a collection yet.</h3>", html)
            self.assertNotIn("Your collection is shared # 1", html)
            self.assertNotIn("Your collection is not shared", html)
            self.assertNotIn('<button class="btn btn-primary btn-sm btn-block" type="submit"> Share your collection</button>', html)
            self.assertIn("<h4>You have not added any art to your collection.</h4>", html)
            self.assertIn('<button class="btn btn-primary" type="submit" >Find some art!</button>', html)
