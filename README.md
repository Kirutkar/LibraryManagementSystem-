# LibraryManagementSystem-
Building a Flask API for a "Library Management System" that allows CRUD operations for books and members.

**Library Management System with Flask**
This project implements a Library Management System using Flask and MySQL. The system allows CRUD (Create, Read, Update, Delete) operations for books and members, with token-based authentication for accessing protected routes like fetching member details. The application also features search functionality to search for books by title or author.

**Features**
*Token-Based Authentication: Secure API access via tokens.
*CRUD Operations: Manage books and members through API endpoints.
*Search Functionality: Search for books by title or author.
*MySQL Database: Uses MySQL for data storage.

**Project Structure**

/project-directory
   
    ├── main.py              # Main Flask application
    ├── /routes
    │   ├── books.py        # Books related routes
    │   ├── members.py      # Members related routes
    │   └── search.py       # Search related routes
    ├── /auth.py            # Token generation and validation logic
    ├── /lms_db
    │   └── lms_db.sql      # SQL script to set up MySQL database
    ├── /requirements.txt   # Python dependencies
    └── /README.md          # Project description and setup guide

**Setup Instructions**

1. Install Dependencies
First, install the required Python packages listed in the requirements.txt file. Run the following command:
pip install -r requirements.txt

2. Set Up MySQL Database
a. Install MySQL
If you don’t have MySQL installed on your machine, download and install it from the official MySQL website.
b. Create the Database and Tables
Once MySQL is installed, you can create the database and tables using the SQL scripts provided in the lms_db folder. Here’s how to do it:
Open MySQL and create a new database:

CREATE DATABASE library_system;
Use the library_system database:
USE library_system;
Run the SQL script to create the tables and insert sample data. This script is located in the lms_db/lms_db.sql file:
source /path/to/lms_db/lms_db.sql
This will create the necessary tables for members, books, and tokens, and insert some sample data for testing.

c. Update Connection Details
In your app.py file, make sure the MySQL connection details are correctly configured:

import mysql.connector

def get_connection():

    return mysql.connector.connect(
    
        host="localhost",  # Your MySQL host (use localhost if running locally)
        user="root",       # Your MySQL username
        password="password",  # Your MySQL password
        database="library_system"  # The database you've created
    )
    
Update these details if necessary based on your local MySQL installation.

**Functionality Overview**
1. Token-Based Authentication

The system uses token-based authentication to access certain endpoints. Here's how it works:
a. Generate Token
To generate a token for a user, send a POST request to /generate-token with the user’s email. The server will generate a token if the email exists in the database.
Request:

POST /generate-token
{

  "email": "john@example.com"
  
}

Response:

{

  "token": "generated_token_here"
  
}

b. Token Validation

Once the token is generated, use it to make authenticated requests. Add the token in the Authorization header to access protected routes.

For example, to get all members, make a GET request to /members with the following header:

Header:

Authorization: generated_token_here
If the token is valid, the system will return the list of members.

2. CRUD Operations

a. Create Member

To add a new member, send a POST request to /members with the member details.

Request:

POST /members

{

  "name": "John Smith",
  
  "email": "johnsmith@example.com"
  
}

b. Create Book

To add a new book, send a POST request to /books with the book details.

Request:

POST /books

{

  "title": "Advanced Flask",
  
  "author": "John Doe",
  
  "year": 2024
  
}

c. Get All Books

To get all books, send a GET request to /books.

Request:

GET /books

d. Update Book

To update an existing book, send a PUT request to /books/{id} with the updated book details.

Request:

PUT /books/1

{

  "title": "Flask Mastery",
  
  "author": "Jane Doe",
  
  "year": 2025
  
}

e. Delete Book

To delete a book, send a DELETE request to /books/{id}.

Request:

DELETE /books/1

3. Search Functionality
   
You can search for books by title or author using the /search endpoint. Add the query parameters title or author to filter the results.

Request:

GET /search?title=Flask


**Running the Application**


1. Start MySQL Service
   
Ensure that your MySQL service is running on your local machine.


3. Run Flask App
   
Run the Flask application using the following command:

python main.py

By default, the application will be hosted on http://localhost:5000.


5. Test the API Endpoints
 
You can test the API endpoints using Postman or any API client. The following steps explain how to use Postman to test the endpoints:

a. Generate Token

Open Postman and make a POST request to http://localhost:5000/generate-token.

Add the request body with the email of a member, such as:

{

  "email": "andie@gmail.com"
  
}

b. Use Token for Authenticated Routes

Once you receive the token, make a GET request to http://localhost:5000/members.

In the Authorization tab in Postman, add a header:

Key: Authorization

Value: Bearer {your_token_here}


**Conclusion**

This Library Management System provides a simple yet effective way to manage books and members, leveraging token-based authentication to secure access to member data. By using Flask for the backend and MySQL for data storage, this project provides a real-world application of a full-stack development approach.







