import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Video Game Analysis", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("merged_dataset.csv")
    df = df.fillna(0)
    df.columns = df.columns.str.lower()
    return df

df = load_data()

# ---------------- NAVBAR ----------------
tabs = st.tabs([
    "🏠 Home",
    "📊 Dashboard",
    "📈 EDA",
    "📂 Dataset",
    "📄 Report",
    "👩 About"
])

# ---------------- HOME ----------------
with tabs[0]:
    st.markdown("""
    <h1 style='text-align:center;'>🎮 Video Game Analysis Website</h1>
    <p style='text-align:center;'>Interactive Data Analytics Platform</p>
    """, unsafe_allow_html=True)

    st.info("Explore video game trends, sales, and engagement with interactive tools.")

    col1, col2, col3 = st.columns(3)
    col1.metric("🎮 Total Games", len(df))
    col2.metric("⭐ Avg Rating", round(df['rating'].mean(),2))
    col3.metric("💰 Total Sales", round(df['global_sales'].sum(),2))

# ---------------- DASHBOARD ----------------
with tabs[1]:
    st.title("📊 Interactive Dashboard")

    # 🔥 USER FILTERS
    col1, col2, col3 = st.columns(3)

    genre = col1.selectbox("Select Genre", ["All"] + list(df['genre'].unique()))
    year = col2.selectbox("Select Year", ["All"] + list(df['year'].unique()))
    platform = col3.selectbox("Select Platform", ["All"] + list(df['platform'].unique()))

    filtered_df = df.copy()

    if genre != "All":
        filtered_df = filtered_df[filtered_df['genre'] == genre]

    if year != "All":
        filtered_df = filtered_df[filtered_df['year'] == year]

    if platform != "All":
        filtered_df = filtered_df[filtered_df['platform'] == platform]

    st.success(f"Filtered Data: {len(filtered_df)} records")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Top Genres")
        genre_sales = filtered_df.groupby("genre")["global_sales"].sum().sort_values(ascending=False).head(10)
        st.bar_chart(genre_sales)

    with col2:
        st.subheader("🌍 Regional Sales")
        region_sales = filtered_df[['na_sales','eu_sales','jp_sales']].sum()
        st.bar_chart(region_sales)

# ---------------- EDA ----------------
with tabs[2]:
    st.title("📈 EDA Analysis")

    chart_type = st.selectbox("Choose Chart", [
        "Rating vs Sales",
        "Wishlist vs Sales",
        "Year vs Sales"
    ])

    if chart_type == "Rating vs Sales":
        fig, ax = plt.subplots()
        ax.scatter(df['rating'], df['global_sales'])
        st.pyplot(fig)

    elif chart_type == "Wishlist vs Sales":
        fig, ax = plt.subplots()
        ax.scatter(df['wishlist'], df['global_sales'])
        st.pyplot(fig)

    elif chart_type == "Year vs Sales":
        if "year" in df.columns:
            year_sales = df.groupby("year")["global_sales"].sum()
            st.line_chart(year_sales)

# ---------------- DATASET ----------------
with tabs[3]:
    st.title("📂 Dataset Explorer")

    st.dataframe(df)

    st.download_button(
        "📥 Download Dataset",
        df.to_csv(index=False),
        "dataset.csv"
    )

# ---------------- REPORT ----------------
with tabs[4]:
    st.title("📄 Power BI Report")

    try:
        with open("Dashboard.pdf", "rb") as f:
            pdf_bytes = f.read()
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')

        pdf_display = f"""
        <embed src="data:application/pdf;base64,{base64_pdf}" 
        width="100%" height="700px" type="application/pdf">
        </embed>
        """

        st.markdown(pdf_display, unsafe_allow_html=True)

        st.download_button("📥 Download PDF", pdf_bytes, "Dashboard.pdf")

    except:
        st.warning("PDF not loading. Please download.")

# ---------------- ABOUT ----------------
with tabs[5]:
    st.title("👩 About Me")

    st.markdown("""
    **Priya Sharma**  
    🎓 B.Tech CSE  

    ### 💻 Skills
    - Python
    - MySQL
    - Power BI
    - Streamlit

    ### 🌐 Project
    Video Game Analysis Website
    """)
