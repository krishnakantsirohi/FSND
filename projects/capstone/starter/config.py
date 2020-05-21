import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True


# Connect to the database
class DatabaseConfig:
    SECRET_KEY = os.urandom(32)
    DATABASE_NAME = 'capstone'
    username = 'postgres'
    password = '1234'
    url = 'localhost:5432'
    SQLALCHEMY_DATABASE_URI = 'postgres://{}:{}@{}/{}'.format(username, password, url, DATABASE_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
