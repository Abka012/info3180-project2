import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, Profile


def create_user(app, email, is_verified=True):
    """Create a test user."""
    from app import bcrypt
    
    with app.app_context():
        user = User(
            email=email,
            password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
            is_verified=is_verified
        )
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user.id


def create_profile(app, user_id, **kwargs):
    """Create a test profile with customizable fields."""
    with app.app_context():
        defaults = {
            'user_id': user_id,
            'name': f'User {user_id}',
            'age': 25,
            'bio': 'Test bio',
            'location': 'New York',
            'geo_preferences': 'anywhere',
            'latitude': kwargs.get('latitude', 40.7128),
            'longitude': kwargs.get('longitude', -74.0060),
            'location_radius': kwargs.get('location_radius', 50),
            'preferred_age_min': kwargs.get('preferred_age_min', 18),
            'preferred_age_max': kwargs.get('preferred_age_max', 50),
            'interests': kwargs.get('interests', ['hiking', 'reading', 'music']),
            'gender': kwargs.get('gender', 'male'),
            'gender_preference': kwargs.get('gender_preference', 'all'),
            'relationship_goal': kwargs.get('relationship_goal', 'serious_relationship'),
            'occupation': kwargs.get('occupation', 'Developer'),
            'visibility': kwargs.get('visibility', True)
        }
        
        profile = Profile(**defaults)
        db.session.add(profile)
        db.session.commit()
        db.session.refresh(profile)
        return profile


def get_token(client, email):
    """Get authentication token for a user."""
    response = client.post('/api/auth/login', json={
        'email': email,
        'password': 'password123'
    })
    return response.json['token']


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['MAILTRAP_SMTP_USER'] = None
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def user1(app):
    """Create first test user."""
    return create_user(app, 'user1@test.com')


@pytest.fixture
def user2(app):
    """Create second test user."""
    return create_user(app, 'user2@test.com')


@pytest.fixture
def user3(app):
    """Create third test user."""
    return create_user(app, 'user3@test.com')


@pytest.fixture
def profile1(app, user1):
    """Create profile for user1."""
    return create_profile(app, user1, 
        name='John',
        age=25,
        latitude=40.7128,
        longitude=-74.0060,
        location_radius=50,
        interests=['hiking', 'reading', 'music'],
        gender='male',
        gender_preference='female',
        relationship_goal='serious_relationship'
    )


@pytest.fixture
def profile2(app, user2):
    """Create profile for user2."""
    return create_profile(app, user2,
        name='Jane',
        age=28,
        latitude=40.7128,
        longitude=-74.0060,
        location_radius=50,
        interests=['hiking', 'cooking', 'travel'],
        gender='female',
        gender_preference='male',
        relationship_goal='serious_relationship'
    )


@pytest.fixture
def profile3(app, user3):
    """Create profile for user3 - incompatible."""
    return create_profile(app, user3,
        name='Bob',
        age=55,
        latitude=34.0522,
        longitude=-118.2437,
        location_radius=25,
        interests=['gaming'],
        gender='male',
        gender_preference='all',
        relationship_goal='friendship'
    )


@pytest.fixture
def token1(client, user1):
    """Get token for user1."""
    return get_token(client, 'user1@test.com')


@pytest.fixture
def token2(client, user2):
    """Get token for user2."""
    return get_token(client, 'user2@test.com')


@pytest.fixture
def token3(client, user3):
    """Get token for user3."""
    return get_token(client, 'user3@test.com')
