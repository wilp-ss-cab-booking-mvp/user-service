#API Logic
from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token
from config import JWT_SECRET
import requests
from flask_jwt_extended import jwt_required, get_jwt_identity


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

# list registered users
@bp.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([
        {"id": user.id, "username": user.username}
        for user in users
    ])


'''Fetch all bookings from booking service
Build a set of booked user_ids
Show only users who are NOT booked.'''
@bp.route('/free-users', methods=['GET'])
@jwt_required()  # Enforce that only logged-in users can call
def free_users():
    all_users = User.query.all()
    try:
        response = requests.get("http://booking:5000/active-bookings", timeout=5)
        response.raise_for_status()
        bookings = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Could not contact booking service", "details": str(e)}), 500

    booked_user_ids = {b["user_id"] for b in bookings}

    free_users = []
    for user in all_users:
        if user.id not in booked_user_ids:
            free_users.append({
                "id": user.id,
                "username": user.username
            })

    return jsonify(free_users)