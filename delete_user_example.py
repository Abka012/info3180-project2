"""Blueprint for a script use to delete user from production build"""

# SQLALCHEMY_DATABASE_URI = "replace with external database url in app/config.py"
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    user = User.query.filter_by(email="your email").first()
    if user:
        db.session.delete(user)  # or user.is_active = False
        db.session.commit()
        print("User deleted")
    else:
        print("User not found")
