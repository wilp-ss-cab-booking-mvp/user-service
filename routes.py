#API Logic
from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token
from config import JWT_SECRET

bp = Blueprint('user_bp', __name__)

''' Register endpoint
Accepts username and password

Checks for duplicates

Saves new user to DB
'''
@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"message": "User already exists"}), 400

    user = User(username=data["username"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered"}), 201

'''Login endpoint
Authenticates user
If valid, creates JWT token
Returns token to be used in headers for future requests
'''
@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"], password=data["password"]).first()
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=user.username)
    return jsonify({"token": token}), 200
