"""Models for Blogly."""

# import Python module datetime
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


def connect_db(app):
    """Connects the database to the Flask app.
    This function should be called from the Flask app."""
    db.app = app
    db.init_app(app)

#  Models are below


class User(db.Model):
    """User.  User can have many posts."""
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                           nullable=False)

    last_name = db.Column(db.String(50),
                          nullable=False)

    image_url = db.Column(db.String(250), nullable=False,
                          default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")

    def __repr__(self):
        u = self
        return f"<User id={u.id} name={u.name} species={u.species} hunger={u.hunger}>"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Post. Post can have one user(i.e., the author)."""
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.Text,
                      nullable=False,
                      unique=True)

    content = db.Column(db.Text,
                        nullable=False)

    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))

    # each post will have a user attribute based on the foreign key
    user = db.relationship('User', backref='posts')

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} created_at={p.created_at}>"

    @property
    def formatted_date(self):
        """Create a user-friendly formatted date."""
        p = self
        return p.created_at.strftime("%a %b %-d %Y, %-I:%M %p")
