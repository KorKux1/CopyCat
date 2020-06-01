# Flask
from flask import  Flask

# Bootstrap 
from flask_bootstrap import Bootstrap

# Config
from .config import  Config

def create_app():
    """
    This function create the flask apliciation and add blueprints. 
    
    Return: flask app aplication
    """
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    app.config.from_object(Config)

    return app
