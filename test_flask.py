from unittest import TestCase
from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user1 = User(first_name="FirstName1", last_name="LastName1",
                     image_url="http://lorempixel.com/400/200/people/6/")
        user2 = User(first_name="FirstName2", last_name="LastName2",
                     image_url="http://lorempixel.com/400/200/people/7/")

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        self.user1 = user1
        self.user2 = user2
        self.user1_id = user1.id
        self.user2_id = user2.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('FirstName1', html)
            self.assertIn('LastName1', html)
            self.assertIn('FirstName2', html)
            self.assertIn('LastName2', html)

    def test_users_user_id(self):
        """Test the user details view for a specific user"""
        with app.test_client() as client:
            resp1 = client.get(f"/users/{self.user1_id}")
            html1 = resp1.get_data(as_text=True)
            resp2 = client.get(f"/users/{self.user2_id}")
            html2 = resp2.get_data(as_text=True)

            self.assertEqual(resp1.status_code, 200)
            self.assertIn('<h1>FirstName1 LastName1</h1>', html1)

            self.assertEqual(resp2.status_code, 200)
            self.assertIn('<h1>FirstName2 LastName2</h1>', html2)

            self.assertIn(self.user1.image_url, html1)
            self.assertIn(self.user2.image_url, html2)

    def test_users_user_id_edit(self):
        """Test the post route for editing a user's info."""
        with app.test_client() as client:
            user_id = 1
            d = {"first-name": "NewFirst",
                 "last-name": "NewLast", "profile-image": "http://lorempixel.com/400/200/people/8/"}
            resp = client.post(
                f"/users/{self.user1_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            # self.assertIn('<h1>FirstName1 LastName1</h1>', html)

            self.assertIn("NewFirst NewLast</a>", html)

    def test_add_user(self):
        """Test the post route for adding a new user."""
        with app.test_client() as client:
            d = {"first-name": "FirstName3", "last-name": "LastName3",
                 "profile-image": "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"}

            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("FirstName3 LastName3</a>", html)
