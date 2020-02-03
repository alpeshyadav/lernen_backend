from config import Config
from models import db
from flask import Flask
from admin import admin_routes
from user import user_routes
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

app.register_blueprint(admin_routes)
app.register_blueprint(user_routes)



if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')