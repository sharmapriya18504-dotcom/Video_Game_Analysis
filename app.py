import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Video Game Analysis", layout="wide")

# ---------------- DARK UI ----------------
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
}

.block-container {
    background-color: #111827;
    padding: 2rem;
    border-radius: 15px;
}

h1, h2, h3 {
    color: #e5e7eb;
}

p, span, label {
    color: #d1d5db !important;
}

section[data-testid="stSidebar"] {
    background-color: #020617;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🎮 Navigation")
section = st.sidebar.radio("Go To", [
    "🏠 Home",
    "📊 Dashboard",
    "📈 EDA Analysis",
    "📂 Dataset",
    "📄 Power BI",
    "👩‍💻 About"
])

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("merged_dataset.csv")
    df = df.fillna(0)
    df.columns = df.columns.str.lower()
    return df

df = load_data()

# ---------------- HOME ----------------
if section == "🏠 Home":
    st.title("🎮 Video Game Analysis Dashboard")

    st.markdown("## 📌 Project Introduction")
    st.write("""
    This project analyzes video game sales, ratings, and engagement data.
    It combines multiple datasets and provides insights using Python,
    MySQL, Power BI, and Streamlit.
    """)

    st.markdown("## 🎯 Objectives")
    st.markdown("""
    - Analyze global and regional sales trends  
    - Identify top genres and publishers  
    - Study rating vs sales relationship  
    - Understand user engagement  
    """)

    st.markdown("## 🔄 Workflow")
    st.info("Cleaning → Merging → SQL → EDA → Power BI → Streamlit")

    col1, col2, col3 = st.columns(3)
    col1.metric("🎮 Total Games", len(df))
    col2.metric("⭐ Avg Rating", round(df['rating'].mean(),2))
    col3.metric("💰 Total Sales", round(df['global_sales'].sum(),2))

# ---------------- DASHBOARD ----------------
elif section == "📊 Dashboard":
    st.title("📊 Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Top Genres")
        genre_sales = df.groupby("genre")["global_sales"].sum().sort_values(ascending=False).head(10)
        st.bar_chart(genre_sales)

    with col2:
        st.subheader("🌍 Regional Sales")
        region_sales = df[['na_sales','eu_sales','jp_sales']].sum()
        st.bar_chart(region_sales)

# ---------------- EDA ----------------
elif section == "📈 EDA Analysis":
    st.title("📈 EDA Analysis")

    analysis_type = st.selectbox(
        "Select Analysis",
        ["Rating vs Sales", "Wishlist vs Sales", "Year vs Sales"]
    )

    if analysis_type == "Rating vs Sales":
        fig, ax = plt.subplots()
        ax.scatter(df['rating'], df['global_sales'])
        ax.set_facecolor("#111827")
        fig.patch.set_facecolor("#111827")
        st.pyplot(fig)

    elif analysis_type == "Wishlist vs Sales":
        fig, ax = plt.subplots()
        ax.scatter(df['wishlist'], df['global_sales'])
        ax.set_facecolor("#111827")
        fig.patch.set_facecolor("#111827")
        st.pyplot(fig)

    elif analysis_type == "Year vs Sales":
        if "year" in df.columns:
            year_sales = df.groupby("year")["global_sales"].sum()
            st.line_chart(year_sales)

# ---------------- DATASET ----------------
elif section == "📂 Dataset":
    st.title("📂 Dataset Explorer")

    st.write("Shape:", df.shape)

    # 🔍 Search box
    search = st.text_input("🔍 Search Game Name")

    # 🎛 Filters
    col1, col2 = st.columns(2)

    with col1:
        if "genre" in df.columns:
            genre = st.selectbox("Select Genre", ["All"] + list(df['genre'].dropna().unique()))
        else:
            genre = "All"

    with col2:
        if "year" in df.columns:
            year = st.selectbox("Select Year", ["All"] + sorted(df['year'].dropna().unique().tolist()))
        else:
            year = "All"

    # 🔝 Top N selector
    top_n = st.slider("Select Top N Rows", 5, 100, 20)

    # Apply filters
    filtered_df = df.copy()

    if search:
        filtered_df = filtered_df[filtered_df['name'].str.lower().str.contains(search.lower())]

    if genre != "All":
        filtered_df = filtered_df[filtered_df['genre'] == genre]

    if year != "All":
        filtered_df = filtered_df[filtered_df['year'] == year]

    st.subheader("📄 Filtered Data")
    st.dataframe(filtered_df.head(top_n))

    # Download
    st.download_button(
        "📥 Download Filtered Data",
        filtered_df.to_csv(index=False),
        "filtered_data.csv",
        mime="text/csv"
    )

# ---------------- POWER BI ----------------
elif section == "📄 Power BI":
    st.title("📄 Power BI Dashboard")

    st.success("📥 Download Full Dashboard")

    with open("Dashboard.pdf", "rb") as f:
        st.download_button("Download PDF", f, "Dashboard.pdf")

    st.divider()

    st.subheader("📊 Sample Insights")

    col1, col2 = st.columns(2)

    with col1:
        if "year" in df.columns:
            year_sales = df.groupby("year")["global_sales"].sum()
            st.line_chart(year_sales)

    with col2:
        pub = df.groupby("publisher")["global_sales"].sum().sort_values(ascending=False).head(10)
        st.bar_chart(pub)

# ---------------- ABOUT ----------------
elif section == "👩‍💻 About":
    st.title("👩‍💻 About Me")

    st.markdown("""
    **Priya Sharma**  
    🎓 B.Tech CSE  

    💻 Skills:
    - Python
    - MySQL
    - Power BI
    - Streamlit  
    """)

# ---------------- FOOTER ----------------
st.sidebar.success("🚀 Developed by Priya Sharma")
