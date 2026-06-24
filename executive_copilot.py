import streamlit as st
import fitz
import base64
from PIL import Image
import io
from openai import OpenAI
import json

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

    Return JSON ONLY.

    {
      "kpis":[
        {
          "name":"",
          "trend":"",
          "risk":"",
          "business_impact":""
        }
      ]
    }

    Rules:
    - Extract every KPI you can identify.
    - Trend must be Up, Down or Stable.
    - Risk must be Low, Medium or High.
    - business_impact should be short.
    - Return valid JSON only.
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

    if st.button("Analyze Entire Report"):
        operational_model = []
        report_summary = ""

        with st.spinner("Analyzing report..."):

            for page_num in range(pdf.page_count):

                page = pdf.load_page(page_num)

                pix = page.get_pixmap(
                    matrix=fitz.Matrix(2,2)
                )

                page_img = pix.tobytes("png")

                base64_image = base64.b64encode(
                    page_img
                ).decode("utf-8")

                response = client.chat.completions.create(
                    model="gpt-4.1",

                    messages=[
                        {
                            "role":"user",
                            "content":[

                                {
                                    "type":"text",
                                    "text":"""
    Analyze this manufacturing report page.

    Return ONLY valid JSON.

    {
  "kpis":[
    {
      "name":"",

      "weekly_values": {
        "W1":"",
        "W2":"",
        "W3":"",
        "W4":""
      },

      "target_values": {
        "W1":"",
        "W2":"",
        "W3":"",
        "W4":""
      },

      "status":"",
      "trend":"",
      "risk":"",
      "business_impact":""
    }
  ]
}

    Rules:
    - Extract KPI name.
    - Extract actual value if visible.
    - Extract target value if visible.
    - Extract status (RED/AMBER/GREEN if visible).
    - Trend = Up/Down/Stable.
    - Risk = Low/Medium/High.
    - Return JSON only.
    - No markdown.
    - No explanation.
    """
                                },

                                {
                                    "type":"image_url",
                                    "image_url":{
                                        "url":f"data:image/png;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],

                    temperature=0
                )

                page_result = response.choices[0].message.content

                try:

                    page_json = json.loads(page_result)

                    operational_model.append(
                        {
                            "page": page_num + 1,
                            "kpis": page_json.get("kpis", [])
                        }
                    )

                except Exception as e:

                    operational_model.append(
                        {
                            "page": page_num + 1,
                            "error": str(e)
                        }
                    )

                report_summary += f"\n\nPAGE {page_num+1}\n"
                report_summary += page_result

        st.session_state["report_summary"] = report_summary
        st.session_state["operational_model"] = operational_model

        st.success("Report Analysis Complete")

        st.text_area(
            "Page Analysis",
            report_summary,
            height=500
        )

        st.subheader("Operational Knowledge Model")
        st.write(operational_model)
    
    if "report_summary" in st.session_state:

        if st.button("Generate Executive Summary"):

            with st.spinner("Generating Executive Summary..."):

                summary_response = client.chat.completions.create(
                    model="gpt-4.1",

                    messages=[
                        {
                            "role": "user",
                            "content": f"""
        You are a COO advisor.

        Using the findings below:

        {st.session_state['report_summary']}

        Provide:

        1. Executive Summary
        2. Top Risks
        3. Critical Areas
        4. Watch Items
    
        Keep it concise.
        """
                        }
                    ],

                    temperature=0
                )

                st.subheader("Executive Summary")

                st.write(
                    summary_response.choices[0].message.content
                )


    
    st.subheader("Extracted Text")

    st.text(
        page.get_text()
    )
