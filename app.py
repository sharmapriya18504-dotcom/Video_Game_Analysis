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

    st.markdown("### 📌 Project Introduction")
    st.info("Analyze video game sales, ratings, and user engagement trends using Python, MySQL, Power BI, and Streamlit.")

    st.markdown("### 🎯 Objectives")
    st.success("""
    ✔ Analyze sales trends  
    ✔ Identify top genres & platforms  
    ✔ Study user engagement  
    ✔ Build interactive dashboards  
    """)

    st.markdown("### 🔄 Project Flow")
    st.code("Data Cleaning ➝ Merging ➝ MySQL ➝ EDA ➝ Power BI ➝ Streamlit")

    st.markdown("---")
    st.image("https://cdn-icons-png.flaticon.com/512/686/686589.png", width=120)

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

    st.subheader("⭐ Rating vs Global Sales")
    fig, ax = plt.subplots()
    ax.scatter(df['rating'], df['global_sales'])
    st.pyplot(fig)

    st.subheader("💖 Wishlist vs Sales")
    fig, ax = plt.subplots()
    ax.scatter(df['wishlist'], df['global_sales'])
    st.pyplot(fig)

    st.subheader("📅 Year vs Sales")
    if 'year' in df.columns:
        year_sales = df.groupby("year")["global_sales"].sum()
        st.line_chart(year_sales)

    st.subheader("🏢 Top Publishers")
    pub_sales = df.groupby("publisher")["global_sales"].sum().sort_values(ascending=False).head(10)
    st.bar_chart(pub_sales)

    st.markdown("### 📌 Insights")
    st.info("""
    - Higher ratings → higher sales  
    - Wishlist ↑ → Sales ↑  
    - Action & Adventure dominate  
    """)

# ---------------- DATASET ----------------
elif section == "📂 Dataset":
    st.title("📂 Dataset Exploration")

    st.write("Rows:", df.shape[0], "| Columns:", df.shape[1])

    st.subheader("📊 Column Info")
    st.write(df.dtypes)

    st.subheader("📈 Summary")
    st.write(df.describe())

    st.subheader("📄 Sample Data")
    st.dataframe(df.head(20))

    if "genre" in df.columns:
        st.subheader("🎛 Filter by Genre")
        selected = st.selectbox("Select Genre", df['genre'].dropna().unique())
        st.dataframe(df[df['genre'] == selected].head(10))

# ---------------- PDF + POWER BI ----------------
elif section == "📄 Power BI + PDF":
    st.title("📊 Power BI + PDF Dashboard")

    st.info("Below is the exported Power BI dashboard (PDF view)")

    import base64

    with open("Dashboard.pdf", "rb") as f:
        pdf_bytes = f.read()
        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')

    pdf_display = f"""
    <embed src="data:application/pdf;base64,{base64_pdf}" 
    width="100%" height="700px" type="application/pdf">
    """

    st.markdown(pdf_display, unsafe_allow_html=True)

    st.download_button(
        "📥 Download PDF",
        pdf_bytes,
        "Dashboard.pdf"
    )

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

