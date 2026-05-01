import pandas as pd
import mysql.connector

# 🔹 MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3307,
    password="Priya@123",  
    database="video_game_analysis"   
)

# 🔹 Query run करना
query = "SELECT * FROM merged_dataset"
df = pd.read_sql(query, conn)

# 🔹 Data check
print("Data Preview:")
print(df.head())

print("\nData Info:")
print(df.info())

print("\nSummary:")
print(df.describe())

# 🔹 Top 10 highest rated games
top_games = df.sort_values(by="rating", ascending=False).head(10)

print(top_games.head())

# 🔹 Correlation
print("\nCorrelation:")
print(df.corr(numeric_only=True))