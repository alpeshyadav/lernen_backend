from flask import Blueprint, request, jsonify, g
from models import Student
from keys import SECRET
from utils import checkpw
import bcrypt
import json
import jwt
from middleware.login import user_login_required, user_is_authorized
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

user_routes = Blueprint('user_routes', __name__)


@user_routes.route("/api/user/signup", methods=['POST'])
def admsignup():
   
    try:
        username = request.json['username']
        fname = request.json['fname']
        if Student.query.get(username=username):
            raise Exception('Username taken. Please choose another username.')
        unhashed = request.json['password']
        if not checkpw(unhashed):
            raise Exception('Password must be at least 6 characters long and must contain a number.')
        password = bcrypt.hashpw(unhashed.encode(), bcrypt.gensalt())
        user = Student(username=username, fname=fname, password=password)
        db.add(user)
        db.commit()
        token = jwt.encode({"id": str(user.id), "username": user.username, "fname": user.fname}, SECRET, algorithm='HS256')
        admdict = json.loads(user.to_json())
        del admdict['password']
        return jsonify({"result": admdict, "token": token.decode()}), 200
    except KeyError:
        return jsonify({"error": "Need all values"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

        return jsonify({"error": str(e)}), 400

@user_routes.route('/api/user/login', methods=['POST'])
def login():
    
    try:
        username = request.json['username']
        password = request.json['password']
        user = Student.query.get(username=username)
        if not user:
            raise Exception("Username or password incorrect")
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            token = jwt.encode({"id": str(user.id), "username": user.username, "fname": user.fname}, SECRET, algorithm='HS256')
            admdict = json.loads(user.to_json())
            del admdict['password']
            return jsonify({"result": admdict, "token": token.decode()}), 200
        raise Exception("Username or password incorrect")
    except KeyError:
        return jsonify({"error": "Need all values"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 404