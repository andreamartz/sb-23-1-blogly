from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Users."""

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
