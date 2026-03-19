import pytest
import sys
import os
import io
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, Profile


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['MAILTRAP_SMTP_USER'] = None
    app.config['UPLOAD_FOLDER'] = '/tmp/test_uploads'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
    
    if os.path.exists('/tmp/test_uploads'):
        import shutil
        shutil.rmtree('/tmp/test_uploads')


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def verified_user(client, app):
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'TestPass123!',
        'confirm_password': 'TestPass123!'
    })
    
    with app.app_context():
        user = db.session.query(User).filter_by(email='test@example.com').first()
        user.is_verified = True
        db.session.commit()
        user_id = user.id
    
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'TestPass123!'
    })
    token = response.get_json()['token']
    
    return {'user_id': user_id, 'token': token}


@pytest.fixture
def user_with_profile(client, app, verified_user):
    with app.app_context():
        profile = Profile(
            user_id=verified_user['user_id'],
            name='Test User',
            age=25,
            bio='Test bio',
            gender='male',
            gender_preference='female',
            interests=['coding', 'music', 'reading'],
            relationship_goal='dating'
        )
        db.session.add(profile)
        db.session.commit()
    
    return verified_user


class TestProfilePictureUpload:
    def test_upload_picture_success_jpg(self, client, user_with_profile):
        token = user_with_profile['token']
        
        data = {
            'file': (io.BytesIO(b'fake image content'), 'test.jpg')
        }
        
        response = client.post(
            '/api/profile/picture',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        assert 'filename' in response.json
    
    def test_upload_picture_success_png(self, client, user_with_profile):
        token = user_with_profile['token']
        
        data = {
            'file': (io.BytesIO(b'fake image content'), 'test.png')
        }
        
        response = client.post(
            '/api/profile/picture',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
    
    def test_upload_picture_no_file(self, client, user_with_profile):
        token = user_with_profile['token']
        
        response = client.post(
            '/api/profile/picture',
            data={},
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 400
        assert 'No file' in response.json['error']
    
    def test_upload_picture_invalid_extension(self, client, user_with_profile):
        token = user_with_profile['token']
        
        data = {
            'file': (io.BytesIO(b'fake executable'), 'test.exe')
        }
        
        response = client.post(
            '/api/profile/picture',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 400
    
    def test_upload_picture_empty_filename(self, client, user_with_profile):
        token = user_with_profile['token']
        
        data = {
            'file': (io.BytesIO(b'fake content'), '')
        }
        
        response = client.post(
            '/api/profile/picture',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 400
    
    def test_upload_picture_unauthorized(self, client):
        data = {
            'file': (io.BytesIO(b'fake image content'), 'test.jpg')
        }
        
        response = client.post(
            '/api/profile/picture',
            data=data,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 401
    
    def test_upload_picture_no_profile(self, client, verified_user):
        token = verified_user['token']
        
        data = {
            'file': (io.BytesIO(b'fake image content'), 'test.jpg')
        }
        
        response = client.post(
            '/api/profile/picture',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 400
        assert 'Create a profile' in response.json['error']
    
    def test_upload_picture_webp(self, client, user_with_profile):
        token = user_with_profile['token']
        
        data = {
            'file': (io.BytesIO(b'fake webp content'), 'test.webp')
        }
        
        response = client.post(
            '/api/profile/picture',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
    
    def test_upload_picture_gif(self, client, user_with_profile):
        token = user_with_profile['token']
        
        data = {
            'file': (io.BytesIO(b'fake gif content'), 'test.gif')
        }
        
        response = client.post(
            '/api/profile/picture',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
