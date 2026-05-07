from flask import (
    Blueprint,
    current_app,
    jsonify,
    request,
    redirect,
    url_for,
    render_template,
    flash,
)
from flask_login import current_user, login_required, login_user, logout_user
from app.models import (
    User,
    Message,
    Notification,
    Match,
    Like,
)  # Import necessary models
from app import (
    db,
    socketio,
    limiter,
)  # Import db, socketio, limiter from app/__init__.py
from werkzeug.utils import secure_filename
import jwt
import os
import re
from datetime import datetime
import uuid

bp = Blueprint("views", __name__)

# Rate limiting configuration (already set up in app/__init__.py or here if separated)
# limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
# limiter.init_app(app) # Re-initialize if limiter is imported from __init__


# --- Helper Functions ---
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


def validate_password_strength(password):
    """Validate password strength and return result."""
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter")
    if not re.search(r"\d", password):
        errors.append("Password must contain at least one number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Password must contain at least one special character")
    return {"is_valid": len(errors) == 0, "errors": errors}


def generate_token(user_id, token_type="auth", expires_days=7):
    """Generate a JWT token."""
    from datetime import datetime, timedelta

    payload = {
        "user_id": user_id,
        "type": token_type,
        "exp": datetime.utcnow() + timedelta(days=expires_days),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def verify_token(token, token_type="auth"):
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
        )
        if token_type and payload.get("type") != token_type:
            return None
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


from app.email_utils import send_email

def get_user_by_public_id(public_id):
    return User.query.filter_by(public_id=public_id).first()


