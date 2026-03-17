from flask import Blueprint, request, jsonify
from app import db
from app.models import Notification, User
from app.views import get_user_from_token

bp_notifications = Blueprint('notifications', __name__, url_prefix='/api/notifications')


@bp_notifications.route('', methods=['GET'])
def get_notifications():
    """Get notifications for current user."""
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    notifications = Notification.query.filter_by(
        user_id=user.id
    ).order_by(Notification.created_at.desc()).limit(50).all()
    
    # Add from_user profile info
    result = []
    for n in notifications:
        data = n.to_dict()
        if n.from_user_id:
            from_profile = db.session.query(
                __import__('app.models', fromlist=['Profile']).Profile
            ).filter_by(user_id=n.from_user_id).first()
            if from_profile:
                data['from_profile'] = from_profile.to_dict()
        result.append(data)
    
    return jsonify(result), 200


@bp_notifications.route('/unread-count', methods=['GET'])
def get_unread_count():
    """Get count of unread notifications."""
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    count = Notification.query.filter_by(
        user_id=user.id,
        is_read=False
    ).count()
    
    return jsonify({'unread_count': count}), 200


@bp_notifications.route('/<int:notification_id>/read', methods=['PUT'])
def mark_as_read(notification_id):
    """Mark a notification as read."""
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    notification = Notification.query.filter_by(
        id=notification_id,
        user_id=user.id
    ).first()
    
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404
    
    notification.is_read = True
    db.session.commit()
    
    return jsonify({'message': 'Notification marked as read'}), 200


@bp_notifications.route('/read-all', methods=['PUT'])
def mark_all_as_read():
    """Mark all notifications as read."""
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    Notification.query.filter_by(
        user_id=user.id,
        is_read=False
    ).update({'is_read': True})
    db.session.commit()
    
    return jsonify({'message': 'All notifications marked as read'}), 200
