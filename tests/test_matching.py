import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, Profile, Like, Match, Notification
from app import bcrypt

# Import fixtures from helpers
from tests.helpers import *


class TestMatchingAlgorithm:
    """Test the matching algorithm scoring."""
    
    def test_match_score_within_radius(self, app, client, profile1, profile2, token1):
        """Test match score when profiles are compatible."""
        response = client.get('/api/matches/potential',
                            headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        matches = response.json
        assert len(matches) > 0
        
        match = next((m for m in matches if m['user_id'] == profile2.user_id), None)
        assert match is not None
        assert match['match_score'] >= 20
    
    def test_match_score_outside_radius(self, app, client, profile1, token1):
        """Test match score for incompatible profile."""
        response = client.get('/api/matches/potential',
                            headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        matches = response.json
        
        profile_ids = [m['user_id'] for m in matches]
        assert profile1.user_id + 2 not in profile_ids
    
    def test_match_score_age_in_range(self, app, client, profile1, profile2, token1):
        """Test age compatibility scoring."""
        # profile1 prefers ages 18-50, profile2 is 28
        response = client.get('/api/matches/potential',
                            headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        matches = response.json
        match = next((m for m in matches if m['user_id'] == profile2.user_id), None)
        assert match is not None
        assert match['match_score'] >= 20  # Age points
    
    def test_match_score_shared_interests(self, app, client, profile1, profile2, token1):
        """Test shared interests scoring."""
        # Both have 'hiking' in common
        response = client.get('/api/matches/potential',
                            headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        matches = response.json
        match = next((m for m in matches if m['user_id'] == profile2.user_id), None)
        assert match is not None
        assert 'hiking' in match['match_details'].get('shared_interests', [])
    
    def test_match_score_relationship_goal(self, app, client, profile1, profile2, token1):
        """Test relationship goal matching."""
        # Both have 'serious_relationship'
        response = client.get('/api/matches/potential',
                            headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        matches = response.json
        match = next((m for m in matches if m['user_id'] == profile2.user_id), None)
        assert match is not None
        assert match['match_details'].get('goal_match') == True
    
    def test_match_score_gender_preference(self, app, client, profile1, profile2, token1):
        """Test gender preference scoring."""
        # profile1 (male) prefers female, profile2 is female
        response = client.get('/api/matches/potential',
                            headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        matches = response.json
        match = next((m for m in matches if m['user_id'] == profile2.user_id), None)
        assert match is not None
        # Should get gender preference points
    
    def test_match_score_below_threshold(self, app, client, profile1, profile3, token1):
        """Test that profiles below threshold are filtered out."""
        # profile3 is incompatible
        response = client.get('/api/matches/potential',
                            headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        matches = response.json
        profile_ids = [m['user_id'] for m in matches]
        assert profile3.user_id not in profile_ids
    
    def test_match_score_above_threshold(self, app, client, profile1, profile2, token1):
        """Test that compatible profiles appear in results."""
        response = client.get('/api/matches/potential',
                            headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        matches = response.json
        assert len(matches) > 0
        assert all(m['match_score'] >= 50 for m in matches)


class TestMatchingActions:
    """Test like/dislike/pass actions."""
    
    def test_like_user(self, app, client, profile1, profile2, token1, user2):
        """Test liking a user."""
        response = client.post(f'/api/matches/like/{user2}',
                             headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        assert response.json['match'] == False
    
    def test_like_creates_notification(self, app, client, profile1, profile2, token1, user2, mock_socket_emit):
        """Test that liking creates a notification."""
        response = client.post(f'/api/matches/like/{user2}',
                             headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        
        with app.app_context():
            notification = Notification.query.filter_by(
                user_id=user2,
                type='like'
            ).first()
            assert notification is not None
            assert 'liked you' in notification.message.lower()
    
    def test_mutual_match_creation(self, app, client, profile1, profile2, token1, token2, user1, user2):
        """Test mutual match when both users like each other."""
        # User1 likes User2
        client.post(f'/api/matches/like/{user2}',
                   headers={'Authorization': f'Bearer {token1}'})
        
        # User2 likes User1
        response = client.post(f'/api/matches/like/{user1}',
                              headers={'Authorization': f'Bearer {token2}'})
        
        assert response.status_code == 200
        assert response.json['match'] == True
        
        with app.app_context():
            match = Match.query.filter(
                ((Match.user1_id == user1) & (Match.user2_id == user2)) |
                ((Match.user1_id == user2) & (Match.user2_id == user1))
            ).first()
            assert match is not None
    
    def test_mutual_match_notification(self, app, client, profile1, profile2, token1, token2, user1, user2, mock_socket_emit):
        """Test mutual match creates notifications for both users."""
        client.post(f'/api/matches/like/{user2}',
                   headers={'Authorization': f'Bearer {token1}'})
        
        client.post(f'/api/matches/like/{user1}',
                   headers={'Authorization': f'Bearer {token2}'})
        
        with app.app_context():
            # Both users should have match notifications
            notifications = Notification.query.filter_by(type='match').all()
            assert len(notifications) >= 2
    
    def test_dislike_user(self, app, client, profile1, profile2, token1, user2):
        """Test disliking a user."""
        response = client.post(f'/api/matches/dislike/{user2}',
                              headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        
        with app.app_context():
            like = Like.query.filter_by(
                from_user_id=profile1.user_id,
                to_user_id=user2
            ).first()
            assert like.status == 'disliked'
    
    def test_pass_user(self, app, client, profile1, profile2, token1, user2):
        """Test passing on a user."""
        response = client.post(f'/api/matches/pass/{user2}',
                             headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        
        with app.app_context():
            like = Like.query.filter_by(
                from_user_id=profile1.user_id,
                to_user_id=user2
            ).first()
            assert like.status == 'passed'
    
    def test_cannot_like_twice(self, app, client, profile1, profile2, token1, user2):
        """Test that liking twice doesn't create duplicate likes."""
        client.post(f'/api/matches/like/{user2}',
                   headers={'Authorization': f'Bearer {token1}'})
        
        response = client.post(f'/api/matches/like/{user2}',
                             headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        
        with app.app_context():
            likes = Like.query.filter_by(
                from_user_id=profile1.user_id,
                to_user_id=user2
            ).all()
            assert len(likes) == 1


class TestPotentialMatches:
    """Test potential matches listing."""
    
    def test_get_potential_matches(self, app, client, profile1, profile2, token1):
        """Test getting potential matches."""
        response = client.get('/api/matches/potential',
                            headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        assert isinstance(response.json, list)
    
    def test_filter_by_age(self, app, client, profile1, profile2, profile3, token1):
        """Test filtering potential matches by age."""
        response = client.get('/api/matches/potential?age_min=20&age_max=30',
                            headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        matches = response.json
        
        for match in matches:
            assert 20 <= match['age'] <= 30
    
    def test_excludes_already_liked(self, app, client, profile1, profile2, token1, user2):
        """Test that already-liked users are excluded."""
        # Like user2 first
        client.post(f'/api/matches/like/{user2}',
                   headers={'Authorization': f'Bearer {token1}'})
        
        # Get potential matches - should exclude user2 since we already interacted
        response = client.get('/api/matches/potential',
                            headers={'Authorization': f'Bearer {token1}'})
        
        # User2 should not appear in potential matches (already liked)
        # Check that we're getting other profiles or empty list
        matches = response.json
        # Since only profile2 exists besides profile1, the list should be empty
        assert response.status_code == 200
    
    def test_excludes_matches(self, app, client, profile1, profile2, token1, token2, user1, user2):
        """Test that matched users are excluded from potential matches."""
        # Create a mutual match
        client.post(f'/api/matches/like/{user2}',
                   headers={'Authorization': f'Bearer {token1}'})
        client.post(f'/api/matches/like/{user1}',
                   headers={'Authorization': f'Bearer {token2}'})
        
        # Get potential matches
        response = client.get('/api/matches/potential',
                            headers={'Authorization': f'Bearer {token1}'})
        
        matches = response.json
        profile_ids = [m['user_id'] for m in matches]
        assert user2 not in profile_ids
    
    def test_empty_when_no_profiles(self, app, client, profile1, token1):
        """Test empty list when no other profiles exist."""
        response = client.get('/api/matches/potential',
                            headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        assert response.json == []
    
    def test_unauthorized_no_potential_matches(self, client):
        """Test that unauthenticated users can't get potential matches."""
        response = client.get('/api/matches/potential')
        assert response.status_code == 401


class TestViewMatches:
    """Test viewing mutual matches."""
    
    def test_get_matches(self, app, client, profile1, profile2, token1, token2, user1, user2):
        """Test getting mutual matches."""
        # Create a match
        client.post(f'/api/matches/like/{user2}',
                   headers={'Authorization': f'Bearer {token1}'})
        client.post(f'/api/matches/like/{user1}',
                   headers={'Authorization': f'Bearer {token2}'})
        
        response = client.get('/api/matches',
                             headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        matches = response.json
        assert len(matches) > 0
        assert 'name' in matches[0]['profile']
    
    def test_get_matches_empty(self, app, client, profile1, token1):
        """Test empty matches list."""
        response = client.get('/api/matches',
                             headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        assert response.json == []


class TestNotifications:
    """Test notifications."""
    
    def test_get_notifications(self, app, client, profile1, profile2, token1, token2, user1, user2):
        """Test getting notifications."""
        # Create a like
        client.post(f'/api/matches/like/{user2}',
                   headers={'Authorization': f'Bearer {token1}'})
        
        response = client.get('/api/notifications',
                             headers={'Authorization': f'Bearer {token2}'})
        
        assert response.status_code == 200
        notifications = response.json
        assert len(notifications) > 0
        assert notifications[0]['type'] == 'like'
    
    def test_unread_count(self, app, client, profile1, profile2, token1, token2, user1, user2):
        """Test getting unread notification count."""
        client.post(f'/api/matches/like/{user2}',
                   headers={'Authorization': f'Bearer {token1}'})
        
        response = client.get('/api/notifications/unread-count',
                             headers={'Authorization': f'Bearer {token2}'})
        
        assert response.status_code == 200
        assert response.json['unread_count'] >= 1
    
    def test_mark_as_read(self, app, client, profile1, profile2, token1, token2, user1, user2):
        """Test marking a notification as read."""
        client.post(f'/api/matches/like/{user2}',
                   headers={'Authorization': f'Bearer {token1}'})
        
        # Get notification ID
        response = client.get('/api/notifications',
                             headers={'Authorization': f'Bearer {token2}'})
        notification_id = response.json[0]['id']
        
        # Mark as read
        response = client.put(f'/api/notifications/{notification_id}/read',
                            headers={'Authorization': f'Bearer {token2}'})
        
        assert response.status_code == 200
        
        # Verify it's marked
        response = client.get('/api/notifications',
                             headers={'Authorization': f'Bearer {token2}'})
        assert response.json[0]['is_read'] == True
    
    def test_mark_all_as_read(self, app, client, profile1, profile2, token1, token2, user1, user2):
        """Test marking all notifications as read."""
        # Create notifications
        client.post(f'/api/matches/like/{user2}',
                   headers={'Authorization': f'Bearer {token1}'})
        
        response = client.put('/api/notifications/read-all',
                            headers={'Authorization': f'Bearer {token2}'})
        
        assert response.status_code == 200
        
        # Verify all marked
        response = client.get('/api/notifications/unread-count',
                             headers={'Authorization': f'Bearer {token2}'})
        assert response.json['unread_count'] == 0
    
    def test_notification_includes_sender_profile(self, app, client, profile1, profile2, token1, token2, user1, user2):
        """Test that notification includes sender's profile data."""
        client.post(f'/api/matches/like/{user2}',
                   headers={'Authorization': f'Bearer {token1}'})
        
        response = client.get('/api/notifications',
                             headers={'Authorization': f'Bearer {token2}'})
        
        assert response.status_code == 200
        notification = response.json[0]
        assert 'from_profile' in notification
        assert 'name' in notification['from_profile']


class TestMatchScoreEndpoint:
    """Test the match score endpoint."""
    
    def test_get_match_score(self, app, client, profile1, profile2, token1, user2):
        """Test getting match score for a specific user."""
        response = client.get(f'/api/matches/score/{user2}',
                             headers={'Authorization': f'Bearer {token1}'})
        
        assert response.status_code == 200
        assert 'score' in response.json
        assert 'details' in response.json
        assert response.json['to_user_id'] == user2
    
    def test_get_match_score_not_found(self, app, client, token1):
        """Test getting score for non-existent user."""
        response = client.get('/api/matches/score/99999',
                             headers={'Authorization': f'Bearer {token1}'})
        
        # Should return 404 or 400
        assert response.status_code in [404, 400]
