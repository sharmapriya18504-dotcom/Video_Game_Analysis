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

