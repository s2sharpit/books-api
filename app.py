from flask import Flask, request, jsonify
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_DATABASE"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
    except pymysql.Error as e:
        print(e)
    return conn


@app.route("/books", methods=["GET", "POST"])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("SELECT * FROM books")
        books = [
            dict(
                id=row["id"],
                author=row["author"],
                language=row["language"],
                title=row["title"],
            )
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)

    if request.method == "POST":
        new_author = request.form["author"]
        new_lang = request.form["language"]
        new_title = request.form["title"]
        sql = """INSERT INTO books (author, language, title) 
                 VALUES(%s, %s, %s)"""

        cursor.execute(sql, (new_author, new_lang, new_title))
        conn.commit()

        return f"Book with the id: {cursor.lastrowid} created successfully", 201


@app.route("/book/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM books WHERE id=%s", (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book), 200
        else:
            return "Something went wrong", 404

    if request.method == "PUT":
        sql = """UPDATE books
                SET title=%s,
                    author=%s,
                    language=%s
                WHERE id=%s"""
        author = request.form["author"]
        lang = request.form["language"]
        title = request.form["title"]
        updated_book = {"id": id, "author": author, "language": lang, "title": title}
        cursor.execute(sql, (title, author, lang, id))
        conn.commit()
        return jsonify(updated_book), 200

    if request.method == "DELETE":
        sql = """DELETE FROM books WHERE id=%s"""
        cursor.execute(sql, (id,))
        conn.commit()
        return "The book with id: {} has been deleted.".format(id), 200