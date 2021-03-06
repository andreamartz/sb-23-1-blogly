"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "supersecretcodefordebugtoolbar"

# Having the Debug Toolbar show redirects explicitly is often useful.  Turned on (True) is the default. To turn it off, uncomment this line:
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home():
    """Shows list of the five most recent posts."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5)

    return render_template('posts/homepage.html', posts=posts)


@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors by showing custom 404 page."""

    return render_template('404.html'), 404

# Users routes


@app.route('/users', methods=["GET"])
def list_users():
    """Shows list of all users in db"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/list.html', users=users)


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

    flash(f"User {new_user.full_name} added.")

    return redirect('/users')


@app.route('/users/<int:user_id>', methods=["GET"])
def show_user(user_id):
    """Shows details about user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/user-details.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["GET"])
def show_edit_user(user_id):
    """Shows user edit page"""

    user = User.query.get_or_404(user_id)
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

    flash(f"User {user.full_name} edited.")

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes the user"""
    # WORKS:
    user = User.query.get_or_404(user_id)
    db.session.delete(user)


    db.session.commit()
    flash(f"User {user.full_name} deleted.")

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def show_new_post_form(user_id):
    """Show form to add a post for that user."""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('/posts/add-post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Handle form submission to add a post.
    Redirect to the user detail page."""

    user = User.query.get_or_404(user_id)

    # Get form info (except tag checkboxes)
    title = request.form["title"]
    content = request.form["content"]

    # Get selected tags from form
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    # Create new user instance
    new_post = Post(title=title,
                    content=content,
                    user=user,
                    tags=tags)

    # Add to db
    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' added.")

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
    tags = Tag.query.all()
    return render_template('/posts/edit-post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_edits(post_id):
    """Handle editing of a post.
    Redirect back to the post view."""

    post = Post.query.get_or_404(post_id)

    # Get form info (except tags)
    post.title = request.form["title"]
    post.content = request.form["content"]

    # Get selected tags from form
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    # Add to db
    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete the post."""
    # WORKS:
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)

    db.session.commit()
    flash(f"Post '{ post.title }' deleted.")

    return redirect(f"/users/{ post.user_id }")


# Tag routes
@app.route('/tags', methods=["GET"])
def list_tags():
    """Shows list of all tags in db"""

    tags = Tag.query.all()
    return render_template('tags/list-tags.html', tags=tags)


@app.route('/tags/<int:tag_id>', methods=["GET"])
def show_tag(tag_id):
    """Show tag details."""

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template('/tags/tag-details.html', tag=tag, posts=posts)


@app.route('/tags/new', methods=["GET", "POST"])
def add_tag():
    """Show form to add a new tag (GET).
    Process submitted form data (POST)."""

    if request.method == 'POST':
        name = request.form["name"]
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()
        flash(f'Tag {new_tag.name} was created.')
        return redirect('/tags')
    else:
        return render_template('/tags/add-tag.html')


@app.route('/tags/<int:tag_id>/edit', methods=["GET", "POST"])
def edit_tag(tag_id):
    """Show form to edit a tag (GET).
    Process submitted form data (POST)."""

    tag = Tag.query.get_or_404(tag_id)

    if request.method == 'POST':
        orig_name = tag.name

        # Get form info
        tag.name = request.form["name"]
        new_name = tag.name

        # Add to db
        db.session.add(tag)
        db.session.commit()

        flash(f"Tag { orig_name } was successfully changed to { new_name }.")

        return redirect("/tags")

    else:
        return render_template("/tags/edit-tag.html", tag=tag)


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    name = tag.name

    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{ tag.name }' deleted.")

    return redirect('/tags')
