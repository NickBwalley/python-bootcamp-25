# blueprints/auth/routes.py
from flask import render_template, redirect, url_for, flash, request, session
from . import auth_bp  # Import the blueprint object

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Authentication logic
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('logged_in', None)  
    session.pop('username', None)
    flash('You have been logged out')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Registration logic
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match')
            return render_template('auth/register.html')
            
        # Add user to database logic
        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')