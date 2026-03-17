from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['WTF_CSRF_ENABLED'] = False
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    db.init_app(app)
    bcrypt.init_app(app)
    
    from app import views
    app.register_blueprint(views.bp)
    
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()
