from flask import Flask, render_template, request, jsonify
from werkzeug.security import generate_password_hash
from app import app, db  # Import Flask app and database
from models import User   # Import User model
import re  # For regex password strength checking

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required!"}), 400

        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Save user to the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

    return render_template("index.html")


@app.route("/check_password", methods=["POST"])
def check_password():
    data = request.get_json()
    password = data.get("password", "")

    if not password:
        return jsonify({"error": "Password is required!"}), 400

    strength = get_password_strength(password)
    return jsonify({"strength": strength})


def get_password_strength(password):
    """Function to determine password strength"""
    if len(password) < 6:
        return "Weak"
    elif len(password) >= 8 and re.search(r"\d", password) and re.search(r"[A-Z]", password) and re.search(r"\W", password):
        return "Strong"
    else:
        return "Medium"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure database tables are created
    app.run(debug=True)
