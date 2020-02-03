import os

class Config(object):
    DEBUG = True
    SECRET_KEY = os.urandom(12)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Alpesh@4599@localhost:5432/postgres"