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
            'password': 'TestPass123!',
            'confirm_password': 'TestPass123!'
        })
        assert response.status_code == 201
        assert 'user_id' in response.json
        assert 'message' in response.json
    
    def test_register_duplicate_email(self, client):
        client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'confirm_password': 'TestPass123!'
        })
        
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'confirm_password': 'TestPass123!'
        })
        assert response.status_code == 400
    
    def test_register_invalid_email(self, client):
        response = client.post('/api/auth/register', json={
            'email': 'invalid-email',
            'password': 'TestPass123!',
            'confirm_password': 'TestPass123!'
        })
        assert response.status_code == 400
    
    def test_register_password_mismatch(self, client):
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'confirm_password': 'DifferentPass1!'
        })
        assert response.status_code == 400
    
    def test_register_weak_password_too_short(self, client):
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'Short1!',
            'confirm_password': 'Short1!'
        })
        assert response.status_code == 400
        assert 'password' in response.json.get('errors', {})
    
    def test_register_weak_password_no_uppercase(self, client):
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'testpass123!',
            'confirm_password': 'testpass123!'
        })
        assert response.status_code == 400
        assert 'password' in response.json.get('errors', {})
    
    def test_register_weak_password_no_number(self, client):
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'TestPassword!',
            'confirm_password': 'TestPassword!'
        })
        assert response.status_code == 400
        assert 'password' in response.json.get('errors', {})
    
    def test_register_weak_password_no_special(self, client):
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'TestPassword123',
            'confirm_password': 'TestPassword123'
        })
        assert response.status_code == 400
        assert 'password' in response.json.get('errors', {})
    
    def test_login_success(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
        
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'TestPass123!'
        })
        assert response.status_code == 200
        assert 'token' in response.json
        assert 'user' in response.json
    
    def test_login_wrong_password(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
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
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
                is_verified=False
            )
            db.session.add(user)
            db.session.commit()
        
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'TestPass123!'
        })
        assert response.status_code == 401
        assert 'verify' in response.json['errors']['general'][0].lower()
    
    def test_login_nonexistent_user(self, client):
        response = client.post('/api/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'TestPass123!'
        })
        assert response.status_code == 401
    
    def test_login_missing_email(self, client):
        response = client.post('/api/auth/login', json={
            'password': 'TestPass123!'
        })
        assert response.status_code == 400
    
    def test_login_missing_password(self, client):
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com'
        })
        assert response.status_code == 400
    
    def test_logout(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
        
        response = client.post('/api/auth/logout')
        assert response.status_code == 200
        assert 'Logged out' in response.json['message']
    
    def test_resend_verification_success(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
                is_verified=False,
                verification_token='old_token'
            )
            db.session.add(user)
            db.session.commit()
        
        response = client.post('/api/auth/resend-verification', json={
            'email': 'test@example.com'
        })
        assert response.status_code == 200
        assert 'sent' in response.json['message'].lower()
    
    def test_resend_verification_already_verified(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
        
        response = client.post('/api/auth/resend-verification', json={
            'email': 'test@example.com'
        })
        assert response.status_code == 400
        assert 'already verified' in response.json['error'].lower()
    
    def test_resend_verification_nonexistent_user(self, client):
        response = client.post('/api/auth/resend-verification', json={
            'email': 'nonexistent@example.com'
        })
        assert response.status_code == 200
    
    def test_resend_verification_invalid_email(self, client):
        response = client.post('/api/auth/resend-verification', json={
            'email': 'invalid-email'
        })
        assert response.status_code == 400
    
    def test_resend_verification_missing_email(self, client):
        response = client.post('/api/auth/resend-verification', json={})
        assert response.status_code == 400
    
    def test_forgot_password_success(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
        
        response = client.post('/api/auth/forgot-password', json={
            'email': 'test@example.com'
        })
        assert response.status_code == 200
        assert 'sent' in response.json['message'].lower()
    
    def test_forgot_password_nonexistent_user(self, client):
        response = client.post('/api/auth/forgot-password', json={
            'email': 'nonexistent@example.com'
        })
        assert response.status_code == 200
    
    def test_forgot_password_invalid_email(self, client):
        response = client.post('/api/auth/forgot-password', json={
            'email': 'invalid-email'
        })
        assert response.status_code == 400
    
    def test_forgot_password_missing_email(self, client):
        response = client.post('/api/auth/forgot-password', json={})
        assert response.status_code == 400


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
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
        
        login_response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'TestPass123!'
        })
        token = login_response.json['token']
        
        response = client.post('/api/profile', 
            json={
                'name': 'John Doe',
                'age': 25,
                'bio': 'I love hiking',
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
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
        
        login_response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'TestPass123!'
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
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
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
            'password': 'TestPass123!'
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
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
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
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
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
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
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


class TestResetPassword:
    def test_reset_password_success(self, client, app):
        with app.app_context():
            from app import bcrypt
            from app.views import generate_token
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('OldPass123!').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.id
        
        with app.app_context():
            reset_token = generate_token(user_id, token_type='reset', expires_days=1)
        
        response = client.post('/api/auth/reset-password', json={
            'token': reset_token,
            'password': 'NewPass456!',
            'confirm_password': 'NewPass456!'
        })
        assert response.status_code == 200
        assert 'reset successfully' in response.json['message'].lower()
        
        login_response2 = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'NewPass456!'
        })
        assert login_response2.status_code == 200
    
    def test_reset_password_invalid_token(self, client):
        response = client.post('/api/auth/reset-password', json={
            'token': 'invalid_token',
            'password': 'NewPass456!',
            'confirm_password': 'NewPass456!'
        })
        assert response.status_code == 400
    
    def test_reset_password_weak_password(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('OldPass123!').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
        
        login_response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'OldPass123!'
        })
        token = login_response.json['token']
        
        response = client.post('/api/auth/reset-password', json={
            'token': token,
            'password': 'weak',
            'confirm_password': 'weak'
        })
        assert response.status_code == 400
        assert 'password' in response.json.get('errors', {})
    
    def test_reset_password_mismatch(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('OldPass123!').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
        
        login_response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'OldPass123!'
        })
        token = login_response.json['token']
        
        response = client.post('/api/auth/reset-password', json={
            'token': token,
            'password': 'NewPass456!',
            'confirm_password': 'DifferentPass1!'
        })
        assert response.status_code == 400
    
    def test_reset_password_missing_token(self, client):
        response = client.post('/api/auth/reset-password', json={
            'password': 'NewPass456!',
            'confirm_password': 'NewPass456!'
        })
        assert response.status_code == 400
    
    def test_reset_password_missing_passwords(self, client):
        response = client.post('/api/auth/reset-password', json={
            'token': 'some_token'
        })
        assert response.status_code == 400


