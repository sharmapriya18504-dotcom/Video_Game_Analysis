import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Video Game Analysis", layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🎮 Navigation")
section = st.sidebar.radio("Go To", [
    "🏠 Home",
    "📊 Dashboard",
    "📈 EDA Analysis",
    "📂 Dataset",
    "📄 Power BI + PDF",
    "👩‍💻 About Me"
])

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("merged_dataset.csv")
    df.columns = df.columns.str.lower()
    return df

df = load_data()

# ---------------- HOME ----------------
if section == "🏠 Home":
    st.title("🎮 Video Game Analysis Dashboard")

    st.markdown("## 📌 Project Introduction")
    st.write("""
    This project analyzes video game sales and engagement data to understand trends,
    user behavior, and platform performance. It combines multiple datasets and uses
    Python, MySQL, Power BI, and Streamlit for complete analysis.
    """)

    st.markdown("## 🎯 Objectives")
    st.markdown("""
    - Analyze global and regional sales trends  
    - Identify top-performing genres and platforms  
    - Study user engagement (ratings, wishlist, plays)  
    - Build interactive dashboards for insights  
    """)

    st.markdown("## 🔄 Project Flow")
    st.write("""
    Data Cleaning ➝ Data Merging ➝ MySQL Storage ➝ EDA ➝ Power BI ➝ Streamlit Dashboard
    """)

# ---------------- DASHBOARD ----------------
elif section == "📊 Dashboard":
    st.title("📊 Key Insights Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("🎮 Total Games", len(df))
    col2.metric("⭐ Avg Rating", round(df['rating'].mean(), 2))
    col3.metric("💰 Total Sales", round(df['global_sales'].sum(), 2))

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Top Genres by Sales")
        genre_sales = df.groupby("genre")["global_sales"].sum().sort_values(ascending=False).head(10)
        st.bar_chart(genre_sales)

    with col2:
        st.subheader("🌍 Regional Sales")
        region_sales = df[['na_sales','eu_sales','jp_sales']].sum()
        st.bar_chart(region_sales)

# ---------------- EDA ----------------
elif section == "📈 EDA Analysis":
    st.title("📈 Exploratory Data Analysis")

    # Rating vs Sales
    st.subheader("⭐ Rating vs Global Sales")
    fig, ax = plt.subplots()
    ax.scatter(df['rating'], df['global_sales'])
    ax.set_xlabel("Rating")
    ax.set_ylabel("Global Sales")
    st.pyplot(fig)

    # Wishlist vs Sales
    st.subheader("💖 Wishlist vs Sales")
    fig, ax = plt.subplots()
    ax.scatter(df['wishlist'], df['global_sales'])
    ax.set_xlabel("Wishlist")
    ax.set_ylabel("Global Sales")
    st.pyplot(fig)

    # Year vs Sales
    st.subheader("📅 Year vs Global Sales")
    if 'year' in df.columns:
        year_sales = df.groupby("year")["global_sales"].sum()
        st.line_chart(year_sales)

    # Top Publishers
    st.subheader("🏢 Top Publishers")
    pub_sales = df.groupby("publisher")["global_sales"].sum().sort_values(ascending=False).head(10)
    st.bar_chart(pub_sales)

    # Insights
    st.markdown("### 📌 Insights")
    st.write("""
    - Higher ratings generally lead to higher sales  
    - Wishlist is positively correlated with sales  
    - Certain genres dominate global market  
    """)

# ---------------- DATASET ----------------
elif section == "📂 Dataset":
    st.title("📂 Dataset Exploration")

    st.subheader("🔍 Dataset Overview")
    st.write("Rows:", df.shape[0], "Columns:", df.shape[1])

    st.subheader("📊 Column Info")
    st.write(df.dtypes)

    st.subheader("📈 Statistical Summary")
    st.write(df.describe())

    st.subheader("📄 Sample Data")
    st.dataframe(df.head(20))

    # Filter option
    st.subheader("🎛 Filter by Genre")
    if "genre" in df.columns:
        selected_genre = st.selectbox("Select Genre", df['genre'].dropna().unique())
        filtered_df = df[df['genre'] == selected_genre]
        st.dataframe(filtered_df.head(10))

# ---------------- PDF ----------------
elif section == "📄 Power BI + PDF":
    st.title("📄 Dashboard PDF View")

    def display_pdf(file):
        with open(file, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        pdf_display = f"""
        <iframe src="data:application/pdf;base64,{base64_pdf}" 
        width="100%" height="700"></iframe>
        """

        st.markdown(pdf_display, unsafe_allow_html=True)

    display_pdf("Dashboard.pdf")

    with open("Dashboard.pdf", "rb") as f:
        st.download_button("📥 Download PDF", f, "Dashboard.pdf")

# ---------------- ABOUT ----------------
elif section == "👩‍💻 About Me":
    st.title("👩‍💻 About Me")

    st.markdown("""
    ### 👩 Priya Sharma  
    🎓 B.Tech CSE (6th Semester)

    ### 💻 Skills:
    - Python (Pandas, Matplotlib)
    - MySQL
    - Power BI
    - Streamlit

    ### 📊 Project:
    Video Game Analysis Dashboard
    """)

# ---------------- FOOTER ----------------
st.sidebar.success("🚀 Developed by Priya Sharma")
