import smtplib
import time
import json
from email.message import EmailMessage
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from flask import current_app


def _get_mail_config():
    return {
        "host": current_app.config.get("SMTP_HOST")
        or current_app.config.get("MAILTRAP_SMTP_HOST"),
        "port": current_app.config.get("SMTP_PORT")
        or current_app.config.get("MAILTRAP_SMTP_PORT"),
        "user": current_app.config.get("SMTP_USER")
        or current_app.config.get("MAILTRAP_SMTP_USER"),
        "password": current_app.config.get("SMTP_PASS")
        or current_app.config.get("MAILTRAP_SMTP_PASS"),
        "from_email": current_app.config.get("SMTP_FROM_EMAIL")
        or current_app.config.get("MAILTRAP_FROM_EMAIL"),
        "use_tls": current_app.config.get("SMTP_USE_TLS", True),
        "use_ssl": current_app.config.get("SMTP_USE_SSL", False),
    }


def _send_resend_email(to_email, subject, body):
    api_key = current_app.config.get("RESEND_API_KEY")
    api_url = current_app.config.get("RESEND_API_URL")
    from_email = current_app.config.get("EMAIL_FROM")

    current_app.logger.info(
        f"[EMAIL] Resend configuration: api_key_set={'***' if api_key else 'NONE'}, api_url={api_url}, from_email={from_email}"
    )

    if not api_key:
        current_app.logger.error(
            "[EMAIL ERROR] RESEND_API_KEY is not configured in production environment"
        )
        current_app.logger.error(
            f"[EMAIL ERROR] Available env vars: RESEND_API_KEY={'***' if api_key else 'NOT SET'}, RESEND_API_URL={api_url}, EMAIL_FROM={from_email}"
        )
        return False

    if not from_email:
        current_app.logger.error(
            "[EMAIL ERROR] EMAIL_FROM is not configured in production environment"
        )
        current_app.logger.error(
            "[EMAIL ERROR] EMAIL_FROM is required for Resend - must be a verified sender domain in Resend dashboard"
        )
        return False

    current_app.logger.info("[EMAIL] Preparing to send email via Resend API")
    current_app.logger.info(f"[EMAIL] To: {to_email}")
    current_app.logger.info(f"[EMAIL] Subject: {subject}")
    current_app.logger.info(f"[EMAIL] From: {from_email}")

    payload = json.dumps(
        {
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "html": body,
        }
    ).encode("utf-8")

    current_app.logger.debug(f"[EMAIL] Full payload: {payload.decode('utf-8')}")

    request = Request(
        api_url,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "driftdater/1.0",
        },
        method="POST",
    )

    try:
        current_app.logger.info(
            f"[EMAIL] Sending POST request to Resend API: {api_url}"
        )
        with urlopen(request, timeout=30) as response:
            response_body = response.read().decode("utf-8")
            current_app.logger.info(
                f"[EMAIL] Resend API response status: {response.status}"
            )
            current_app.logger.info(
                f"[EMAIL] Resend API response body: {response_body}"
            )

            if 200 <= response.status < 300:
                current_app.logger.info(
                    f"[EMAIL] SUCCESS - Email sent successfully to {to_email}"
                )
                return True

            current_app.logger.error(
                f"[EMAIL ERROR] Resend API returned status {response.status}: {response_body}"
            )
            return False
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        current_app.logger.error(
            f"[EMAIL ERROR] Resend HTTP error: status={exc.code}, reason={exc.reason}, body={error_body}"
        )
        current_app.logger.error(
            "[EMAIL ERROR] This usually means: 1) Sender email not verified in Resend, 2) API key is invalid, 3) Rate limit exceeded"
        )
        return False
    except URLError as exc:
        current_app.logger.error(
            f"[EMAIL ERROR] Network error reaching Resend API: {exc.reason}"
        )
        current_app.logger.error(
            "[EMAIL ERROR] Check network connectivity and firewall settings"
        )
        return False
    except Exception as exc:
        current_app.logger.error(
            f"[EMAIL ERROR] Unexpected error sending email to {to_email}: {type(exc).__name__}: {exc}"
        )
        current_app.logger.exception("[EMAIL ERROR] Full exception traceback:")
        return False


