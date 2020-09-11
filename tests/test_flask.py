from unittest import TestCase
from app import app
from models import db, User, Post
import datetime

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
        """Add sample users and posts."""

        Post.query.delete()
        User.query.delete()
        db.session.commit()

        date_time1 = datetime.datetime(2020, 1, 1, 0, 0, 0)
        date_time2 = datetime.datetime(2020, 1, 1, 0, 0, 1)

        user1 = User(first_name="FirstName1", last_name="LastName1",
                     image_url="http://lorempixel.com/400/200/people/6/")
        user2 = User(first_name="FirstName2", last_name="LastName2",
                     image_url="http://lorempixel.com/400/200/people/7/")

        db.session.add_all([user1, user2])
        db.session.commit()

        post1 = Post(title="Title1", content="Content1",
                     user_id=user2.id, created_at=date_time1)
        post2 = Post(title="Title2", content="Content2",
                     user_id=user2.id, created_at=date_time2)

        db.session.add_all([post1, post2])
        db.session.commit()

        self.user1 = user1
        self.user2 = user2

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


class PostViewsTestCase(TestCase):
    """Tests for views for Posts"""

    def setUp(self):
        """Add sample users and posts."""

        Post.query.delete()
        User.query.delete()
        db.session.commit()

        date_time = datetime.datetime(2020, 1, 1, 0, 00, 00)

        user1 = User(first_name="FirstName1", last_name="LastName1",
                     image_url="http://lorempixel.com/400/200/people/6/", id=1)
        user2 = User(first_name="FirstName2", last_name="LastName2",
                     image_url="http://lorempixel.com/400/200/people/7/", id=2)

        post1 = Post(title="Title1", content="Content1",
                     user_id=2, created_at=date_time)
        post2 = Post(title="Title2", content="Content2",
                     user_id=2, created_at=date_time)

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()

        self.user1 = user1
        self.user2 = user2
        self.user1_id = user1.id
        self.user2_id = user2.id

        self.post1 = post1
        self.post2 = post2
        self.post1_id = post1.id
        self.post2_id = post2.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Title1', html)
            self.assertIn('Content1', html)
            self.assertIn('Title2', html)
            self.assertIn('Content2', html)
            self.assertIn('Wed Jan 1 2020, 12:00 AM', html)

    def test_posts_post_id(self):
        """Test the post details view for a specific post"""
        with app.test_client() as client:
            resp1 = client.get(f"/posts/{self.post1_id}")
            html1 = resp1.get_data(as_text=True)
            resp2 = client.get(f"/posts/{self.post2_id}")
            html2 = resp2.get_data(as_text=True)

            self.assertEqual(resp1.status_code, 200)
            self.assertIn('<h1>Title1</h1>', html1)

            self.assertEqual(resp2.status_code, 200)
            self.assertIn('<h1>Title2</h1>', html2)

    def test_delete_post(self):
        """Test post deletion."""
        with app.test_client() as client:
            post_id = 1
            post = Post.query.get_or_404(post_id)

            d = {"title": "Title1", "content": "Content1",
                 "created_at": date_time, "user_id": 2}
            resp = client.post(
                f"/posts/{self.post_id}/delete", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>FirstName1 LastName1</h1>', html)
            self.assertIn('<h2 class="mt-4">Posts</h2>', html)

            # Test that the user is flashed a message saying that the deletion occurred.
            self.assertIn("<p>Post 'Title1' deleted.</p>")

            # Test that this post is no longer in the database.
