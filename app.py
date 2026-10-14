"""
Oba-Byte Enterprises — website backend.

Serves the static site (index.html) and handles the contact form:
a POST to /api/contact emails the message to you via SMTP.

Run:
    pip install -r requirements.txt
    cp .env.example .env     # then edit .env with your Gmail + app password
    python app.py
    open http://localhost:8000
"""
import os
import re
import smtplib
import ssl
from email.message import EmailMessage

from flask import Flask, request, jsonify, send_from_directory

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")          # the Gmail you send FROM
SMTP_PASS = os.environ.get("SMTP_PASS", "")          # a Gmail "App Password"
MAIL_TO = os.environ.get("MAIL_TO", "obajeabrham24@gmail.com")
PORT = int(os.environ.get("PORT", "8000"))

app = Flask(__name__, static_folder=None)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@app.route("/")
def home():
    return send_from_directory(HERE, "index.html")


@app.route("/<path:path>")
def static_files(path):
    # serve any other file that sits next to app.py (css, images, etc.)
    full = os.path.join(HERE, path)
    if os.path.isfile(full):
        return send_from_directory(HERE, path)
    return ("Not found", 404)


@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify(error="Please fill in all three fields."), 400
    if not EMAIL_RE.match(email):
        return jsonify(error="That email address doesn't look right."), 400
    if len(message) > 5000:
        return jsonify(error="Message is too long."), 400

    if not SMTP_USER or not SMTP_PASS:
        # Not configured yet — don't pretend it was sent.
        return jsonify(error="Email is not configured on the server yet."), 503

    msg = EmailMessage()
    msg["Subject"] = f"New enquiry from {name} — Oba-Byte website"
    msg["From"] = SMTP_USER
    msg["To"] = MAIL_TO
    msg["Reply-To"] = email
    msg.set_content(
        f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}\n"
    )

    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
            server.starttls(context=ctx)
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
    except Exception as exc:
        app.logger.error("mail failed: %s", exc)
        return jsonify(error="Could not send right now. Please email us directly."), 502

    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
