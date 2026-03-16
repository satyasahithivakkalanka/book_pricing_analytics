import sqlite3
import pandas as pd

conn = sqlite3.connect("books.db")
df = pd.read_sql_query("SELECT * FROM books LIMIT 10;", conn)
conn.close()

print(df)
print("Total rows:", len(df))
