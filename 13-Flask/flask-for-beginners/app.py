from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'Learn!ngfl4sk'  # Required for session management

# Home route
@app.route('/')
def home():
    return '<h1>Welcome! Go to <a href="/login">/login</a> to log in.</h1>'

# Static route example
@app.route('/about')
def about():
    return 'This is the about page'

# Dynamic route example
@app.route('/user/<username>')
def show_user_profile(username):
    return f'User: {username}'

# Jinja2 templating example
@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)

# Login route - GET and POST handling
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Grab user input from the form
        username = request.form['username']
        password = request.form['password']
        
        # You can validate credentials here (e.g., check against a database)
        session['username'] = username  # Save to session
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')  # Show login form

# Dashboard route - only visible if logged in
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f'''
            <h2>Logged in as {session["username"]}</h2>
            <a href="/logout">Logout</a>
        '''
    return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
