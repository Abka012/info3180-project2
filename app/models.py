from app import db
from datetime import datetime
import secrets
import string

def generate_verification_token():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64))

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(64), unique=True, default=generate_verification_token)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    profile = db.relationship('Profile', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'

class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    geo_preferences = db.Column(db.String(50), default='anywhere')
    
    interests = db.Column(db.JSON, default=list)
    
    profile_picture = db.Column(db.String(255))
    
    visibility = db.Column(db.Boolean, default=True)
    
    gender = db.Column(db.String(50))
    gender_preference = db.Column(db.String(50), default='all')
    
    relationship_goal = db.Column(db.String(50))
    occupation = db.Column(db.String(100))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'age': self.age,
            'bio': self.bio,
            'location': self.location,
            'geo_preferences': self.geo_preferences,
            'interests': self.interests or [],
            'profile_picture': self.profile_picture,
            'visibility': self.visibility,
            'gender': self.gender,
            'gender_preference': self.gender_preference,
            'relationship_goal': self.relationship_goal,
            'occupation': self.occupation,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Profile {self.name}>'
