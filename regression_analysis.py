import sqlite3
import pandas as pd
import statsmodels.api as sm

# Load data from the database
conn = sqlite3.connect("books.db")
df = pd.read_sql_query("SELECT price, rating FROM books", conn)
conn.close()

# Drop rows with missing values just in case
df = df.dropna(subset=["price", "rating"])

# X = rating, y = price
X = sm.add_constant(df["rating"])
y = df["price"]

model = sm.OLS(y, X).fit()
print(model.summary())
