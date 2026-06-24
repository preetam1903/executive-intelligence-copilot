import streamlit as st
import fitz
import base64
from PIL import Image
import io
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
    if st.button("Segment Page"):

        image = Image.open(
            io.BytesIO(img)
        )

        st.write(
            f"Image Size: {image.width} x {image.height}"
        )

        cols = 4
        rows = 4

        segment_width = image.width // cols
        segment_height = image.height // rows

        st.subheader("Page Segments")

        segment_no = 1

        for row in range(rows):

            display_cols = st.columns(cols)

            for col in range(cols):

                left = col * segment_width
                top = row * segment_height

                right = left + segment_width
                bottom = top + segment_height

                segment = image.crop(
                    (left, top, right, bottom)
                )

                with display_cols[col]:

                    st.write(
                        f"Segment {segment_no}"
                    )

                    st.image(segment)

                segment_no += 1


        


    
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

    Identify every KPI, chart or metric.

    For each one provide:

    - KPI Name
    - Trend (Increasing/Decreasing/Stable)
    - Business Impact
    - Risk Level (Low/Medium/High)

    At the end provide:

    Most Critical KPI:
    Reason:

    Return concise bullet points.
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
