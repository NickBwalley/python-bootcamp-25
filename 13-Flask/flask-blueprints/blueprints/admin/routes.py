# blueprints/admin/routes.py
from flask import render_template, redirect, url_for, flash, session
from . import admin_bp
from functools import wraps

# Custom decorator for admin routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or session.get('username') != 'admin':
            flash('You must be logged in as an admin to view this page')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/users')
@admin_required
def users():
    # Fetch users from database
    users_list = [
        {'id': 1, 'username': 'admin', 'email': 'admin@example.com'},
        {'id': 2, 'username': 'user1', 'email': 'user1@example.com'},
        {'id': 3, 'username': 'user2', 'email': 'user2@example.com'}
    ]
    return render_template('admin/users.html', users=users_list)