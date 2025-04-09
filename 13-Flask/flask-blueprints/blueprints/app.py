# app.py
from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # For session management
    
    # Register blueprints
    from blueprints.auth import auth_bp
    from blueprints.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    
    # Main routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)