class TestRefreshToken:
    def test_refresh_token_success(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.id
        
        response = client.post('/api/auth/refresh', json={
            'user_id': user_id
        })
        assert response.status_code == 200
        assert 'token' in response.json
        assert 'user' in response.json
    
    def test_refresh_token_invalid_user(self, client):
        response = client.post('/api/auth/refresh', json={
            'user_id': 99999
        })
        assert response.status_code == 404
    
    def test_refresh_token_missing_user_id(self, client):
        response = client.post('/api/auth/refresh', json={})
        assert response.status_code == 400


class TestCurrentUser:
    def test_get_current_user_success(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
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
            'password': 'TestPass123!'
        })
        token = login_response.json['token']
        
        response = client.get('/api/auth/me',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        assert response.json['email'] == 'test@example.com'
        assert response.json['name'] == 'John Doe'
        assert response.json['is_verified'] == True
        assert response.json['has_profile'] == True
    
    def test_get_current_user_unauthenticated(self, client):
        response = client.get('/api/auth/me')
        assert response.status_code == 401
    
    def test_get_current_user_invalid_token(self, client):
        response = client.get('/api/auth/me',
            headers={'Authorization': 'Bearer invalid_token'}
        )
        assert response.status_code == 401


class TestProfileUpdate:
    def test_update_profile_success(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
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
            'password': 'TestPass123!'
        })
        token = login_response.json['token']
        
        response = client.put('/api/profile',
            json={
                'name': 'Jane Doe',
                'age': 26,
                'bio': 'Updated bio',
                'interests': 'hiking, reading, music, cooking',
                'gender': 'female',
                'gender_preference': 'male',
                'relationship_goal': 'marriage',
                'occupation': 'Designer',
                'visibility': True
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        assert response.json['name'] == 'Jane Doe'
        assert response.json['age'] == 26
    
    def test_update_profile_not_found(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
        
        login_response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'TestPass123!'
        })
        token = login_response.json['token']
        
        response = client.put('/api/profile',
            json={'name': 'John'},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 404
    
    def test_update_profile_unauthorized(self, client):
        response = client.put('/api/profile',
            json={'name': 'John'},
            headers={'Authorization': 'Bearer invalid_token'}
        )
        assert response.status_code == 401
    
    def test_update_profile_insufficient_interests(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
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
            'password': 'TestPass123!'
        })
        token = login_response.json['token']
        
        response = client.put('/api/profile',
            json={'name': 'John', 'interests': 'hiking'},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 400


class TestViewOtherProfile:
    def test_view_other_profile_not_found(self, client):
        response = client.get('/api/profile/99999')
        assert response.status_code == 404
    
    def test_view_other_profile_private_authenticated_different_user(self, client, app):
        with app.app_context():
            from app import bcrypt
            user = User(
                email='test@example.com',
                password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8'),
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
        
        login_response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'TestPass123!'
        })
        token = login_response.json['token']
        
        response = client.get(f'/api/profile/{profile_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
