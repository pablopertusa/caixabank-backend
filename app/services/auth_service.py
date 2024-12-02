from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import db, User
import uuid
from app.utils.validator import is_valid_email

def register_user(data):
    # Validate data
    if not data or "email" not in data or "password" not in data or "name" not in data:
        return {"error": "All fields are required."}, 400

    email = data.get("email").strip()
    password = data.get("password").strip()
    name = data.get("name").strip()

    if not email or not password or not name:
        return {"error": "No empty fields allowed."}, 400

    if not is_valid_email(email):
        return {"error": f"Invalid email: {email}"}, 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return {"error": "Email already exists."}, 400

    # Create new user
    hashed_password = generate_password_hash(password).decode("utf-8")
    user_id = str(uuid.uuid4())
    new_user = User(id=user_id, name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return {
        "name": name,
        "hashedPassword": hashed_password,
        "email": email,
    }, 201

def login_user(data):
    # Validate data
    if not data or "email" not in data or "password" not in data:
        return {"error": "Bad credentials."}, 401

    email = data.get("email").strip()
    password = data.get("password").strip()

    if not email or not password:
        return {"error": "Bad credentials."}, 401

    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": f"User not found for the given email: {email}"}, 400

    # Verify password
    if not check_password_hash(user.password, password):
        return {"error": "Bad credentials."}, 401
    
    user = User.query.filter_by(email=email).first()
    if user:
        id = user.id
    else: 
        return 500

    # Generate JWT token
    token = create_access_token(identity=str(id))
    return {"token": token}, 200
