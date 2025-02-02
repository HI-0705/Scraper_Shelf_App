import sqlite3


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table(conn):
    try:
        sql_create_books_table = """ CREATE TABLE IF NOT EXISTS books (
                                        id integer PRIMARY KEY,
                                        title text NOT NULL,
                                        price text NOT NULL,
                                        rating text NOT NULL,
                                        category text NOT NULL
                                    ); """
        c = conn.cursor()
        c.execute(sql_create_books_table)
    except sqlite3.Error as e:
        print(e)


def insert_book(conn, book):
    sql = """ INSERT INTO books(title, price, rating, category)
              VALUES(?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, book)
    conn.commit()
    return cur.lastrowid
