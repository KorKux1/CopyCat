# OS
from os import environ

class Config():
    """ 
    This clase contains the app configurations
    """
    SECRET_KEY = environ['SECRET_KEY']