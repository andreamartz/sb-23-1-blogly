"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "supersecretcodefordebugtoolbar"
# Having the Debug Toolbar show redirects explicitly is often useful.  To turn it on, comment out this line:
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home():
    """Shows list of all users in db"""
    return redirect('/users')


@app.route('/users', methods=["GET"])
def list_users():
    """Shows list of all users in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/list.html', users=users)


@app.route('/users/<int:user_id>', methods=["GET"])
def show_user(user_id):
    """Shows details about user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/user-details.html', user=user)


@app.route('/users/new', methods=["GET"])
def show_new_user_form():
    """Shows add form for new users"""
    return render_template('users/add-user.html')


@app.route('/users/new', methods=["POST"])
def add_user():
    """Adds a new user and redirects to list of users"""

    # Get form info
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["profile-image"] or None

    # Create new user instance
    new_user = User(first_name=first_name,
                    last_name=last_name,
                    image_url=image_url)
    # Add to db
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/edit', methods=["GET"])
def show_edit_user(user_id):
    """Shows user edit page"""
    user = User.query.get_or_404(user_id)
    # NOTE: handle the situation where user_id is not valid
    return render_template('users/edit-user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Handle form submission to update a user.
    Redirect to list of users"""

    user = User.query.get_or_404(user_id)

    # Get form info
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["profile-image"] or None

    # Add to db
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

# UNTESTED BELOW


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes the user"""
    user = User.query.filter_by(id=user_id)

    user.delete()
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def show_new_post_form(user_id):
    """Show form to add a post for that user."""
    user = User.query.get_or_404(user_id)
    return render_template('/posts/add-post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Handle form submission to add a post.
    Redirect to the user detail page."""
    user = User.query.get_or_404(user_id)

    # Get form info
    title = request.form["title"]
    content = request.form["content"]

    # Create new user instance
    new_post = Post(title=title,
                    content=content,
                    user=user)

    # Add to db
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

# Posts routes


@app.route('/posts/<int:post_id>', methods=["GET"])
def show_post(post_id):
    """Show a post.
    Show buttons to edit and delete the post."""
    post = Post.query.get_or_404(post_id)
    return render_template("/posts/post-details.html", post=post)


@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def show_post_edit_form(post_id):
    """Show form to edit a post.
    Also offer option to cancel (and go back to user page)."""
    post = Post.query.get_or_404(post_id)
    return render_template('/posts/edit-post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_edits(post_id):
    """Handel editing of a post.
    Redirect back to the post view."""

    post = Post.query.get_or_404(post_id)

    # Get form info
    post.title = request.form["title"]
    post.content = request.form["content"]

    # Add to db
    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")

