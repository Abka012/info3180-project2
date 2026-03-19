import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, Profile, Bookmark


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
def test_user(client, app):
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
def test_profile(client, app, test_user):
    with app.app_context():
        profile = Profile(
            user_id=test_user['user_id'],
            name='Test User',
            age=25,
            bio='Test bio',
            gender='male',
            gender_preference='female',
            interests=['music', 'travel'],
            relationship_goal='dating'
        )
        db.session.add(profile)
        db.session.commit()
    
    return profile


class TestSearch:
    def test_search_profiles_unauthorized(self, client):
        response = client.post('/api/matches/search', json={})
        assert response.status_code == 401

    def test_search_by_age_range(self, client, test_user, test_profile, app):
        other_user_id = create_test_user(client, 'other@test.com', 'TestPass123!', 'Other User', 30)
        
        token = test_user['token']
        response = client.post(
            '/api/matches/search',
            json={'age_min': 25, 'age_max': 35},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200

    def test_search_by_interests(self, client, test_user, test_profile, app):
        other_user_id = create_test_user(client, 'other@test.com', 'TestPass123!', 'Other User', 25, ['music', 'gaming'])
        
        token = test_user['token']
        response = client.post(
            '/api/matches/search',
            json={'interests': ['music']},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) > 0

    def test_search_sort_by_newest(self, client, test_user, test_profile, app):
        create_test_user(client, 'other@test.com', 'TestPass123!', 'Other User')
        
        token = test_user['token']
        response = client.post(
            '/api/matches/search',
            json={'sort_by': 'newest'},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200


class TestBookmarks:
    def test_get_bookmarks_unauthorized(self, client):
        response = client.get('/api/matches/bookmarks')
        assert response.status_code == 401

    def test_add_bookmark(self, client, test_user, test_profile, app):
        other_user_id = create_test_user(client, 'other@test.com', 'TestPass123!', 'Other User')
        
        token = test_user['token']
        response = client.post(
            f'/api/matches/bookmark/{other_user_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 201

    def test_add_duplicate_bookmark(self, client, test_user, test_profile, app):
        other_user_id = create_test_user(client, 'other@test.com', 'TestPass123!', 'Other User')
        
        token = test_user['token']
        client.post(
            f'/api/matches/bookmark/{other_user_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        response = client.post(
            f'/api/matches/bookmark/{other_user_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200

    def test_bookmark_self(self, client, test_user, test_profile):
        token = test_user['token']
        response = client.post(
            f'/api/matches/bookmark/{test_user["user_id"]}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 400

    def test_get_bookmarks(self, client, test_user, test_profile, app):
        other_user_id = create_test_user(client, 'other@test.com', 'TestPass123!', 'Other User')
        
        token = test_user['token']
        client.post(
            f'/api/matches/bookmark/{other_user_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        response = client.get(
            '/api/matches/bookmarks',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) > 0

    def test_remove_bookmark(self, client, test_user, test_profile, app):
        other_user_id = create_test_user(client, 'other@test.com', 'TestPass123!', 'Other User')
        
        token = test_user['token']
        client.post(
            f'/api/matches/bookmark/{other_user_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        response = client.delete(
            f'/api/matches/bookmark/{other_user_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200

    def test_remove_nonexistent_bookmark(self, client, test_user, test_profile, app):
        other_user_id = create_test_user(client, 'other@test.com', 'TestPass123!', 'Other User')
        
        token = test_user['token']
        response = client.delete(
            f'/api/matches/bookmark/{other_user_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 404


def create_test_user(client, email, password, name, age=25, interests=None):
    if interests is None:
        interests = ['music']
    
    response = client.post('/api/auth/register', json={
        'email': email,
        'password': password,
        'confirm_password': password
    })
    
    with client.application.app_context():
        user = db.session.query(User).filter_by(email=email).first()
        user.is_verified = True
        db.session.commit()
        user_id = user.id
    
    response = client.post('/api/auth/login', json={
        'email': email,
        'password': password
    })
    
    with client.application.app_context():
        profile = Profile(
            user_id=user_id,
            name=name,
            age=age,
            bio='Test bio',
            gender='male',
            gender_preference='female',
            interests=interests,
            relationship_goal='dating'
        )
        db.session.add(profile)
        db.session.commit()
    
    return user_id
