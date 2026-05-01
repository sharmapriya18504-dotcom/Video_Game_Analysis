import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("merged_dataset.csv")

df.columns = df.columns.str.lower()

# -----------------------------
# Rating vs Sales
# -----------------------------
plt.figure()
plt.scatter(df['rating'], df['global_sales'])
plt.title("Rating vs Global Sales")
plt.xlabel("rating")
plt.ylabel("global sales")
plt.savefig("rating_vs_sales.png")
plt.close()

# -----------------------------
# Wishlist vs Sales
# -----------------------------
plt.figure()
plt.scatter(df['wishlist'], df['global_sales'])
plt.title("Wishlist vs Global Sales")
plt.xlabel("wishlist")
plt.ylabel("global sales")
plt.savefig("wishlist_vs_sales.png")
plt.close()

# -----------------------------
# Year vs Sales
# -----------------------------
if 'year' in df.columns:
    plt.figure()
    df.groupby('year')['global_sales'].sum().plot()
    plt.title("Year vs Sales")
    plt.savefig("year_vs_sales.png")
    plt.close()

# -----------------------------
# Genre Fix (important)
# -----------------------------
genre_col = 'genre' if 'genre' in df.columns else 'genres'

# -----------------------------
# Genre vs Sales
# -----------------------------
plt.figure()
df.groupby(genre_col)['global_sales'].sum().sort_values(ascending=False).head(10).plot(kind='bar')
plt.title("Top Genres by Sales")
plt.savefig("genre_sales.png")
plt.close()

print("EDA Completed Successfully")