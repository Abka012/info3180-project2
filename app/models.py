"""
Database models for the dating application.

This module contains all SQLAlchemy models representing the application's
data entities, including users, profiles, matches, messages, and notifications.
"""

import secrets
from datetime import datetime, timezone

from app import db  # Import db from app/__init__.py
from flask_login import UserMixin
from app import login_manager  # Import login_manager from __init__.py

# Import JSON type for interests column
from sqlalchemy.types import JSON


def utc_now():
    """
    Get current UTC timestamp.

    Returns:
        Current datetime in UTC timezone
    """
    return datetime.now(timezone.utc)


def generate_verification_token():
    """Generate a secure verification token."""
    return secrets.token_urlsafe(32)


# Initialize LoginManager and set user_loader
# Note: LoginManager is initialized in __init__.py, so we import it.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- Models ---


class User(UserMixin, db.Model):
    """
    User model representing application users.

    Attributes:
        id: Primary key
        email: User's email address (unique)
        username: User's username (unique)
        password_hash: Hashed password
        is_verified: Email verification status
        verification_token: Token for email verification
        created_at: Account creation timestamp
        last_active: Last activity timestamp
        profile: One-to-one relationship with Profile
        likes_sent: Likes sent by this user
        likes_received: Likes received by this user
        notifications: User's notifications
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(
        db.String(80), unique=True, nullable=False, index=True
    )  # Kept from existing model, aligns with ER diagram description
    password_hash = db.Column(db.String(128), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(
        db.String(64), unique=True, default=generate_verification_token
    )
    created_at = db.Column(db.DateTime, default=utc_now)
    last_active = db.Column(db.DateTime, default=utc_now)

    def set_password(self, password):
        from app import bcrypt

        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        from app import bcrypt

        return bcrypt.check_password_hash(self.password_hash, password)

    # Relationships
    sent_messages = db.relationship(
        "Message", foreign_keys="Message.sender_id", backref="sender", lazy=True
    )
    received_messages = db.relationship(
        "Message", foreign_keys="Message.receiver_id", backref="receiver", lazy=True
    )
    likes_sent = db.relationship(
        "Like", foreign_keys="Like.from_user_id", backref="liker", lazy=True
    )
    likes_received = db.relationship(
        "Like", foreign_keys="Like.to_user_id", backref="liked_user", lazy=True
    )
    matches_initiated = db.relationship(
        "Match", foreign_keys="Match.user1_id", backref="user1", lazy=True
    )
    matches_received = db.relationship(
        "Match", foreign_keys="Match.user2_id", backref="user2", lazy=True
    )
    # Profile relationship - A user has one profile
    profile = db.relationship(
        "Profile", backref="user", uselist=False, cascade="all,delete-orphan", lazy=True
    )

    # Foreign keys for notifications
    user_notifications = db.relationship(
        "Notification",
        foreign_keys="Notification.user_id",
        back_populates="recipient",
        lazy=True,
        overlaps="received_notifications,recipient_user",
    )
    triggered_notifications = db.relationship(
        "Notification",
        foreign_keys="Notification.from_user_id",
        back_populates="notifier",
        lazy=True,
        overlaps="sent_notifications,notifier_user",
    )

    def get_id(self):
        return str(self.id)  # Flask-Login expects get_id() method

    @property
    def user_id(self):
        return self.id

    def __repr__(self):
        return f"<User {self.username}>"


class Profile(db.Model):
    """
    Profile model storing public-facing dating profile data for a user.

    Attributes:
        profile_id: Primary key
        user_id: Foreign key linking to the User (one-to-one)
        name: Display name
        age: Age used in discovery
        bio: Free-form profile description
        preferred_age_min: Minimum preferred age for matches
        preferred_age_max: Maximum preferred age for matches
        interests: Interest tags (JSON array)
        profile_picture: Filename of the uploaded profile picture
        visibility: Public/private profile flag
        gender: User gender
        gender_preference: Preferred gender for matches
        relationship_goal: Desired relationship type
        occupation: Occupation text
        created_at: Profile creation timestamp
        updated_at: Profile last modification timestamp
    """

    __tablename__ = "profiles"

    profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    preferred_age_min = db.Column(db.Integer, default=18)
    preferred_age_max = db.Column(db.Integer, default=50)
    interests = db.Column(JSON, default=list)  # Use default=list for empty list
    profile_picture = db.Column(db.String(255), nullable=True)
    visibility = db.Column(db.Boolean, default=True)
    gender = db.Column(db.String(50), nullable=True)
    gender_preference = db.Column(db.String(50), default="all")
    relationship_goal = db.Column(db.String(50), nullable=True)
    occupation = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now, index=True)
    updated_at = db.Column(
        db.DateTime, default=utc_now, onupdate=utc_now
    )  # Use onupdate for automatic updates

    def __repr__(self):
        return f"<Profile {self.profile_id} for User {self.user_id}>"

    def to_dict(self):
        return {
            "profile_id": self.profile_id,
            "user_id": self.user_id,
            "name": self.name,
            "age": self.age,
            "bio": self.bio,
            "gender": self.gender,
            "gender_preference": self.gender_preference,
            "interests": self.interests or [],
            "relationship_goal": self.relationship_goal,
            "occupation": self.occupation,
            "profile_picture": self.profile_picture,
            "visibility": self.visibility,
            "preferred_age_min": self.preferred_age_min,
            "preferred_age_max": self.preferred_age_max,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Like(db.Model):
    """
    Model for user likes/dislikes/passes.

    Attributes:
        like_id: Primary key
        from_user_id: User initiating the action
        to_user_id: User receiving the action
        status: Type of action ('liked', 'disliked', 'passed')
        created_at: Timestamp of the action
    """

    __tablename__ = "likes"

    like_id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(20), default="liked")
    created_at = db.Column(db.DateTime, default=utc_now, index=True)

    # Constraint: UNIQUE(from_user_id, to_user_id) ensures a user can only have one active row per target user.
    __table_args__ = (
        db.UniqueConstraint("from_user_id", "to_user_id", name="uq_user_like"),
    )

    def __repr__(self):
        return (
            f"<Like from {self.from_user_id} to {self.to_user_id} status {self.status}>"
        )


class Match(db.Model):
    """
    Model for mutual matches between two users.

    Attributes:
        match_id: Primary key
        user1_id: ID of the first matched user
        user2_id: ID of the second matched user
        created_at: Timestamp of the match
    """

    __tablename__ = "matches"

    match_id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now, index=True)

    # Constraint: UNIQUE(user1_id, user2_id) ensures a match is recorded only once between two users.
    __table_args__ = (
        db.UniqueConstraint("user1_id", "user2_id", name="uq_mutual_match"),
    )

    def __repr__(self):
        return f"<Match {self.match_id} between {self.user1_id} and {self.user2_id}>"


# Notification model (adjusted based on markdown, maintaining existing logic)
class Notification(db.Model):
    """
    Notification model representing user notifications for events like likes, matches, and messages.

    Attributes:
        notification_id: Primary key
        user_id: User who receives the notification (FK to users.id)
        type: Type of notification ('match', 'like', 'message')
        message: Notification message content
        from_user_id: User who triggered the notification (FK to users.id, nullable)
        is_read: Whether notification has been read
        created_at: Timestamp when notification was created
    """

    __tablename__ = "notifications"
    # Indices as per markdown and existing code for efficient lookups.
    __table_args__ = (
        db.Index(
            "ix_notifications_user_read_created",
            "user_id",
            "is_read",
            "created_at",
        ),
        db.Index("ix_notifications_from_user", "from_user_id"),
    )

    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # FK to users.id
    type = db.Column(db.String(50), nullable=False)  # 'match', 'like', 'message'
    message = db.Column(db.String(255), nullable=False)
    from_user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True
    )  # FK to users.id
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships to User, ensuring correct foreign key mapping
    # recipient maps to user_id (the user receiving the notification)
    recipient = db.relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="user_notifications",
        lazy=True,
        overlaps="received_notifications,recipient_user",
    )
    # notifier maps to from_user_id (the user who triggered the notification)
    notifier = db.relationship(
        "User",
        foreign_keys=[from_user_id],
        back_populates="triggered_notifications",
        lazy=True,
        overlaps="sent_notifications,notifier_user",
    )

    def to_dict(self):
        """Converts notification object to a dictionary for API responses."""
        return {
            "id": self.notification_id,
            "user_id": self.user_id,
            "type": self.type,
            "message": self.message,
            "from_user_id": self.from_user_id,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Message(db.Model):
    """
    Model for chat messages between matched users.

    Attributes:
        message_id: Primary key
        sender_id: ID of the user sending the message (FK to users.id)
        receiver_id: ID of the user receiving the message (FK to users.id)
        content: The message body
        created_at: Timestamp of the message
        read_at: Timestamp when the message was read (nullable)
    """

    __tablename__ = "messages"

    message_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now, index=True)
    read_at = db.Column(db.DateTime, nullable=True)

    # Indexing for efficient retrieval of conversations and unread message counts.
    __table_args__ = (
        db.Index(
            "ix_messages_sender_receiver_created",
            "sender_id",
            "receiver_id",
            "created_at",
        ),
        db.Index(
            "ix_messages_receiver_sender_created",
            "receiver_id",
            "sender_id",
            "created_at",
        ),
        db.Index(
            "ix_messages_receiver_read", "receiver_id", "read_at"
        ),  # Useful for checking unread messages for a receiver
    )

    def __repr__(self):
        return f"<Message from {self.sender_id} to {self.receiver_id} at {self.created_at}>"

    def to_dict_extended(self, current_user_id):
        is_sender = self.sender_id == current_user_id
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
            "is_sender": is_sender,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "read_at": self.read_at.isoformat() if self.read_at else None,
        }


class Bookmark(db.Model):
    """
    Model for users saving profiles for later review.

    Attributes:
        bookmark_id: Primary key
        user_id: User creating the bookmark (FK to users.id)
        bookmarked_user_id: The user being bookmarked (FK to users.id)
        created_at: Timestamp of the bookmark creation
    """

    __tablename__ = "bookmark"  # As per markdown: 'bookmark' (singular)

    bookmark_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    bookmarked_user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=utc_now, index=True)

    # Constraint: UNIQUE(user_id, bookmarked_user_id) ensures a user can only bookmark another user once.
    __table_args__ = (
        db.UniqueConstraint("user_id", "bookmarked_user_id", name="uq_user_bookmark"),
    )

    def __repr__(self):
        return f"<Bookmark by {self.user_id} for {self.bookmarked_user_id}>"
