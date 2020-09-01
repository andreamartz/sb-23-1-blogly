"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "supersecretcodefordebugtoolbar"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home():
    """Shows list of all users in db"""
    return redirect('/users')


@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Shows details about user"""
    user = User.query.get_or_404(user_id)
    return render_template('user-details.html', user=user)


@app.route('/users/new')
def show_new_user_form():
    """Shows add form for new users"""
    return render_template('add-user.html')


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

    return redirect(f'/users')


@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """Shows user edit page"""
    user = User.query.get_or_404(user_id)
    # NOTE: handle the situation where user_id is not valid
    return render_template('edit-user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Handle form submission to update a user.
    Redirect to list of users"""

    user = User.query.get_or_404(user_id)

    # Get form info
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["profile-image"] or None

    # NOTE: Make sure to not submit a new record
    # NOTE: Make sure to not edit the user to be an empty record

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
