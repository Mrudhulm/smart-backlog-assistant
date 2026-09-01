import os
import sys
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from pypdf import PdfReader

# Ensure parent directory is in python path to import core src modules
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.ai_client import AIBacklogClient

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super-secret-fallback-key-change-me")
app.config.update(
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("APP_ENV") == "production",
    REMEMBER_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_SAMESITE="Lax",
)

APP_USERNAME = os.getenv("APP_USERNAME", "mrudhul")
APP_PASSWORD = os.getenv("APP_PASSWORD", "password123")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = PROJECT_ROOT / "inputs"
OUTPUT_FOLDER = PROJECT_ROOT / "outputs"
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

USERS = {
    APP_USERNAME.lower(): {
        "password_hash": generate_password_hash(APP_PASSWORD),
        "id": APP_USERNAME.lower(),
    }
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        return User(user_id)
    return None

def get_recent_reports():
    if not OUTPUT_FOLDER.exists():
        return []
    return sorted([f.name for f in OUTPUT_FOLDER.glob("*.html")], reverse=True)


def render_dashboard(data=None, error=None):
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template(
        "dashboard.html",
        data=data,
        reports=get_recent_reports(),
        error=error,
        current_timestamp=current_timestamp,
    )


def format_generation_error(error):
    error_text = str(error)
    if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
        return (
            "Gemini API quota is exhausted for the current project/model. "
            "Wait for the quota reset or use an API project with available quota, then try again."
        )
    return f"Backlog generation failed: {error_text}"


@app.after_request
def add_security_headers(response):
    """Inject security response headers to mitigate XSS and clickjacking."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    if isinstance(error, HTTPException):
        return error
    app.logger.exception("Unhandled exception: %s", error)
    return render_dashboard(error="An unexpected server error occurred. Please check the API configuration and try again."), 500

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")

        expected_username = APP_USERNAME.lower()
        if username == expected_username and check_password_hash(USERS[expected_username]["password_hash"], password):
            user = User(username)
            login_user(user)
            return redirect(url_for("index"))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html", error=None)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    return render_dashboard(data=None, error=None)


@app.route("/process", methods=["POST"])
@login_required
def process():
    username = request.form.get("username", current_user.id).strip().lower()
    raw_text = request.form.get("raw_text", "").strip()
    uploaded_file = request.files.get("file")

    if uploaded_file and uploaded_file.filename != "":
        # Security: Sanitize filename to block path traversal attacks
        safe_filename = secure_filename(uploaded_file.filename)
        file_path = UPLOAD_FOLDER / safe_filename
        uploaded_file.save(file_path)

        ext = file_path.suffix.lower()
        if ext == ".pdf":
            reader = PdfReader(file_path)
            raw_text = "".join([page.extract_text() or "" for page in reader.pages])
        elif ext in [".txt", ".md"]:
            raw_text = file_path.read_text(encoding="utf-8")

    if not raw_text:
        return redirect(url_for("index"))

    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    project_slug = f"{username}-{date_str}"

    try:
        if not os.getenv("GEMINI_API_KEY"):
            raise RuntimeError("GEMINI_API_KEY is missing. Set it in the environment or .env file.")

        ai_client = AIBacklogClient()
        backlog_data = ai_client.generate_backlog(raw_text)
        dump_data = backlog_data.model_dump()
        # Always use the container's current date and time, even if Gemini returns a date-only value.
        dump_data["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        json_output_path = OUTPUT_FOLDER / f"{project_slug}.json"
        html_output_path = OUTPUT_FOLDER / f"{project_slug}.html"

        with open(json_output_path, "w", encoding="utf-8") as f:
            import json
            json.dump(dump_data, f, indent=4)

        from src.parser import DocumentParser
        DocumentParser.save_html_dashboard(dump_data, str(html_output_path))
    except Exception as exc:
        app.logger.exception("Backlog generation failed")
        return render_dashboard(error=format_generation_error(exc))

    return render_dashboard(data=dump_data, error=None)

@app.route("/outputs/<path:filename>")
@login_required
def serve_output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    # Security: Disable debug mode in production environments
    app.run(host="0.0.0.0", port=5000, debug=False)