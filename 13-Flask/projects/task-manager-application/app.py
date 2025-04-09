# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Database setup
def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT,
        status TEXT DEFAULT 'pending',
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user:
            flash('Username already exists')
            conn.close()
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Logged in successfully!')
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# Task routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE user_id = ? ORDER BY due_date', 
                       (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('dashboard.html', tasks=tasks)

@app.route('/task/new', methods=['GET', 'POST'])
def new_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO tasks (title, description, due_date, user_id) VALUES (?, ?, ?, ?)',
                   (title, description, due_date, session['user_id']))
        conn.commit()
        conn.close()
        
        flash('Task created successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('new_task.html')

@app.route('/task/<int:id>/edit', methods=['GET', 'POST'])
def edit_task(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ? AND user_id = ?', 
                      (id, session['user_id'])).fetchone()
    
    if not task:
        conn.close()
        flash('Task not found')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        status = request.form['status']
        
        conn.execute('UPDATE tasks SET title = ?, description = ?, due_date = ?, status = ? WHERE id = ?',
                   (title, description, due_date, status, id))
        conn.commit()
        conn.close()
        
        flash('Task updated successfully!')
        return redirect(url_for('dashboard'))
    
    conn.close()
    return render_template('edit_task.html', task=task)

@app.route('/task/<int:id>/delete', methods=['POST'])
def delete_task(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ? AND user_id = ?', (id, session['user_id']))
    conn.commit()
    conn.close()
    
    flash('Task deleted successfully!')
    return redirect(url_for('dashboard'))

# Helper template filters
@app.template_filter('format_date')
def format_date(date_str):
    if date_str:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    return ""

if __name__ == '__main__':
    app.run(debug=True)