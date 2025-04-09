import os

class Config:
    SECRET_KEY = os.urandom(24)  # Random secret key
    SQLALCHEMY_DATABASE_URI = "sqlite:///passwords.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
