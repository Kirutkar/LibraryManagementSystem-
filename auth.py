import secrets
from flask import Blueprint, request, jsonify
from functools import wraps
from db import get_connection  # Ensure get_connection is defined

# Create Blueprint for auth
auth_bp = Blueprint('auth', __name__)

# Token Generation Route
@auth_bp.route('/generate-token', methods=['POST'])
def generate_token():
    connection = None
    cursor = None
    try:
        data = request.json
        email = data.get('email')

        if not email:
            return jsonify({"error": "Email is required"}), 400

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT id FROM members WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "Invalid email"}), 404

        token = secrets.token_hex(32)
        insert_query = "INSERT INTO tokens (member_id, token) VALUES (%s, %s)"
        cursor.execute(insert_query, (user['id'], token))
        connection.commit()
        return jsonify({"token": token}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()

# Token Authentication Decorator
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        connection = None
        cursor = None
        try:
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"error": "Token is missing"}), 401

            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM tokens WHERE token = %s"
            cursor.execute(query, (token,))
            token_data = cursor.fetchone()

            if not token_data:
                return jsonify({"error": "Invalid token"}), 403

            request.member_id = token_data['member_id']
            return f(*args, **kwargs)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

    return decorated_function