def get_user_from_token():
    """Get user from JWT token in Authorization header"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
        )
        user = db.session.get(User, payload["user_id"])
        return user
    except Exception:
        return None


# --- Routes ---


@bp.route("/")
@limiter.limit("1000 per day")  # Example limit for homepage
def index():
    if current_user.is_authenticated:
        # Assuming 'browse' route is registered under the 'views' blueprint
        return redirect(url_for("views.browse"))
    # Assuming 'login' route is registered under the 'auth' blueprint (which is named 'auth')
    return redirect(url_for("auth.login"))


@bp.route("/register", methods=["GET", "POST"])
@limiter.limit("5/minute")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("views.browse"))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        age_str = request.form.get("age")
        gender = request.form.get("gender")
        interested_in = request.form.get("interested_in")

        if not all(
            [
                username,
                email,
                password,
                password2,
                first_name,
                age_str,
                gender,
                interested_in,
            ]
        ):
            flash("All fields are required. Please fill in all the details.", "danger")
            return redirect(url_for("views.register"))  # Use blueprint name

        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for("views.register"))  # Use blueprint name
        if User.query.filter_by(email=email).first():
            flash(
                "Email address already registered. Please log in or use a different email.",
                "danger",
            )
            return redirect(url_for("views.register"))  # Use blueprint name

        if password != password2:
            flash(
                "Passwords do not match. Please ensure passwords are the same.",
                "danger",
            )
            return redirect(url_for("views.register"))  # Use blueprint name

        try:
            age = int(age_str)
            if age < 18:
                flash(
                    "You must be at least 18 years old to use this service.", "danger"
                )
                return redirect(url_for("views.register"))  # Use blueprint name
        except ValueError:
            flash("Invalid age entered. Please enter a valid number.", "danger")
            return redirect(url_for("views.register"))  # Use blueprint name

        new_user = User(
            username=username,
            email=email,
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.flush()

        new_profile = Profile(
            user_id=new_user.id,
            name=f"{first_name} {last_name}",
            age=age,
            gender=gender,
            gender_preference=interested_in,
            profile_picture="default_avatar.png",
        )
        db.session.add(new_profile)
        db.session.commit()

        flash("Your account has been created! Please log in.", "success")
        return redirect(url_for("auth.login"))  # Redirect to auth blueprint login

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
@limiter.limit("100/hour")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.browse"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("remember")  # 'on' or None

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=True if remember else False)
            user.last_login = datetime.utcnow()  # Assuming last_login attribute exists
            db.session.commit()

            flash("Login successful!", "success")
            next_page = request.args.get("next")
            # Use blueprint name for browse route
            return redirect(next_page or url_for("views.browse"))
        else:
            flash("Login failed. Please check your email and password.", "danger")

    return render_template("login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))  # Redirect to auth blueprint login


@bp.route("/profile")
@login_required
def profile():
    user_data = {
        "id": current_user.public_id,  # Assuming public_id exists
        "username": current_user.username,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "age": current_user.age,
        "gender": current_user.gender,
        "interested_in": current_user.interested_in,
        "bio": current_user.bio,
        "profile_picture": url_for(
            "static", filename=f"profile_pics/{current_user.profile_picture}"
        ),
        "is_verified": current_user.is_verified,
        "email": current_user.email,
    }
    return render_template("profile.html", user=user_data)


@bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    user = User.query.get(current_user.id)
    if request.method == "POST":
        user.username = request.form.get("username")
        try:
            age = int(request.form.get("age"))
        except ValueError:
            flash("Invalid age. Please enter a number.", "danger")
            return redirect(url_for("views.edit_profile"))  # Use blueprint name

        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if not profile:
            profile = Profile(user_id=current_user.id, name=current_user.username, age=age)
            db.session.add(profile)
        else:
            profile.age = age

        profile.gender = request.form.get("gender")
        profile.gender_preference = request.form.get("interested_in")
        profile.bio = request.form.get("bio")

        if "profile_picture" in request.files:
            file = request.files["profile_picture"]
            if file and allowed_file(file.filename):
                ext = file.filename.rsplit(".", 1)[1].lower()
                unique_filename = f"{uuid.uuid4()}.{ext}"
                filename = secure_filename(unique_filename)
                
                profile_pics_folder = current_app.config.get("PROFILE_PICS_FOLDER")
                os.makedirs(profile_pics_folder, exist_ok=True)
                
                filepath = os.path.join(profile_pics_folder, filename)
                file.save(filepath)
                
                if profile.profile_picture and profile.profile_picture != "default_avatar.png":
                    try:
                        old_path = os.path.join(profile_pics_folder, profile.profile_picture)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    except OSError as e:
                        print(f"Error removing old profile picture: {e}")
                profile.profile_picture = filename
            elif file.filename != "":
                flash(
                    "Invalid file type for profile picture. Allowed types are png, jpg, jpeg, gif.",
                    "danger",
                )

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("views.profile"))  # Use blueprint name

    return render_template("edit_profile.html", user=user)


@bp.route("/browse")
@login_required
@limiter.limit("60/hour")
def browse():
    current_user_id = current_user.id
    current_user_interest = current_user.interested_in

    target_genders = []
    if current_user_interest == "Male":
        target_genders.append("Male")
    elif current_user_interest == "Female":
        target_genders.append("Female")
    elif current_user_interest == "Everyone":
        target_genders.extend(["Male", "Female", "Other"])

    # Simplified query: exclude self, require verified, match interest, and not already liked/matched
    potential_matches = (
        User.query.filter(
            User.id != current_user_id,
            User.is_verified,
            User.gender.in_(target_genders) if target_genders else True,
            ~User.likes_received.any(
                Like.liker_id == current_user_id
            ),  # User has not received a like from this potential match
            ~User.likes_given.any(
                Like.liked_id == current_user_id
            ),  # User has not liked this potential match
            ~User.matches_initiated.any(
                Match.user2_id == current_user_id
            ),  # User has not initiated a match with this potential match
            ~User.matches_received.any(
                Match.user1_id == current_user_id
            ),  # User has not received a match from this potential match
        )
        .order_by(User.id)
        .limit(20)
        .all()
    )

    for user in potential_matches:
        user.profile_picture_url = url_for(
            "static", filename=f"profile_pics/{user.profile_picture}"
        )

    return render_template("browse.html", users=potential_matches)


@bp.route("/like", methods=["POST"])
@login_required
@limiter.limit("100/hour")
def like_user():
    data = request.get_json()
    liked_user_public_id = data.get("user_id")

    if not liked_user_public_id:
        return jsonify({"error": "User ID is required"}), 400

    current_user_id = current_user.id

    user_to_like = User.query.filter_by(public_id=liked_user_public_id).first()
    if not user_to_like:
        return jsonify({"error": "User not found"}), 404

    liked_user_id_int = user_to_like.id

    if liked_user_id_int == current_user_id:
        return jsonify({"error": "Cannot like yourself"}), 400

    existing_like = Like.query.filter_by(
        liker_id=current_user_id, liked_id=liked_user_id_int
    ).first()
    if existing_like:
        return jsonify({"message": "You have already liked this user"}), 200

    new_like = Like(liker_id=current_user_id, liked_id=liked_user_id_int)
    db.session.add(new_like)

    mutual_like = Like.query.filter_by(
        liker_id=liked_user_id_int, liked_id=current_user_id
    ).first()

    if mutual_like:
        user1_id = min(current_user_id, liked_user_id_int)
        user2_id = max(current_user_id, liked_user_id_int)
        new_match = Match(user1_id=user1_id, user2_id=user2_id)
        db.session.add(new_match)

        liker_user = User.query.get(current_user_id)
        liked_user = User.query.get(liked_user_id_int)

        notification_liker = Notification(
            user_id=liked_user_id_int,
            type="match",
            related_user_id=current_user_id,
            content=f"It's a match with {liker_user.username}!",
        )
        db.session.add(notification_liker)

        notification_liked = Notification(
            user_id=current_user_id,
            type="match",
            related_user_id=liked_user_id_int,
            content=f"It's a match with {liked_user.username}!",
        )
        db.session.add(notification_liked)

        # Use socketio.emit
        socketio.emit(
            "new_match",
            {
                "user_id": liked_user_id_int,
                "matched_with": {
                    "id": liker_user.public_id,
                    "username": liker_user.username,
                    "profile_picture": liker_user.profile_picture,
                    "timestamp": new_match.timestamp.isoformat(),
                },
            },
            room=str(liked_user.public_id),
        )

        socketio.emit(
            "new_match",
            {
                "user_id": current_user_id,
                "matched_with": {
                    "id": liked_user.public_id,
                    "username": liked_user.username,
                    "profile_picture": liked_user.profile_picture,
                    "timestamp": new_match.timestamp.isoformat(),
                },
            },
            room=str(liker_user.public_id),
        )

    else:
        liker_user = User.query.get(current_user_id)
        liked_user = User.query.get(liked_user_id_int)
        notification = Notification(
            user_id=liked_user_id_int,
            type="like",
            related_user_id=current_user_id,
            content=f"{liker_user.username} liked you!",
        )
        db.session.add(notification)

        socketio.emit(
            "new_like",
            {
                "user_id": liked_user_id_int,
                "liked_by": {
                    "id": liker_user.public_id,
                    "username": liker_user.username,
                    "profile_picture": liker_user.profile_picture,
                    "timestamp": new_like.timestamp.isoformat(),
                },
            },
            room=str(liked_user.public_id),
        )

    try:
        db.session.commit()
        return (
            jsonify({"message": "Action successful", "is_match": bool(mutual_like)}),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@bp.route("/unlike", methods=["POST"])
@login_required
@limiter.limit("100/hour")
def unlike_user():
    data = request.get_json()
    unliked_user_public_id = data.get("user_id")

    if not unliked_user_public_id:
        return jsonify({"error": "User ID is required"}), 400

    current_user_id = current_user.id
    user_to_unlike = User.query.filter_by(public_id=unliked_user_public_id).first()
    if not user_to_unlike:
        return jsonify({"error": "User not found"}), 404

    liked_user_id_int = user_to_unlike.id  # Use the actual ID of the user to unlike

    like = Like.query.filter_by(
        liker_id=current_user_id, liked_id=liked_user_id_int
    ).first()
    if like:
        db.session.delete(like)

    db.session.commit()
    return jsonify({"message": "User unliked successfully"}), 200


@bp.route("/matches")
@login_required
def matches():
    current_user_id = current_user.id
    user_matches = (
        Match.query.filter(
            ((Match.user1_id == current_user_id) | (Match.user2_id == current_user_id))
            & ~(Match.user1_deleted & Match.user2_deleted)
        )
        .order_by(Match.timestamp.desc())
        .all()
    )

    matches_list = []
    for match in user_matches:
        other_user_id = (
            match.user2_id if match.user1_id == current_user_id else match.user1_id
        )
        other_user = User.query.get(other_user_id)

        if other_user:
            user_deleted_match = (
                match.user1_id == current_user_id and match.user1_deleted
            ) or (match.user2_id == current_user_id and match.user2_deleted)

            if not user_deleted_match:
                matches_list.append(
                    {
                        "id": match.id,
                        "user_id": other_user.public_id,
                        "username": other_user.username,
                        "profile_picture": url_for(
                            "static",
                            filename=f"profile_pics/{other_user.profile_picture}",
                        ),
                        "last_message_preview": "Start chatting...",
                        "timestamp": match.timestamp.isoformat(),
                        "user_deleted": user_deleted_match,
                    }
                )

    return render_template("matches.html", matches=matches_list)


@bp.route("/messages/<match_id>")
@login_required
def messages(match_id):
    current_user_id = current_user.id
    try:
        match_id_int = int(match_id)
    except ValueError:
        flash("Invalid match ID", "danger")
        return redirect(url_for("views.matches"))  # Use blueprint name

    match = Match.query.get(match_id_int)
    if not match:
        flash("Match not found.", "danger")
        return redirect(url_for("views.matches"))  # Use blueprint name

    if match.user1_id == current_user_id:
        other_user_id = match.user2_id
        if match.user1_deleted:
            flash("This conversation has been ended by the other user.", "info")
            return redirect(url_for("views.matches"))  # Use blueprint name
    elif match.user2_id == current_user_id:
        other_user_id = match.user1_id
        if match.user2_deleted:
            flash("This conversation has been ended by the other user.", "info")
            return redirect(url_for("views.matches"))  # Use blueprint name
    else:
        flash("You do not have access to this conversation.", "danger")
        return redirect(url_for("views.matches"))  # Use blueprint name

    other_user = User.query.get(other_user_id)
    if not other_user:
        flash("User not found.", "danger")
        return redirect(url_for("views.matches"))  # Use blueprint name

    messages = (
        Message.query.filter(
            (
                (Message.sender_id == current_user_id)
                & (Message.receiver_id == other_user_id)
            )
            | (
                (Message.sender_id == other_user_id)
                & (Message.receiver_id == current_user_id)
            )
        )
        .order_by(Message.timestamp)
        .all()
    )

    for msg in messages:
        if msg.receiver_id == current_user_id and not msg.read:
            msg.read = True
    db.session.commit()

    message_list = []
    for msg in messages:
        message_list.append(
            {
                "id": msg.id,
                "sender_id": msg.sender.public_id,  # Assuming public_id exists
                "username": msg.sender.username,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "read": msg.read,
                "is_current_user": msg.sender_id == current_user_id,
            }
        )

    return render_template(
        "messages.html", messages=message_list, other_user=other_user, match_id=match_id
    )


@bp.route("/send_message/<match_id>", methods=["POST"])
@login_required
@limiter.limit("100/hour")
def send_message(match_id):
    data = request.get_json()
    content = data.get("content")

    if not content:
        return jsonify({"error": "Message content cannot be empty"}), 400

    current_user_id = current_user.id
    try:
        match_id_int = int(match_id)
    except ValueError:
        return jsonify({"error": "Invalid match ID"}), 400

    match = Match.query.get(match_id_int)
    if not match:
        return jsonify({"error": "Match not found"}), 404

    if match.user1_id == current_user_id:
        other_user_id = match.user2_id
        if match.user1_deleted:
            return jsonify({"error": "Cannot send message, chat has been ended"}), 400
    elif match.user2_id == current_user_id:
        other_user_id = match.user1_id
        if match.user2_deleted:
            return jsonify({"error": "Cannot send message, chat has been ended"}), 400
    else:
        return jsonify({"error": "You are not part of this match"}), 403

    other_user = User.query.get(other_user_id)
    if not other_user:
        return jsonify({"error": "Other user not found"}), 404

    new_message = Message(
        sender_id=current_user_id, receiver_id=other_user_id, content=content
    )
    db.session.add(new_message)

    notification = Notification(
        user_id=other_user_id,
        type="message",
        related_user_id=current_user_id,
        content=f"{current_user.username}: {content[:50]}{'...' if len(content)>50 else ''}",
    )
    db.session.add(notification)

    try:
        db.session.commit()
        message_data = {
            "id": new_message.id,
            "sender_id": current_user.public_id,  # Assuming public_id exists
            "username": current_user.username,
            "content": new_message.content,
            "timestamp": new_message.timestamp.isoformat(),
            "read": new_message.read,
            "is_current_user": True,
        }
        socketio.emit("new_message", message_data, room=str(other_user.public_id))
        socketio.emit(
            "notification",
            {
                "user_id": other_user_id,
                "type": "message",
                "related_user_id": current_user.public_id,
                "content": notification.content,
            },
            room=str(other_user.public_id),
        )

        return (
            jsonify(
                {"message": "Message sent successfully", "message_data": message_data}
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# --- Flask-Migrate commands ---
# Note: These are typically run via the Flask CLI, not directly in app.py
# Example: flask db init, flask db migrate, flask db upgrade
