import streamlit as st
import fitz  # PyMuPDF
import pandas as pd

st.set_page_config(
    page_title="Executive Intelligence Copilot",
    layout="wide"
)

st.title("📊 Executive Intelligence Copilot")

uploaded_file = st.sidebar.file_uploader(
    "Upload Monthly Report",
    type=["pdf"]
)

if uploaded_file:

    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    st.success(f"PDF Loaded Successfully - {pdf.page_count} Pages")

    extracted_pages = []

    for page_num in range(pdf.page_count):

        page = pdf.load_page(page_num)

        text = page.get_text()

        extracted_pages.append({
            "Page": page_num + 1,
            "Content": text
        })

    page_df = pd.DataFrame(extracted_pages)

    tab1, tab2 = st.tabs([
        "Report Extraction",
        "Executive Chat"
    ])

    with tab1:

        st.subheader("Extracted Pages")

        selected_page = st.selectbox(
            "Select Page",
            page_df["Page"]
        )

        page_text = page_df[
            page_df["Page"] == selected_page
        ]["Content"].iloc[0]

        st.text_area(
            "Page Content",
            page_text,
            height=500
        )

    with tab2:

        st.info(
            "Executive Chat will be enabled in Phase 2"
        )
