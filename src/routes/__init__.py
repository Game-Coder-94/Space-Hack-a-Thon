from flask import Blueprint

# Initialize the Blueprint for routes
app_routes = Blueprint('app_routes', __name__)

# Example route
@app_routes.route('/')
def home():
    return "Welcome to the Space Hack-a-Thon API!"