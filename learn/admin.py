from flask import Blueprint, request, jsonify, g
from models import Admin, Student
from keys import SECRET
from utils import checkpw
from middleware.login import admin_login_required, admin_is_authorized
import bcrypt
import json
import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

admin_routes = Blueprint('admin_routes', __name__)


engine = create_engine("postgresql://postgres:password@localhost:5432/postgres")
db = scoped_session(sessionmaker(bind=engine))

@admin_routes.route("/api/admin/signup", methods=['POST'])
def admsignup():
   
    try:
        username = request.json['username']
        fname = request.json['fname']
        if Admin.query.get(username=username):
            raise Exception('Username taken. Please choose another username.')
        unhashed = request.json['password']
        if not checkpw(unhashed):
            raise Exception('Password must be at least 6 characters long and must contain a number.')
        password = bcrypt.hashpw(unhashed.encode(), bcrypt.gensalt())
        admin = Admin(username=username, fname=fname, password=password)
        db.add(admin)
        db.commit()
        token = jwt.encode({"id": str(admin.id), "username": admin.username, "fname": admin.fname}, SECRET, algorithm='HS256')
        admdict = json.loads(admin.to_json())
        del admdict['password']
        return jsonify({"result": admdict, "token": token.decode()}), 200
    except KeyError:
        return jsonify({"error": "Need all values"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

        return jsonify({"error": str(e)}), 400

@admin_routes.route('/api/admin/login', methods=['POST'])
def login():
    
    try:
        username = request.json['username']
        password = request.json['password']
        admin = Admin.query.get(username=username)
        if not admin:
            raise Exception("Username or password incorrect")
        if bcrypt.checkpw(password.encode(), admin.password.encode()):
            token = jwt.encode({"id": str(admin.id), "username": admin.username, "fname": admin.fname}, SECRET, algorithm='HS256')
            admdict = json.loads(admin.to_json())
            del admdict['password']
            return jsonify({"result": admdict, "token": token.decode()}), 200
        raise Exception("Username or password incorrect")
    except KeyError:
        return jsonify({"error": "Need all values"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 404