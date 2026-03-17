from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_socketio import SocketIO
from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
socketio = SocketIO()

# Store user sessions for WebSocket
connected_users = {}


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['WTF_CSRF_ENABLED'] = False
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    db.init_app(app)
    bcrypt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", async_mode='threading')
    
    # Register blueprints
    from app import views
    from app import matches
    from app import notifications
    
    app.register_blueprint(views.bp)
    app.register_blueprint(matches.bp)
    app.register_blueprint(notifications.bp_notifications)
    
    # Set socket emit function
    from app.matches import set_socket_emit
    set_socket_emit(lambda user_id, event, data: 
        socketio.emit(event, data, room=f'user_{user_id}')
    )
    
    # WebSocket events
    @socketio.on('connect')
    def handle_connect(auth=None):
        print(f'Client connected: {auth}')
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')
    
    @socketio.on('subscribe')
    def handle_subscribe(data):
        user_id = data.get('user_id')
        if user_id:
            connected_users[user_id] = True
            from flask import request
            print(f'User {user_id} subscribed')
    
    @socketio.on('unsubscribe')
    def handle_unsubscribe(data):
        user_id = data.get('user_id')
        if user_id and user_id in connected_users:
            del connected_users[user_id]
    
    with app.app_context():
        db.create_all()
    
    return app


app = create_app()


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
