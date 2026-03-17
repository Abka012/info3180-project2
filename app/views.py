import os
import jwt
from datetime import datetime, timedelta, timezone
from flask import Blueprint, request, jsonify, current_app
from app import db, bcrypt
from app.models import User, Profile
from app.forms import RegistrationForm, LoginForm, ProfileForm
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

bp = Blueprint('main', __name__)

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(days=7),
        'iat': datetime.now(timezone.utc)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def send_email(to_email, subject, body):
    import time
    time.sleep(1)  # Rate limiting delay
    
    try:
        smtp_host = current_app.config.get('MAILTRAP_SMTP_HOST')
        smtp_port = current_app.config.get('MAILTRAP_SMTP_PORT')
        smtp_user = current_app.config.get('MAILTRAP_SMTP_USER')
        smtp_pass = current_app.config.get('MAILTRAP_SMTP_PASS')
        from_email = current_app.config.get('MAILTRAP_FROM_EMAIL')
        
        if not smtp_user or not smtp_pass:
            print(f"[MOCK EMAIL] To: {to_email}, Subject: {subject}")
            return True
        
        print(f"[EMAIL] Attempting to send to {to_email} via {smtp_host}:{smtp_port}")
        
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        
        print(f"[EMAIL] Successfully sent to {to_email}")
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email: {e}")
        return False

def allowed_file(filename):
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'webp'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

def get_user_from_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user = db.session.get(User, payload['user_id'])
        return user
    except:
        return None

@bp.route('/')
def index():
    return jsonify(message="Welcome to DriftDater API", version="1.0")

@bp.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    form = RegistrationForm(data=data)
    if not form.validate():
        return jsonify({'errors': form.errors}), 400
    
    if User.query.filter_by(email=form.email.data).first():
        return jsonify({'errors': {'email': ['This email is already registered']}}), 400
    
    password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    
    user = User(
        email=form.email.data,
        password_hash=password_hash
    )
    db.session.add(user)
    db.session.commit()
    
    verify_url = f"http://localhost:5173/verify/{user.verification_token}"
    
    email_body = f"""
    <html>
    <body>
        <h2>Welcome to DriftDater!</h2>
        <p>Thank you for registering. Please verify your email by clicking the link below:</p>
        <p><a href="{verify_url}">Verify Email</a></p>
        <p>Or copy this link: {verify_url}</p>
    </body>
    </html>
    """
    
    send_email(user.email, "Verify your DriftDater account", email_body)
    
    return jsonify({
        'message': 'Registration successful. Please check your email to verify your account.',
        'user_id': user.id
    }), 201

@bp.route('/api/auth/verify/<token>', methods=['GET'])
def verify_email(token):
    user = User.query.filter_by(verification_token=token).first()
    
    if not user:
        return jsonify({'error': 'Invalid verification token'}), 404
    
    if user.is_verified:
        return jsonify({'message': 'Email already verified'}), 200
    
    user.is_verified = True
    user.verification_token = None
    db.session.commit()
    
    return jsonify({'message': 'Email verified successfully'}), 200

@bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    form = LoginForm(data=data)
    if not form.validate():
        return jsonify({'errors': form.errors}), 400
    
    user = User.query.filter_by(email=form.email.data).first()
    
    if not user or not bcrypt.check_password_hash(user.password_hash, form.password.data):
        return jsonify({'errors': {'general': ['Invalid email or password']}}), 401
    
    if not user.is_verified:
        return jsonify({'errors': {'general': ['Please verify your email before logging in']}}), 401
    
    token = generate_token(user.id)
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'is_verified': user.is_verified,
            'has_profile': user.profile is not None
        }
    }), 200

@bp.route('/api/auth/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200

@bp.route('/api/auth/me', methods=['GET'])
def get_current_user():
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'is_verified': user.is_verified,
        'has_profile': user.profile is not None
    }), 200

@bp.route('/api/profile', methods=['GET'])
def get_profile():
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    profile = Profile.query.filter_by(user_id=user.id).first()
    
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    return jsonify(profile.to_dict()), 200

@bp.route('/api/profile', methods=['POST'])
def create_profile():
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    existing = Profile.query.filter_by(user_id=user.id).first()
    if existing:
        return jsonify({'error': 'Profile already exists. Use PUT to update.'}), 400
    
    data = request.get_json() or {}
    data['interests'] = data.get('interests', [])
    
    form = ProfileForm(data=data)
    if not form.validate():
        return jsonify({'errors': form.errors}), 400
    
    interests_list = [i.strip() for i in form.interests.data.split(',') if i.strip()]
    if len(interests_list) < 3:
        return jsonify({'errors': {'interests': ['Please add at least 3 interests']}}), 400
    
    profile = Profile(
        user_id=user.id,
        name=form.name.data,
        age=form.age.data,
        bio=form.bio.data,
        location=form.location.data,
        geo_preferences=form.geo_preferences.data,
        interests=interests_list,
        gender=form.gender.data,
        gender_preference=form.gender_preference.data,
        relationship_goal=form.relationship_goal.data,
        occupation=form.occupation.data,
        visibility=form.visibility.data
    )
    
    db.session.add(profile)
    db.session.commit()
    
    return jsonify(profile.to_dict()), 201

@bp.route('/api/profile', methods=['PUT'])
def update_profile():
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    profile = Profile.query.filter_by(user_id=user.id).first()
    
    if not profile:
        return jsonify({'error': 'Profile not found. Create one first.'}), 404
    
    data = request.get_json() or {}
    data['interests'] = data.get('interests', [])
    
    form = ProfileForm(data=data)
    if not form.validate():
        return jsonify({'errors': form.errors}), 400
    
    interests_list = [i.strip() for i in form.interests.data.split(',') if i.strip()]
    if len(interests_list) < 3:
        return jsonify({'errors': {'interests': ['Please add at least 3 interests']}}), 400
    
    profile.name = form.name.data
    profile.age = form.age.data
    profile.bio = form.bio.data
    profile.location = form.location.data
    profile.geo_preferences = form.geo_preferences.data
    profile.interests = interests_list
    profile.gender = form.gender.data
    profile.gender_preference = form.gender_preference.data
    profile.relationship_goal = form.relationship_goal.data
    profile.occupation = form.occupation.data
    profile.visibility = form.visibility.data
    
    db.session.commit()
    
    return jsonify(profile.to_dict()), 200

@bp.route('/api/profile/picture', methods=['POST'])
def upload_picture():
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    profile = Profile.query.filter_by(user_id=user.id).first()
    
    if not profile:
        return jsonify({'error': 'Create a profile first'}), 400
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f"user_{user.id}_{file.filename}")
        upload_folder = current_app.config.get('UPLOAD_FOLDER', './uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        profile.profile_picture = filename
        db.session.commit()
        
        return jsonify({
            'message': 'Profile picture uploaded',
            'filename': filename
        }), 200
    
    return jsonify({'error': 'Invalid file type'}), 400

@bp.route('/api/profile/<int:user_id>', methods=['GET'])
def view_other_profile(user_id):
    profile = db.session.get(Profile, user_id)
    
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    if not profile.visibility:
        user = get_user_from_token()
        if not user or user.id != user_id:
            return jsonify({'error': 'This profile is private'}), 403
    
    return jsonify(profile.to_dict()), 200

@bp.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
