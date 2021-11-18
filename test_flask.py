from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UsersViewTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample pet."""

        User.query.delete()

        user1= User(first_name="TestUser", last_name="Test")
        user2=User(first_name="John", last_name="Doe")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        self.user1_id = user1.id
        self.user2_id = user2.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_homepage(self):
        """Show homepage"""
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            user1=(User.query.all()[0]) #TestUser Test
            user2=(User.query.all()[1]) #John Doe

            self.assertEqual(resp.status_code, 200)

            self.assertIn('<h1>Users',html) #Checks the headline
            self.assertIn('TestUser Test', html) #Checks TestUser Test exists
            self.assertIn('John Doe', html)
            self.assertIn('<button class="btn btn-primary">Add User',html)  #Checks Add User Button

            ordered_users=User.query.order_by(User.last_name.asc()).order_by(User.first_name.asc()).all()
            p=self

            self.assertEqual([f'{ordered_users[0]}',f'{ordered_users[1]}'], [f"<User id={user2.id} first_name={user2.first_name} last_name={user2.last_name} url_shortened={user2.image_url[:10]}>",
            f"<User id={user1.id} first_name={user1.first_name} last_name={user1.last_name} url_shortened={user1.image_url[:10]}>"])


    def test_addUserPage(self):
        """Show addUserPage"""
        with app.test_client() as client:
            response = client.get("/user/new")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code,200)
            self.assertIn('<form action="/user/new"', html)
            self.assertIn('<button type="submit" class="btn btn-secondary" name="cancel">Cancel', html)

    def test_invalidAddUserinputs(self):
        """Tests Invalid Add User Info"""
        with app.test_client() as client:

            #Checks empty first name field
            d = {"firstName":'',"lastName": "Test3", "imageURL": "https://media.istockphoto.com/photos/kitten-at-home-garden-wall-picture-id1273661469?b=1&k=20&m=1273661469&s=170667a&w=0&h=K-b-88J89oSBIwbD0WhhDoOvybcbjfePJoOHS0grHHA="}
            response1 = client.post("/user/new", data=d, follow_redirects=True)
            html1=response1.get_data(as_text=True)
            self.assertIn("Invalid Input: First Name is required!", html1)

            #Checks empty last name field
            d1= {"firstName": "Tester","lastName": "", "imageURL": "https://media.istockphoto.com/photos/kitten-at-home-garden-wall-picture-id1273661469?b=1&k=20&m=1273661469&s=170667a&w=0&h=K-b-88J89oSBIwbD0WhhDoOvybcbjfePJoOHS0grHHA="}
            response2 = client.post("/user/new", data=d1, follow_redirects=True)
            html2=response2.get_data(as_text=True)
            self.assertIn("Invalid Input: Last Name is required!", html2)
  
    
    def test_newUserAdded(self):
        """Checks New User Add Functionality"""
        with app.test_client() as client:
            d = {"firstName": "TestUser3", "lastName": "Test3", "imageURL": "https://media.istockphoto.com/photos/kitten-at-home-garden-wall-picture-id1273661469?b=1&k=20&m=1273661469&s=170667a&w=0&h=K-b-88J89oSBIwbD0WhhDoOvybcbjfePJoOHS0grHHA="}
            resp = client.post("/user/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<li>First Name: Testuser3", html)
            self.assertIn("<li>Last Name: Test3", html)


    def test_showUserInfo(self):
        """Checks User Info Page Functionality"""
        with app.test_client() as client:
            
            user1=User.query.all()[0]
            resp = client.get(f"/user/{user1.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<li>First Name: {user1.first_name}", html)
            self.assertIn(f"<li>Last Name: {user1.last_name}", html)
            self.assertIn('<button class="btn btn-warning">Edit User</button>', html)
            self.assertIn('<button class="btn btn-danger">Delete User</button>', html)
            self.assertIn('<button class="btn btn-secondary">Go to Main Page</button>', html)

    
    def test_deleteUser(self):
        """Checks Delete User Functionality"""

        with app.test_client() as client:
            
            #checks delete functionality
            deleted_user=User.query.all()[0]
            resp = client.post(f"/user/{deleted_user.id}/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertNotIn(f"<li>First Name: {deleted_user.first_name}", html)
            self.assertNotIn(f"<li>Last Name: {deleted_user.last_name}", html)


            #Checks redirect functionality
            deleted_user2=User.query.all()[0]
            resp = client.post(f"/user/{deleted_user2.id}/delete")
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location,"http://localhost/")


    def test_EditUser(self):
        """Checks Edit User Functionality"""

        with app.test_client() as client:
            editted_user=User.query.all()[0]

            name=editted_user.first_name
            surname=editted_user.last_name

            d = {"firstName": "Simba", "lastName": "Lion", "imageURL": "https://media.istockphoto.com/photos/kitten-at-home-garden-wall-picture-id1273661469?b=1&k=20&m=1273661469&s=170667a&w=0&h=K-b-88J89oSBIwbD0WhhDoOvybcbjfePJoOHS0grHHA="}
            resp = client.post(f"/user/{editted_user.id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<li>First Name: Simba", html)
            self.assertIn("<li>Last Name: Lion", html)

           
            self.assertNotIn(f"<li>First Name: {name}", html)
            self.assertNotIn(f"<li>Last Name: {surname}", html)



