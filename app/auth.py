import secrets
import re
from flask import Blueprint, request, jsonify
from app.models import User, Profile
from app import db, limiter
from app.email_utils import send_email
from flask_login import login_user, logout_user

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.route("/register", methods=["POST"])
@limiter.limit("5/minute")
def register():
    data = request.get_json()
    if not data or not all(
        k in data for k in ("email", "password", "confirm_password")
    ):
        return jsonify({"errors": {"email": "Missing fields"}}), 400

    if data["password"] != data["confirm_password"]:
        return jsonify({"errors": {"password": "Passwords do not match"}}), 400

    from app.views import validate_password_strength

    validation = validate_password_strength(data["password"])
    if not validation["is_valid"]:
        return jsonify({"errors": {"password": validation["errors"]}}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"errors": {"email": "Email already exists"}}), 400

    import re

    if not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
        return jsonify({"errors": {"email": "Invalid email format"}}), 400

    user = User(email=data["email"], username=data["email"].split("@")[0])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    from flask import current_app

    verification_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:5173')}/verify/{user.verification_token}"
    subject = "Verify your email - Dating App"
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Verify your email</h2>
            <p>Thanks for signing up! Please click the link below to verify your email:</p>
            <p><a href="{verification_url}" style="background: #e74c3c; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Verify Email</a></p>
            <p>Or copy and paste this link into your browser:</p>
            <p style="color: #666;">{verification_url}</p>
            <p style="color: #999; font-size: 12px;">This link expires in 7 days.</p>
        </body>
    </html>
    """

    current_app.logger.info(
        f"[REGISTER] User registered: {user.email}, user_id={user.user_id}"
    )
    current_app.logger.info(
        f"[REGISTER] Verification token generated: {user.verification_token[:20]}..."
    )

    email_sent = send_email(user.email, subject, body)
    if email_sent:
        current_app.logger.info(
            f"[REGISTER] Verification email sent successfully to {user.email}"
        )
    else:
        current_app.logger.error(
            f"[REGISTER] FAILED to send verification email to {user.email}"
        )

    return jsonify({"message": "User registered", "user_id": user.user_id}), 201


@bp.route(
    "/login", methods=["POST", "GET"]
)  # Allow GET requests for testing/ Playwright navigation
def login():
    if request.method == "POST":
        data = request.get_json()
        if not data or not all(k in data for k in ("email", "password")):
            return jsonify({"errors": {"email": "Missing email or password"}}), 400

        user = User.query.filter_by(email=data.get("email")).first()
        if user and user.check_password(data.get("password")):
            if not user.is_verified:
                return (
                    jsonify(
                        {"errors": {"general": ["Please verify your email first"]}}
                    ),
                    401,
                )
            login_user(user)
            from app.views import generate_token

            token = generate_token(user_id=user.user_id)
            profile = user.profile
            return (
                jsonify(
                    {
                        "token": token,
                        "user": {
                            "id": user.id,
                            "email": user.email,
                            "is_verified": user.is_verified,
                            "has_profile": profile is not None,
                            "name": profile.name if profile else None,
                        },
                    }
                ),
                200,
            )
        return jsonify({"error": "Invalid credentials"}), 401

    elif request.method == "GET":
        return (
            jsonify({"message": "Login API endpoint. Use POST for authentication."}),
            200,
        )

    return jsonify({"error": "Method not allowed"}), 405


@bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify({"message": "Logged out"}), 200


@bp.route("/me", methods=["GET"])
def get_current_user():
    """Get current authenticated user."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid authorization header"}), 401

    token = auth_header.split(" ")[1]
    try:
        from app.views import verify_token

        payload = verify_token(token, token_type="auth")
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401

        user = db.session.get(User, payload["user_id"])
        if not user:
            return jsonify({"error": "User not found"}), 404

        profile = Profile.query.filter_by(user_id=user.id).first()
        return (
            jsonify(
                {
                    "id": user.id,
                    "email": user.email,
                    "is_verified": user.is_verified,
                    "has_profile": profile is not None,
                    "name": profile.name if profile else None,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 401


@bp.route("/verify/<token>", methods=["GET"])
def verify_email(token):
    """Verify user email with token."""
    from flask import current_app

    current_app.logger.info(
        f"[VERIFY_EMAIL] Verification request received with token: {token[:20]}..."
    )

    user = User.query.filter_by(verification_token=token).first()
    if not user:
        current_app.logger.warning(
            f"[VERIFY_EMAIL] Invalid token provided: {token[:20]}..."
        )
        return jsonify({"error": "Invalid verification token"}), 404

    if user.is_verified:
        current_app.logger.info(
            f"[VERIFY_EMAIL] Email already verified for user_id={user.user_id}, email={user.email}"
        )
        return jsonify({"message": "Email already verified"}), 200

    current_app.logger.info(
        f"[VERIFY_EMAIL] Verifying email for user_id={user.user_id}, email={user.email}"
    )
    user.is_verified = True
    db.session.commit()
    current_app.logger.info(f"[VERIFY_EMAIL] SUCCESS - Email verified for {user.email}")

    return jsonify({"message": "Email verified successfully"}), 200


@bp.route("/resend-verification", methods=["POST"])
def resend_verification():
    """Resend verification email."""
    from flask import current_app

    data = request.get_json()
    email = data.get("email")

    current_app.logger.info(f"[RESEND_VERIFY] Request received for email: {email}")

    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        current_app.logger.warning(f"[RESEND_VERIFY] Invalid email format: {email}")
        return jsonify({"error": "Invalid email format"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        current_app.logger.info(
            "[RESEND_VERIFY] Email not found in database, returning generic response"
        )
        return (
            jsonify(
                {"message": "If the email exists, a verification link has been sent"}
            ),
            200,
        )

    if user.is_verified:
        current_app.logger.info(f"[RESEND_VERIFY] User already verified: {email}")
        return (
            jsonify(
                {"message": "If the email exists, a verification link has been sent"}
            ),
            200,
        )

    current_app.logger.info(
        f"[RESEND_VERIFY] Generating new verification token for user_id={user.user_id}"
    )
    user.verification_token = secrets.token_urlsafe(32)
    db.session.commit()
    current_app.logger.info("[RESEND_VERIFY] New token saved to database")

    verification_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:5173')}/verify/{user.verification_token}"
    subject = "Verify your email - Dating App"
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Verify your email</h2>
            <p>Thanks for signing up! Please click the link below to verify your email:</p>
            <p><a href="{verification_url}" style="background: #e74c3c; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Verify Email</a></p>
            <p>Or copy and paste this link into your browser:</p>
            <p style="color: #666;">{verification_url}</p>
            <p style="color: #999; font-size: 12px;">This link expires in 7 days.</p>
        </body>
    </html>
    """

    current_app.logger.info(f"[RESEND_VERIFY] Calling send_email for {email}")
    email_result = send_email(user.email, subject, body)
    if email_result:
        current_app.logger.info(
            f"[RESEND_VERIFY] Verification email sent successfully to {email}"
        )
    else:
        current_app.logger.error(
            f"[RESEND_VERIFY] FAILED to send verification email to {email}"
        )

    return jsonify({"message": "Verification email sent"}), 200


@bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    """Request password reset."""
    data = request.get_json()
    email = data.get("email")

    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"error": "Invalid email format"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        # Don't reveal if user exists
        return (
            jsonify({"message": "If the email exists, a reset link has been sent"}),
            200,
        )

    # Generate reset token (commented out for production use)
    # from app.views import generate_token
    # reset_token = generate_token(user_id=user.user_id, token_type="reset", expires_days=1)
    # In production, send email with reset link

    return jsonify({"message": "Password reset email sent"}), 200


@bp.route("/reset-password", methods=["POST"])
def reset_password():
    """Reset password with token."""
    data = request.get_json()
    token = data.get("token")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if not token:
        return jsonify({"error": "Token is required"}), 400
    if not password or not confirm_password:
        return jsonify({"error": "Password and confirmation are required"}), 400
    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    from app.views import validate_password_strength

    validation = validate_password_strength(password)
    if not validation["is_valid"]:
        return jsonify({"errors": {"password": validation["errors"]}}), 400

    from app.views import verify_token

    payload = verify_token(token, token_type="reset")
    if not payload:
        return jsonify({"error": "Invalid or expired token"}), 400

    user = db.session.get(User, payload["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.set_password(password)
    db.session.commit()
    return jsonify({"message": "Password reset successfully"}), 200


@bp.route("/refresh", methods=["POST"])
def refresh_token():
    """Refresh authentication token."""
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    from app.views import generate_token

    token = generate_token(user_id=user.user_id)
    profile = user.profile

    return (
        jsonify(
            {
                "token": token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "is_verified": user.is_verified,
                    "has_profile": profile is not None,
                },
            }
        ),
        200,
    )
