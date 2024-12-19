from flask import Blueprint, request, jsonify
from db import get_connection
from auth import token_required

members_bp = Blueprint('members', __name__)

# CREATE a new member
@members_bp.route('/members', methods=['POST'])
def create_member():
    connection = None
    cursor = None
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        joined_date = data.get('joined_date')

        connection = get_connection()
        cursor = connection.cursor()
        query = '''INSERT INTO members (name, email, phone, joined_date)
                   VALUES (%s, %s, %s, %s)'''
        cursor.execute(query, (name, email, phone, joined_date))
        connection.commit()
        return jsonify({"message": "Member created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()

# READ all members
@members_bp.route('/members', methods=['GET'])
@token_required
def get_members():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM members')
        members = cursor.fetchall()
        if not members:
            return jsonify({"message": "No members found"}), 404
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()

# READ a single member by ID
@members_bp.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM members WHERE id = %s', (member_id,))
        member = cursor.fetchone()
        if not member:
            return jsonify({"message": "Member not found"}), 404
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()

# UPDATE a member
@members_bp.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    connection = None
    cursor = None
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        joined_date = data.get('joined_date')

        connection = get_connection()
        cursor = connection.cursor()
        query = '''UPDATE members
                   SET name = %s, email = %s, phone = %s, joined_date = %s
                   WHERE id = %s'''
        cursor.execute(query, (name, email, phone, joined_date, member_id))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Member not found"}), 404

        return jsonify({"message": "Member updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()

# DELETE a member by ID
@members_bp.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = 'DELETE FROM members WHERE id = %s'
        cursor.execute(query, (member_id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Member not found"}), 404

        return jsonify({"message": "Member deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()
