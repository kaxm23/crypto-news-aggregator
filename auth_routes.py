from flask import Blueprint, request, jsonify
from models import db, User
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
        
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'message': 'Logged in successfully'})
        
    return jsonify({'error': 'Invalid credentials'}), 401

@auth.route('/profile', methods=['GET'])
@login_required
def get_profile():
    # Implementation for getting user profile
    pass

@auth.route('/favorites', methods=['POST'])
@login_required
def add_favorite():
    # Implementation for adding favorite cryptocurrencies
    pass
