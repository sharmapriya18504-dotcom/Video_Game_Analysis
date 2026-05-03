import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Video Game Analysis", layout="wide")

# ---------------- LIGHT THEME STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #e3f2fd, #ffffff);
}

h1, h2, h3 {
    color: #0d47a1;
}

.css-1d391kg {
    background-color: #ffffff !important;
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
    This project analyzes video game data including sales, ratings, and user engagement.
    It combines multiple datasets and provides meaningful insights using Python,
    MySQL, Power BI, and Streamlit.
    """)

    st.markdown("## 🎯 Project Objectives")
    st.markdown("""
    - Analyze global and regional sales trends  
    - Identify top-performing genres and publishers  
    - Study relationship between ratings and sales  
    - Understand user engagement (wishlist, plays)  
    - Build interactive dashboards for better insights  
    """)

    st.markdown("## 🔄 Project Workflow")
    st.info("""
    Data Cleaning ➝ Data Merging ➝ MySQL ➝ EDA ➝ Power BI ➝ Streamlit Dashboard
    """)

    # Quick stats
    col1, col2, col3 = st.columns(3)
    col1.metric("🎮 Total Games", len(df))
    col2.metric("⭐ Avg Rating", round(df['rating'].mean(),2))
    col3.metric("💰 Total Sales", round(df['global_sales'].sum(),2))


# ---------------- DASHBOARD ----------------
elif section == "📊 Dashboard":
    st.title("📊 Key Insights Dashboard")

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

    st.subheader("⭐ Rating vs Global Sales")
    fig, ax = plt.subplots()
    ax.scatter(df['rating'], df['global_sales'])
    st.pyplot(fig)

    st.subheader("💖 Wishlist vs Sales")
    fig, ax = plt.subplots()
    ax.scatter(df['wishlist'], df['global_sales'])
    st.pyplot(fig)


# ---------------- DATASET ----------------
elif section == "📂 Dataset":
    st.title("📂 Dataset Overview")

    st.write("Shape:", df.shape)
    st.dataframe(df.head(20))


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

    🚀 Project:
    Video Game Analysis Dashboard
    """)

# ---------------- FOOTER ----------------
st.sidebar.success("🚀 Developed by Priya Sharma")
