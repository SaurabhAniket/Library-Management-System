import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                    book_id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    genre TEXT NOT NULL,
                    available_copies INTEGER NOT NULL
                    )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                    member_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    role TEXT NOT NULL
                    )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY,
                    book_id INTEGER,
                    member_id INTEGER,
                    member_role TEXT,
                    action TEXT,
                    FOREIGN KEY (book_id) REFERENCES books (book_id),
                    FOREIGN KEY (member_id) REFERENCES members (member_id)
                    )''')

conn.commit()

def add_book(book_id, title, author, genre, available_copies):
    cursor.execute('''INSERT INTO books (book_id, title, author, genre, available_copies) VALUES (?, ?, ?, ?, ?)''',
                   (book_id, title, author, genre, available_copies))
    conn.commit()

def borrow_book(book_id, member_id, member_role):
    cursor.execute('''SELECT available_copies FROM books WHERE book_id = ?''', (book_id,))
    available_copies = cursor.fetchone()[0]
    if available_copies > 0:
        cursor.execute('''UPDATE books SET available_copies = ? WHERE book_id = ?''', (available_copies - 1, book_id))
        cursor.execute('''INSERT INTO transactions (book_id, member_id, member_role, action) VALUES (?, ?, ?, ?)''',
                       (book_id, member_id, member_role, 'Borrow'))
        conn.commit()
        return True
    else:
        return False

def return_book(book_id, member_id, member_role):
    cursor.execute('''SELECT available_copies FROM books WHERE book_id = ?''', (book_id,))
    available_copies = cursor.fetchone()[0]
    cursor.execute('''UPDATE books SET available_copies = ? WHERE book_id = ?''', (available_copies + 1, book_id))
    cursor.execute('''INSERT INTO transactions (book_id, member_id, member_role, action) VALUES (?, ?, ?, ?)''',
                   (book_id, member_id, member_role, 'Return'))
    conn.commit()

def get_available_books():
    cursor.execute('''SELECT * FROM books WHERE available_copies > 0''')
    books = cursor.fetchall()
    return books

def close_connection():
    conn.close()
