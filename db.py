import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_DATABASE"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
)

cursor = conn.cursor()

sql_query = """CREATE TABLE books
                (id INTEGER PRIMARY KEY,
                author TEXT NOT NULL,
                language TEXT NOT NULL,
                title TEXT NOT NULL
            )"""

cursor.execute(sql_query)
conn.close()
