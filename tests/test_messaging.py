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
        'password': 'password123',
        'confirm_password': 'password123'
    })
    
    with app.app_context():
        user = db.session.query(User).filter_by(email='test@example.com').first()
        user.is_verified = True
        db.session.commit()
        user_id = user.id
    
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
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
            location='New York',
            gender='male',
            gender_preference='female',
            interests='coding,music',
            relationship_goal='dating'
        )
        db.session.add(profile)
        db.session.commit()
    
    return profile


class TestMessaging:
    def test_send_message_unauthorized(self, client):
        response = client.post('/api/messages/1', json={'content': 'Hello'})
        assert response.status_code == 401

    def test_get_conversations_unauthorized(self, client):
        response = client.get('/api/messages')
        assert response.status_code == 401

    def test_send_message_no_match(self, client, test_user, test_profile):
        token = test_user['token']
        other_user_id = create_test_user(client, 'other@test.com', 'password123', 'Other User')
        
        response = client.post(
            f'/api/messages/{other_user_id}',
            json={'content': 'Hello'},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 403

    def test_send_message_success(self, client, test_user, test_profile, app):
        from app.models import Match
        
        other_user_id = create_test_user(client, 'other@test.com', 'password123', 'Other User')
        
        with app.app_context():
            match = Match(user1_id=test_user['user_id'], user2_id=other_user_id)
            db.session.add(match)
            db.session.commit()
        
        token = test_user['token']
        response = client.post(
            f'/api/messages/{other_user_id}',
            json={'content': 'Hello there!'},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data['content'] == 'Hello there!'
        assert data['sender_id'] == test_user['user_id']

    def test_message_too_long(self, client, test_user, test_profile, app):
        from app.models import Match
        
        other_user_id = create_test_user(client, 'other@test.com', 'password123', 'Other User')
        
        with app.app_context():
            match = Match(user1_id=test_user['user_id'], user2_id=other_user_id)
            db.session.add(match)
            db.session.commit()
        
        token = test_user['token']
        long_content = 'x' * 1001
        response = client.post(
            f'/api/messages/{other_user_id}',
            json={'content': long_content},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 400

    def test_get_conversations(self, client, test_user, test_profile, app):
        from app.models import Match, Message
        
        other_user_id = create_test_user(client, 'other@test.com', 'password123', 'Other User')
        
        with app.app_context():
            match = Match(user1_id=test_user['user_id'], user2_id=other_user_id)
            db.session.add(match)
            
            msg = Message(
                sender_id=test_user['user_id'],
                receiver_id=other_user_id,
                content='Test message'
            )
            db.session.add(msg)
            db.session.commit()
        
        token = test_user['token']
        response = client.get(
            '/api/messages',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) > 0

    def test_get_message_history(self, client, test_user, test_profile, app):
        from app.models import Match, Message
        
        other_user_id = create_test_user(client, 'other@test.com', 'password123', 'Other User')
        
        with app.app_context():
            match = Match(user1_id=test_user['user_id'], user2_id=other_user_id)
            db.session.add(match)
            
            msg = Message(
                sender_id=test_user['user_id'],
                receiver_id=other_user_id,
                content='Test message'
            )
            db.session.add(msg)
            db.session.commit()
        
        token = test_user['token']
        response = client.get(
            f'/api/messages/{other_user_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'messages' in data
        assert 'other_user' in data

    def test_unread_count(self, client, test_user, test_profile, app):
        from app.models import Match, Message
        
        other_user_id = create_test_user(client, 'other@test.com', 'password123', 'Other User')
        
        with app.app_context():
            match = Match(user1_id=test_user['user_id'], user2_id=other_user_id)
            db.session.add(match)
            
            msg = Message(
                sender_id=other_user_id,
                receiver_id=test_user['user_id'],
                content='Unread message'
            )
            db.session.add(msg)
            db.session.commit()
        
        token = test_user['token']
        response = client.get(
            '/api/messages/unread',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['unread_count'] >= 1


def create_test_user(client, email, password, name):
    from app.models import User, Profile
    
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
    token = response.get_json()['token']
    
    with client.application.app_context():
        profile = Profile(
            user_id=user_id,
            name=name,
            age=25,
            bio='Test bio',
            location='New York',
            gender='male',
            gender_preference='female',
            interests='coding,music',
            relationship_goal='dating'
        )
        db.session.add(profile)
        db.session.commit()
    
    return user_id
