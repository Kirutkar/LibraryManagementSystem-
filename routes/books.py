from flask import Blueprint, request, jsonify
from db import get_connection

books_bp = Blueprint('books', __name__)

@books_bp.route('/books', methods=['POST'])  # CREATE
def create_book():
    connection = None
    cursor = None
    try:
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        published_year = data.get('published_year')
        genre = data.get('genre')
        quantity = data.get('quantity')

        connection = get_connection()
        cursor = connection.cursor()
        query = '''INSERT INTO books (title, author, published_year, genre, quantity)
                   VALUES (%s, %s, %s, %s, %s)'''
        cursor.execute(query, (title, author, published_year, genre, quantity))
        connection.commit()
        return jsonify({"message": "Book created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@books_bp.route('/books', methods=['GET'])  # READ ALL
def get_books():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
        return jsonify(books), 200 if books else ({"message": "No books found"}, 404)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@books_bp.route('/books/<int:book_id>', methods=['GET'])  # READ BY ID
def get_book(book_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM books WHERE id = %s', (book_id,))
        book = cursor.fetchone()
        if not book:
            return jsonify({"message": "Book not found"}), 404
        return jsonify(book), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()
    pass

@books_bp.route('/books/<int:book_id>', methods=['PUT'])  # UPDATE
def update_book(book_id):
    connection = None
    cursor = None
    try:
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        published_year = data.get('published_year')
        genre = data.get('genre')
        quantity = data.get('quantity')

        connection = get_connection()
        cursor = connection.cursor()
        query = '''UPDATE books
                       SET title = %s, author = %s, published_year = %s, genre = %s, quantity = %s
                       WHERE id = %s'''
        cursor.execute(query, (title, author, published_year, genre, quantity, book_id))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Book not found"}), 404

        return jsonify({"message": "Book updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()
    pass

@books_bp.route('/books/<int:book_id>', methods=['DELETE'])  # DELETE
def delete_book(book_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = 'DELETE FROM books WHERE id = %s'
        cursor.execute(query, (book_id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Book not found"}), 404

        return jsonify({"message": "Book deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()
    pass
