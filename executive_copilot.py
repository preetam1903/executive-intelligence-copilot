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

        with st.spinner("Analyzing page..."):

            response = client.chat.completions.create(
                model="gpt-4.1",

                messages=[
                    {
                        "role": "user",
                        "content": [

                            {
                                "type": "text",
                                "text": """
    Analyze this manufacturing report page.

    Extract:

    1. Page title
    2. Chart titles
    3. KPI names
    4. Trend direction

    Return a concise summary.
    """
                            },

                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }

                        ]
                    }
                ],

                temperature=0
            )

            result = response.choices[0].message.content

            st.subheader("Vision Analysis")

            st.write(result)

    

    st.subheader("Extracted Text")

    st.text(
        page.get_text()
    )
