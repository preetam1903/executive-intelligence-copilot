import streamlit as st
import fitz

from chart_detector import ChartDetector
from header_agent import HeaderAgent
from plot_analyzer import PlotAnalyzer
from bar_extractor import BarExtractor
from xaxis_agent import XAxisAgent
from stack_value_extractor import StackValueExtractor

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Executive Intelligence Copilot",
    layout="wide"
)

st.title("Executive Intelligence Copilot")


# --------------------------------------------------
# API KEY
# --------------------------------------------------

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]


# --------------------------------------------------
# UPLOAD PDF
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Executive Report",
    type=["pdf"]
)


if uploaded_file is None:
    st.stop()


# --------------------------------------------------
# PREVIEW PDF
# --------------------------------------------------

try:

    pdf = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

except Exception as e:

    st.error(str(e))
    st.stop()


left, right = st.columns([4,1])

with left:

    page = pdf.load_page(0)

    pix = page.get_pixmap(
        matrix=fitz.Matrix(2,2)
    )

    st.image(
        pix.tobytes("png"),
        width="stretch"
    )

with right:

    st.metric(
        "Pages",
        pdf.page_count
    )

    st.metric(
        "File",
        uploaded_file.name
    )

pdf.close()
uploaded_file.seek(0)


# --------------------------------------------------
# BUILD BUTTON
# --------------------------------------------------

if not st.button(
    "Start Extraction",
    width="stretch"
):
    st.stop()


# --------------------------------------------------
# INITIALIZE
# --------------------------------------------------

with st.spinner("Loading PDF..."):

    detector = ChartDetector()

    header_agent = HeaderAgent(
        OPENAI_API_KEY
    )
    xaxis_agent = XAxisAgent(
        OPENAI_API_KEY
    )

    pages = detector.convert_pdf_to_images(
        uploaded_file
    )

uploaded_file.seek(0)


# --------------------------------------------------
# FIRST PAGE ONLY
# --------------------------------------------------

page_image = pages[0]

st.divider()

st.subheader("Page 1 Loaded")

st.image(
    page_image,
    width="stretch"
)


# --------------------------------------------------
# HEADER DETECTION
# --------------------------------------------------

with st.spinner("Detecting charts..."):

    headers_json = header_agent.detect_headers(
        page_image
    )


import json

try:

    charts = json.loads(headers_json)

except Exception:

    st.error("Header Agent returned invalid JSON")

    st.code(headers_json)

    st.stop()


if len(charts) == 0:

    st.error("No charts detected.")

    st.stop()


# --------------------------------------------------
# FIRST CHART ONLY
# --------------------------------------------------

chart = charts[0]

st.divider()


# --------------------------------------------------
# CROP CHART
# --------------------------------------------------

chart_image = detector.crop_chart(
    page_image,
    chart["bbox"]
)
metadata = {

    "plot_area": {

        "left": 68,
        "right": 379,
        "top": 105,
        "bottom": 311

    },

    "bars": 27

}

extractor = StackValueExtractor(
    metadata
)
st.divider()

st.subheader("Chart Crop")

st.image(
    chart_image,
    width="stretch"
)

st.divider()

st.subheader("X Axis Labels")

xaxis = xaxis_agent.extract_labels(
    chart_image
)

st.json(xaxis)
# --------------------------------------------------
# PLOT ANALYZER
# --------------------------------------------------



plot_analyzer = PlotAnalyzer()

plot = plot_analyzer.analyze(chart_image)

st.divider()
st.subheader("Detected Plot")
st.json(plot)

# --------------------------------------------------
# BAR DETECTION
# --------------------------------------------------



bar_extractor = BarExtractor()

bars = bar_extractor.detect_bars(chart_image)

st.divider()

st.subheader("Detected Bars")

st.json(bars)

# --------------------------------------------------
# EXPECTED BAR CENTERS
# --------------------------------------------------




debug_image = extractor.draw_sampling_lines(
    chart_image
)
centers = extractor.compute_bar_centers()

sample = extractor.sample_bar(
    chart_image,
    centers[0]
)
classified = extractor.classify_bar(
    sample
)

st.divider()

st.subheader("Sampling Lines")

st.image(
    debug_image,
    width="stretch"
)
st.divider()


st.subheader("Bar 1 Classification")

st.write("Center X :", centers[0])

for i in range(0, len(classified), 10):

    st.write(
        f"Row {i} : {classified[i]}"
    )

st.success("Milestone 3 Complete")
