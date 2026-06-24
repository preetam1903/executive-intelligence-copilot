import fitz
import streamlit as st

pdf = fitz.open(
    stream=uploaded_file.read(),
    filetype="pdf"
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

st.text(page.get_text())
