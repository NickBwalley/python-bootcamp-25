# blueprints/auth/__init__.py
from flask import Blueprint

# Create a blueprint named 'auth'
# The first parameter is the blueprint's name
# The second parameter is the import name (usually __name__)
# The third parameter specifies the blueprint's template folder
auth_bp = Blueprint('auth', __name__, 
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/auth/static')

# Import routes at the bottom to avoid circular imports
from . import routes