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

    image_url = db.Column(db.Text, nullable=False,
                          default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"

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
                        db.ForeignKey('users.id'), nullable=False)

    posts_tags = db.relationship("PostTag",
                                 backref="post", cascade="all, delete-orphan")

    tags = db.relationship("Tag",
                           secondary="posts_tags", backref="posts")

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} created_at={p.created_at}>"

    @property
    def formatted_date(self):
        """Create a user-friendly formatted date."""
        p = self
        return p.created_at.strftime("%a %b %-d %Y, %-I:%M %p")


class Tag(db.Model):
    """Tag for posts. 
    A single tag can be on many posts.
    A single post can have many tags."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.Text,
                     unique=True,
                     nullable=False)

    posts_tags = db.relationship("PostTag",
                                 backref="tag",
                                 cascade="all, delete-orphan")

    def __repr__(self):
        t = self
        return f"<Tag id={t.id} name={t.name}>"


class PostTag(db.Model):
    """PostTag for joins"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)
