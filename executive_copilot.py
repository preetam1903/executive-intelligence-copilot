import streamlit as st
import fitz
import base64
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)
st.set_page_config(layout="wide")

st.title("Executive Intelligence Copilot")

uploaded_file = st.file_uploader(
    "Upload PDF Report",
    type=["pdf"]
)

if uploaded_file is not None:

    pdf = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    st.success(
        f"PDF Loaded Successfully - {pdf.page_count} Pages"
    )

    page_no = st.selectbox(
        "Select Page",
        range(pdf.page_count)
    )

    page = pdf.load_page(page_no)

    pix = page.get_pixmap(
        matrix=fitz.Matrix(2, 2)
    )

    img = pix.tobytes("png")

    st.image(
        img,
        caption=f"Page {page_no + 1}"
    )
    if st.button("Analyze Page"):

        base64_image = base64.b64encode(
            img
        ).decode("utf-8")

        st.success("Image Ready For Vision Analysis")

        st.write(
            f"Image Size: {len(base64_image)} characters"
        )

    

    st.subheader("Extracted Text")

    st.text(
        page.get_text()
    )
