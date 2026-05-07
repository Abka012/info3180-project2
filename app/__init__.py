"""
Application factory and initialization.

This module contains the application factory function that creates and configures
the Flask application instance, including database setup, blueprint registration,
and WebSocket configuration.
"""

import os

from flask import Flask, current_app, send_from_directory
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Removed duplicate LoginManager import and added auth import

from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
socketio = SocketIO()
migrate = Migrate()
login_manager = LoginManager()  # Initialized at module level
limiter = Limiter(
    key_func=get_remote_address, default_limits=["200 per day", "50 per hour"]
)


# Store user sessions for WebSocket
connected_users = {}


def create_app(config_class=Config):
    """
    Create and configure the Flask application instance.

    Args:
        config_class: Configuration class to use (defaults to Config)

    Returns:
        Configured Flask application instance

    This function:
    - Creates the Flask app with the specified configuration
    - Initializes database, authentication, and WebSocket extensions
    - Sets up CORS for API endpoints
    - Registers blueprints for different application modules
    - Configures WebSocket event handlers
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["WTF_CSRF_ENABLED"] = False

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "https://driftdater-frontend-7zt8.onrender.com",
                    "http://localhost:5173",
                    "http://localhost:4173",
                ]
            }
        },
    )

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)  # Initialize LoginManager with the app
    login_manager.login_view = "login"  # Set the login view route name
    login_manager.login_message_category = (
        "info"  # Set message category for flash messages
    )

    socketio.init_app(
        app,
        cors_allowed_origins=[
            "https://driftdater-frontend-7zt8.onrender.com",
            "http://localhost:5173",
            "http://localhost:4173",
        ],
        async_mode="threading",
    )

    # Ensure upload directories exist
    with app.app_context():
        upload_folder = app.config.get("UPLOAD_FOLDER", "./uploads")
        if not os.path.isabs(upload_folder):
            upload_folder = os.path.join(app.root_path, "..", upload_folder)

        profile_pics_folder = os.path.join(upload_folder, "profile_pics")
        os.makedirs(profile_pics_folder, exist_ok=True)
        app.logger.info(f"Storage directories ensured at: {upload_folder}")

    # Serve uploaded files
    @app.route("/uploads/<path:filename>")
    def serve_upload(filename):
        """
        Serve uploaded files from the uploads directory.

        Args:
            filename: Name of the file to serve

        Returns:
            File response from the uploads directory
        """
        upload_folder = current_app.config.get("UPLOAD_FOLDER", "./uploads")
        if not os.path.isabs(upload_folder):
            upload_folder = os.path.join(app.root_path, "..", upload_folder)

        # Check if file exists in the direct path
        if os.path.exists(os.path.join(upload_folder, filename)):
            return send_from_directory(upload_folder, filename)

        # If not found, check if it's in the profile_pics subdirectory
        profile_pics_folder = os.path.join(upload_folder, "profile_pics")
        if os.path.exists(os.path.join(profile_pics_folder, filename)):
            return send_from_directory(profile_pics_folder, filename)

        # Fallback to direct path (will 404 if missing)
        return send_from_directory(upload_folder, filename)

    # Register blueprints
    from app import (
        matches,
        messages,
        notifications,
        views,
        auth,
        profile,
    )  # Import auth module

    app.register_blueprint(views.bp)
    app.register_blueprint(matches.bp)
    app.register_blueprint(notifications.bp_notifications)
    app.register_blueprint(messages.bp_messages)
    app.register_blueprint(auth.bp)  # Register auth blueprint
    app.register_blueprint(profile.bp)  # Register profile blueprint

    # Set socket emit function
    from app.matches import set_socket_emit

    set_socket_emit(
        lambda user_id, event, data: socketio.emit(event, data, room=f"user_{user_id}")
    )

    # WebSocket events
    @socketio.on("connect")
    def handle_connect(auth=None):
        """
        Handle WebSocket connection event.

        Args:
            auth: Optional authentication data
        """
        print(f"Client connected: {auth}")

    @socketio.on("disconnect")
    def handle_disconnect():
        """Handle WebSocket disconnection event."""
        print("Client disconnected")

    @socketio.on("subscribe")
    def handle_subscribe(data):
        """
        Handle user subscription to WebSocket channel.

        Args:
            data: Subscription data containing user_id
        """
        user_id = data.get("user_id")
        if user_id:
            connected_users[user_id] = True
            print(f"User {user_id} subscribed")

    @socketio.on("unsubscribe")
    def handle_unsubscribe(data):
        """
        Handle user unsubscription from WebSocket channel.

        Args:
            data: Unsubscription data containing user_id
        """
        user_id = data.get("user_id")
        if user_id and user_id in connected_users:
            del connected_users[user_id]

    return app


# SEED DATABASE
# subprocess.run(["python", "seed.py"])
