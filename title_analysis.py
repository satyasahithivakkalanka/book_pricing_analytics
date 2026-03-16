import sqlite3
import pandas as pd

# Load required columns
conn = sqlite3.connect("books.db")
df = pd.read_sql_query(
    "SELECT title_length, has_positive_word, price, rating FROM books",
    conn,
)
conn.close()

# Average rating comparison
print("Average Rating based on Positive Words in Title:")
print(df.groupby("has_positive_word")["rating"].mean())

# Average price comparison
print("\nAverage Price based on Positive Words in Title:")
print(df.groupby("has_positive_word")["price"].mean())

# Correlation between title length and price
print("\nCorrelation between Title Length and Price:")
print(df["title_length"].corr(df["price"]))
