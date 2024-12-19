CREATE DATABASE lib_db;
USE lib_db;
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    published_year INT NOT NULL
);
CREATE TABLE members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO books (title, author, published_year) 
VALUES 
('The Great Gatsby', 'F. Scott Fitzgerald', 1925),
('Think Python','Allen B.Downey',2002),
('Learning Python','Mark Lutz & David Ascher',2013),
('Data Science From Scratch','Joel Grus',2015),
('Python For Data Analysis','Wes McKinney',2022),
('Harry Potter','JK Rowling',1997),
('1984', 'George Orwell', 1949);

INSERT INTO members (name, email) 
VALUES 
('Andie', 'andie@gmail.com'),
('Barath', 'barath14@gmail.com'),
('Raju','raju98@gmail.com'),
('Tarang','tar23@gmail.com'),
('Zakiya','zaki66@gmail.com');


SELECT user, host, plugin FROM mysql.user;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
FLUSH PRIVILEGES;

CREATE USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
GRANT ALL PRIVILEGES ON library_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;

ALTER TABLE books
ADD COLUMN genre VARCHAR(100),
ADD COLUMN quantity INT DEFAULT 0;

ALTER TABLE members
ADD COLUMN phone VARCHAR(20),
ADD COLUMN joined_date DATE;

SELECT * FROM members;
SELECT * FROM books;

UPDATE books
SET genre = 'Novel', quantity = 5
WHERE id = 1;

UPDATE books
SET genre = 'Programming', quantity = 3
WHERE id = 2;

UPDATE books
SET genre = 'Programming', quantity = 3
WHERE id = 3;

UPDATE books
SET genre = 'Data Science', quantity = 4
WHERE id = 4;

UPDATE books
SET genre = 'Programming', quantity = 2
WHERE id = 5;

UPDATE books
SET genre = 'Fantasy', quantity = 7
WHERE id = 6;

UPDATE books
SET genre = 'Dystopian', quantity = 5
WHERE id = 7;

UPDATE members
SET phone = '9874567890', joined_date = '2023-01-01'
WHERE id = 1;

UPDATE members
SET phone = '9845678901', joined_date = '2023-02-15'
WHERE id = 2;

UPDATE members
SET phone = '8756789012', joined_date = '2023-03-10'
WHERE id = 3;

UPDATE members
SET phone = '9765435633', joined_date = '2023-04-25'
WHERE id = 4;

UPDATE members
SET phone = '9675464328', joined_date = '2023-05-30'
WHERE id = 5;

SELECT * FROM books;
SELECT * FROM members;

SELECT COUNT(*) FROM books;
SELECT * FROM books LIMIT 3 OFFSET 6;

CREATE TABLE tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    token VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(id)
);



