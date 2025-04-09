from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)  # Define Flask app before using it
CORS(app)  # Now apply CORS to the defined app

@app.route('/check_password', methods=['POST'])
def check_password():
    try:
        data = request.get_json()
        password = data.get("password", "")

        if not password:
            return jsonify({"error": "Password is required"}), 400

        strength = "Weak"
        if len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isupper() for char in password) and any(char in "!@#$%^&*()" for char in password):
            strength = "Strong"
        elif len(password) >= 6:
            strength = "Medium"

        return jsonify({"strength": strength})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
