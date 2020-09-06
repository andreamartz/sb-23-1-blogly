from unittest import TestCase

import datetime
from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for users."""

    def setUp(self):
        """Clean up any existing users before each test."""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction after each test."""

        db.session.rollback()

    def test_get_full_name(self):
        """Test the get_full_name() instance method."""
        user = User(first_name="TestUserFirst", last_name="TestUserLast")
        self.assertEquals(user.get_full_name(), "TestUserFirst TestUserLast")

    def test_full_name(self):
        """Test the full_name property."""
        user = User(first_name="TestUserFirst", last_name="TestUserLast")
        self.assertEquals(user.full_name, "TestUserFirst TestUserLast")


class PostModelTestCase(TestCase):
    """Tests for model for posts."""

    def setUp(self):
        """Clean up any existing posts before each test."""

        Post.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction after each test."""

        db.session.rollback()

    def test_formatted_date(self):
        """Test the formatted_date instance method."""
        date_time = datetime.datetime(2020, 1, 1, 0, 00, 00)

        post = Post(title="TestTitle", content="Content Goes Here",
                    created_at=date_time)

        self.assertEquals(post.formatted_date, "Wed Jan 1 2020, 12:00 AM")
