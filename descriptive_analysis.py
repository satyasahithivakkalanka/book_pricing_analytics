import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load data from database
conn = sqlite3.connect("books.db")
df = pd.read_sql_query("SELECT * FROM books", conn)
conn.close()

print("SUMMARY STATISTICS:")
print(df.describe())

# 2. Price distribution
plt.figure()
plt.hist(df["price"], bins=20)
plt.title("Price Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.show()

# 3. Rating distribution
plt.figure()
sns.countplot(x="rating", data=df)
plt.title("Rating Distribution")
plt.xlabel("Rating (1–5)")
plt.ylabel("Count")
plt.show()

# 4. Category-wise average price (top 10)
category_avg = (
    df.groupby("category")["price"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)
print("\nTOP 10 CATEGORIES BY AVERAGE PRICE:")
print(category_avg)