def _send_smtp_email(to_email, subject, body):
    mail_config = _get_mail_config()

    current_app.logger.info(
        "[EMAIL] Attempting SMTP fallback"
    )
    current_app.logger.info(
        "[EMAIL] SMTP credentials configured"
    )

    if not mail_config["user"] or not mail_config["password"]:
        if current_app.config.get("DEBUG"):
            current_app.logger.info(
                "[MOCK EMAIL] DEBUG mode - email not actually sent"
            )
            current_app.logger.info(f"[MOCK EMAIL] To: {to_email}")
            current_app.logger.info(f"[MOCK EMAIL] Subject: {subject}")
            current_app.logger.info(f"[MOCK EMAIL] Body preview: {body[:200]}...")
            return True

        current_app.logger.error("[EMAIL ERROR] SMTP_USER/SMTP_PASS are not configured")
        return False

    try:
        current_app.logger.info(
        "[EMAIL] Connecting to SMTP server"
    )

        msg = EmailMessage()
        msg["From"] = mail_config["from_email"]
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content("Please view this email in an HTML-compatible email client.")
        msg.add_alternative(body, subtype="html")

        current_app.logger.info(
            f"[EMAIL] SMTP message prepared: from={mail_config['from_email']}, to={to_email}"
        )

        smtp_class = smtplib.SMTP_SSL if mail_config["use_ssl"] else smtplib.SMTP
        current_app.logger.info(f"[EMAIL] Using SMTP class: {smtp_class.__name__}")

        with smtp_class(mail_config["host"], mail_config["port"], timeout=30) as server:
            current_app.logger.info(f"[EMAIL] SMTP connection established")
            if mail_config["use_tls"] and not mail_config["use_ssl"]:
                current_app.logger.info(f"[EMAIL] Starting TLS encryption")
                server.starttls()
            current_app.logger.info(f"[EMAIL] Attempting SMTP authentication")
            server.login(mail_config["user"], mail_config["password"])
            current_app.logger.info(f"[EMAIL] SMTP authenticated successfully")
            server.send_message(msg)
            current_app.logger.info(f"[EMAIL] Message sent successfully")

        current_app.logger.info(f"[EMAIL] SUCCESS - Email sent to {to_email} via SMTP")
        return True
    except Exception as exc:
        current_app.logger.error(
            f"[EMAIL ERROR] SMTP send failed: {type(exc).__name__}: {exc}"
        )
        current_app.logger.exception("[EMAIL ERROR] Full SMTP exception traceback:")
        return False


def send_email(to_email, subject, body):
    """Send an HTML email using the configured provider."""
    current_app.logger.info("===== EMAIL REQUEST STARTED =====")
    current_app.logger.info(f"[EMAIL] Target: {to_email}")
    current_app.logger.info(f"[EMAIL] Subject: {subject}")

    if not current_app.config.get("TESTING"):
        time.sleep(1)
    else:
        current_app.logger.info("[MOCK EMAIL] TESTING mode enabled")
        current_app.logger.info(f"[MOCK EMAIL] To: {to_email}")
        current_app.logger.info(f"[MOCK EMAIL] Subject: {subject}")
        current_app.logger.info(f"[MOCK EMAIL] Body preview: {body[:200]}...")
        current_app.logger.info("===== EMAIL REQUEST COMPLETED =====")
        return True

    provider = current_app.config.get("EMAIL_PROVIDER", "smtp").lower()
    current_app.logger.info(f"[EMAIL] Email provider configured: {provider}")

    if provider == "resend":
        current_app.logger.info("[EMAIL] Using Resend API provider")
        current_app.logger.info("[EMAIL] Checking Resend configuration...")
        result = _send_resend_email(to_email, subject, body)
        current_app.logger.info(
            f"[EMAIL] Resend send result: {'SUCCESS' if result else 'FAILED'}"
        )
        current_app.logger.info("===== EMAIL REQUEST COMPLETED =====")
        return result

    current_app.logger.info("[EMAIL] Using SMTP provider (fallback)")
    result = _send_smtp_email(to_email, subject, body)
    current_app.logger.info(
        f"[EMAIL] SMTP send result: {'SUCCESS' if result else 'FAILED'}"
    )
    current_app.logger.info(f"[EMAIL] ===== EMAIL REQUEST COMPLETED =====")
    return result
