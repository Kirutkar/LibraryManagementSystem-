from flask import Blueprint, request, jsonify
from db import get_connection

search_bp = Blueprint('search', __name__)
#-------SEARCH FUNCTIONALITY BY TITLE OR AUTHOR---------

@search_bp.route('/books/search', methods=['GET'])

def search_books():
    connection = None
    cursor = None
    try:
        title = request.args.get('title', None)
        author = request.args.get('author', None)

        if not title and not author:
            return jsonify({"message": "Please provide at least 'title' or 'author' to search."}), 400

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM books WHERE"
        params = []

        if title:
            query += " title LIKE %s"
            params.append(f"%{title}%")
        if author:
            if title:
                query += " OR"
            query += " author LIKE %s"
            params.append(f"%{author}%")

        cursor.execute(query, params)
        books = cursor.fetchall()

        if not books:
            return jsonify({"message": "No books found"}), 404

        return jsonify(books), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()
