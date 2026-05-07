import os
from flask import Blueprint, request, jsonify, current_app
from app.models import Profile
from app import db
from app.views import get_user_from_token

bp = Blueprint("profile", __name__, url_prefix="/api/profile")


def validate_and_get_errors(data):
    """Validate profile data and return errors dict."""
    errors = {}

    name = data.get("name")
    age = data.get("age")

    if not name:
        errors["name"] = "Name is required"
    elif len(name) < 2:
        errors["name"] = "Name must be at least 2 characters"
    elif len(name) > 50:
        errors["name"] = "Name must be at most 50 characters"

    if not age:
        errors["age"] = "Age is required"
    elif age < 18:
        errors["age"] = "Must be at least 18 years old"
    elif age > 100:
        errors["age"] = "Age must be less than 100"

    interests = data.get("interests", "")
    if isinstance(interests, str):
        interests = [i.strip() for i in interests.split(",") if i.strip()]
    elif isinstance(interests, list):
        interests = interests

    if len(interests) < 3:
        errors["interests"] = "At least 3 interests are required"

    bio = data.get("bio", "")
    if len(bio) > 500:
        errors["bio"] = "Bio must be at most 500 characters"

    occupation = data.get("occupation", "")
    if len(occupation) > 100:
        errors["occupation"] = "Occupation must be at most 100 characters"

    gender = data.get("gender", "")
    valid_genders = ["male", "female", "non_binary", "other", "prefer_not_to_say", ""]
    if gender not in valid_genders:
        errors["gender"] = "Invalid gender"

    gender_preference = data.get("gender_preference", "all")
    valid_preferences = ["male", "female", "all", ""]
    if gender_preference not in valid_preferences:
        errors["gender_preference"] = "Invalid gender preference"

    relationship_goal = data.get("relationship_goal", "")
    valid_goals = [
        "friendship",
        "casual_dating",
        "serious_relationship",
        "marriage",
        "",
    ]
    if relationship_goal not in valid_goals:
        errors["relationship_goal"] = "Invalid relationship goal"

    return errors


@bp.route("", methods=["POST"])
def create_profile():
    """Create a new profile for the authenticated user."""
    user = get_user_from_token()
    if not user:
        return jsonify({"error": "Authentication required"}), 401

    existing = Profile.query.filter_by(user_id=user.user_id).first()
    if existing:
        return jsonify({"error": "Profile already exists"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"errors": {"data": "No data provided"}}), 400

    errors = validate_and_get_errors(data)
    if errors:
        return jsonify({"errors": errors}), 400

    interests = data.get("interests", "")
    if isinstance(interests, str):
        interests = [i.strip() for i in interests.split(",") if i.strip()]
    elif isinstance(interests, list):
        interests = interests

    profile = Profile(
        user_id=user.user_id,
        name=data["name"],
        age=data["age"],
        bio=data.get("bio", ""),
        interests=interests,
        gender=data.get("gender", ""),
        gender_preference=data.get("gender_preference", "all"),
        relationship_goal=data.get("relationship_goal", ""),
        occupation=data.get("occupation", ""),
        visibility=data.get("visibility", True),
    )
    db.session.add(profile)
    db.session.commit()

    return jsonify(profile.to_dict()), 201


@bp.route("", methods=["GET"])
def get_my_profile():
    """Get current user's profile."""
    user = get_user_from_token()
    if not user:
        return jsonify({"error": "Authentication required"}), 401

    profile = Profile.query.filter_by(user_id=user.user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    return jsonify(profile.to_dict()), 200


@bp.route("/<int:user_id>", methods=["GET"])
def get_other_profile(user_id):
    """Get another user's profile."""
    user = get_user_from_token()

    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    if not profile.visibility:
        if not user or user.user_id != user_id:
            return jsonify({"error": "Profile is private"}), 403

    return jsonify(profile.to_dict()), 200


@bp.route("", methods=["PUT"])
def update_profile():
    """Update current user's profile."""
    user = get_user_from_token()
    if not user:
        return jsonify({"error": "Authentication required"}), 401

    profile = Profile.query.filter_by(user_id=user.user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"errors": {"data": "No data provided"}}), 400

    errors = validate_and_get_errors(data)
    if errors:
        return jsonify({"errors": errors}), 400

    interests = data.get("interests")
    if interests:
        if isinstance(interests, str):
            interests = [i.strip() for i in interests.split(",") if i.strip()]
        profile.interests = interests

    profile.name = data.get("name", profile.name)
    profile.age = data.get("age", profile.age)
    profile.bio = data.get("bio", profile.bio or "")
    profile.gender = data.get("gender", profile.gender or "")
    profile.gender_preference = data.get(
        "gender_preference", profile.gender_preference or "all"
    )
    profile.relationship_goal = data.get(
        "relationship_goal", profile.relationship_goal or ""
    )
    profile.occupation = data.get("occupation", profile.occupation or "")
    profile.visibility = data.get("visibility", profile.visibility)

    db.session.commit()

    return jsonify(profile.to_dict()), 200


@bp.route("/picture", methods=["POST"])
def upload_picture():
    """Upload a profile picture."""
    user = get_user_from_token()
    if not user:
        return jsonify({"error": "Authentication required"}), 401

    profile = Profile.query.filter_by(user_id=user.user_id).first()
    if not profile:
        return jsonify({"error": "Create a profile first"}), 400

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "No file selected"}), 400

    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    ext = os.path.splitext(file.filename.lower())[1]
    if ext not in allowed_extensions:
        return jsonify({"error": "Invalid file type. Allowed: jpg, png, webp"}), 400

    import uuid

    filename = f"{uuid.uuid4()}{ext}"
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "./uploads")
    if not os.path.isabs(upload_folder):
        upload_folder = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), upload_folder
        )
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    profile.profile_picture = filename
    db.session.commit()

    return jsonify({"message": "Profile picture uploaded", "filename": filename}), 200
