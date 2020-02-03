from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)

# create an engine

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:Alpesh@4599@localhost:5432/postgres'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
db.init_app(app)
CORS(app)

app.register_blueprint(admin_routes)
app.register_blueprint(user_routes)


def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
