import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, Profile

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['MAILTRAP_SMTP_USER'] = None  # Disable email in tests
    
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

class TestAuth:
    def test_register_success(self, client):
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        assert response.status_code == 201
        assert 'user_id' in response.json
        assert 'message' in response.json
    
    def test_register_duplicate_email(self, client):
        client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        assert response.status_code == 400
    
    def test_register_invalid_email(self, client):
        response = client.post('/api/auth/register', json={
            'email': 'invalid-email',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        assert response.status_code == 400
    
    def test_register_password_mismatch(self, client):
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'different'
        })
        assert response.status_code == 400
    
    def test_login_success(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
        
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        assert response.status_code == 200
        assert 'token' in response.json
        assert 'user' in response.json
    
    def test_login_wrong_password(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
        
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        assert response.status_code == 401
    
    def test_login_unverified_email(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
                is_verified=False
            )
            db.session.add(user)
            db.session.commit()
        
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        assert response.status_code == 401
        assert 'verify' in response.json['errors']['general'][0].lower()


class TestProfile:
    def test_create_profile_unauthorized(self, client):
        response = client.post('/api/profile', json={
            'name': 'John',
            'age': 25,
            'interests': 'hiking, reading, music'
        })
        assert response.status_code == 401
    
    def test_create_profile_success(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
        
        login_response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        token = login_response.json['token']
        
        response = client.post('/api/profile', 
            json={
                'name': 'John Doe',
                'age': 25,
                'bio': 'I love hiking',
                'location': 'New York',
                'interests': 'hiking, reading, music, cooking, travel',
                'gender': 'male',
                'gender_preference': 'all',
                'relationship_goal': 'serious_relationship',
                'occupation': 'Developer',
                'visibility': True
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 201
        assert response.json['name'] == 'John Doe'
        assert response.json['age'] == 25
    
    def test_create_profile_insufficient_interests(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
        
        login_response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        token = login_response.json['token']
        
        response = client.post('/api/profile', 
            json={
                'name': 'John',
                'age': 25,
                'interests': 'hiking, reading'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 400
    
    def test_get_profile(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
            
            profile = Profile(
                user_id=user.id,
                name='John Doe',
                age=25,
                interests=['hiking', 'reading', 'music']
            )
            db.session.add(profile)
            db.session.commit()
        
        login_response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        token = login_response.json['token']
        
        response = client.get('/api/profile',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        assert response.json['name'] == 'John Doe'
    
    def test_view_other_profile_public(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
            
            profile = Profile(
                user_id=user.id,
                name='John Doe',
                age=25,
                visibility=True,
                interests=['hiking']
            )
            db.session.add(profile)
            db.session.commit()
            profile_id = profile.id
        
        response = client.get(f'/api/profile/{profile_id}')
        assert response.status_code == 200
        assert response.json['name'] == 'John Doe'
    
    def test_view_other_profile_private(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
            
            profile = Profile(
                user_id=user.id,
                name='John Doe',
                age=25,
                visibility=False,
                interests=['hiking']
            )
            db.session.add(profile)
            db.session.commit()
            profile_id = profile.id
        
        response = client.get(f'/api/profile/{profile_id}')
        assert response.status_code == 403


class TestEmailVerification:
    def test_verify_email_success(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
                verification_token='test_token_123'
            )
            db.session.add(user)
            db.session.commit()
        
        response = client.get('/api/auth/verify/test_token_123')
        assert response.status_code == 200
        
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            assert user.is_verified == True
            assert user.verification_token is None
    
    def test_verify_email_invalid_token(self, client):
        response = client.get('/api/auth/verify/invalid_token')
        assert response.status_code == 404
