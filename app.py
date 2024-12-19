from flask import Flask, jsonify, request  # Added 'request' import
import mysql.connector
import secrets
from functools import wraps

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='lib_db'
    )
#----------BOOKS CRUD OPERATIONS------#
@app.route('/books', methods=['POST'])#CREATE
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

        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()


@app.route('/books', methods=['GET'])#READ ALL BOOKS
def get_books():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM books')
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

@app.route('/books/<int:book_id>', methods=['GET'])#READ A SINGLE BOOK BY ID
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
@app.route('/books/name/<string:book_name>', methods=['GET'])  # READ A SINGLE BOOK BY NAME
def get_book_by_name(book_name):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        # Use the book name in the query
        query = 'SELECT * FROM books WHERE title = %s'
        cursor.execute(query, (book_name,))
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

@app.route('/books/<int:book_id>', methods=['PUT'])#UPDATE A BOOK
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


@app.route('/books/<int:book_id>', methods=['DELETE'])#DELETE A BOOK BY ID
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


# --------- MEMBERS CRUD OPERATIONS --------- #

# CREATE a new member
@app.route('/members', methods=['POST'])
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
@app.route('/members', methods=['GET'])
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
@app.route('/members/<int:member_id>', methods=['GET'])
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
@app.route('/members/<int:member_id>', methods=['PUT'])
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
@app.route('/members/<int:member_id>', methods=['DELETE'])
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

#-------SEARCH FUNCTIONALITY BY TITLE OR AUTHOR---------

@app.route('/books/search', methods=['GET'])

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

#------TOKEN GENERATION-------#
@app.route('/generate-token', methods=['POST'])
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


@app.route('/members', methods=['GET'])
@token_required
def get_members():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch all members
        query = "SELECT * FROM members"
        cursor.execute(query)
        members = cursor.fetchall()

        return jsonify(members), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()


if __name__ == '__main__':
    app.run(debug=True)
