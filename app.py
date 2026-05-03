import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Video Game Analysis", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #1f4037, #99f2c8);
}
h1, h2, h3 {
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("merged_dataset.csv")
    df = df.fillna(0)
    df.columns = df.columns.str.lower()
    return df

df = load_data()

# ---------------- NAV ----------------
tabs = st.tabs([
    "🏠 Home",
    "📊 Dashboard",
    "📈 EDA",
    "📂 Dataset",
    "📄 Power BI",
    "👩 About"
])

# ---------------- HOME ----------------
with tabs[0]:
    st.title("🎮 Video Game Analysis Dashboard")

    st.info("Interactive dashboard to explore video game trends, sales & engagement 🚀")

    col1, col2, col3 = st.columns(3)
    col1.metric("🎮 Total Games", len(df))
    col2.metric("⭐ Avg Rating", round(df['rating'].mean(),2))
    col3.metric("💰 Total Sales", round(df['global_sales'].sum(),2))

# ---------------- DASHBOARD ----------------
with tabs[1]:
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
with tabs[2]:
    st.title("📈 EDA Analysis")

    fig, ax = plt.subplots()
    ax.scatter(df['rating'], df['global_sales'])
    ax.set_title("Rating vs Global Sales")
    st.pyplot(fig)

# ---------------- DATASET ----------------
with tabs[3]:
    st.title("📂 Dataset")

    st.dataframe(df.head(50))

# ---------------- POWER BI ----------------
with tabs[4]:
    st.title("📄 Power BI Report Section")

    st.success("📥 Download Full Power BI Dashboard Below")

    # Download button
    with open("Dashboard.pdf", "rb") as f:
        st.download_button("📥 Download Dashboard PDF", f, "Dashboard.pdf")

    st.divider()

    st.subheader("📊 Sample Insights (Power BI Style)")

    col1, col2 = st.columns(2)

    with col1:
        st.write("📈 Sales Trend by Year")
        if "year" in df.columns:
            year_sales = df.groupby("year")["global_sales"].sum()
            st.line_chart(year_sales)

    with col2:
        st.write("🏆 Top Publishers")
        pub = df.groupby("publisher")["global_sales"].sum().sort_values(ascending=False).head(10)
        st.bar_chart(pub)

# ---------------- ABOUT ----------------
with tabs[5]:
    st.title("👩 About Me")

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
