import streamlit as st
import fitz

from chart_detector import ChartDetector
from header_agent import HeaderAgent
from plot_analyzer import PlotAnalyzer
from bar_extractor import BarExtractor

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

st.subheader("First Chart Detected")

st.json(chart)


# --------------------------------------------------
# CROP CHART
# --------------------------------------------------

chart_image = detector.crop_chart(
    page_image,
    chart["bbox"]
)

st.divider()

st.subheader("Chart Crop")

st.image(
    chart_image,
    width="stretch"
)
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

st.subheader("Chart Keys")
st.write(chart.keys())
label_count = len(
    chart["x_axis"]["labels"]
)

centers = plot_analyzer.compute_expected_bar_positions(
    plot,
    label_count
)

st.divider()

st.subheader("Expected Bar Centers")

st.write(centers)

st.write("Total Bars :", len(centers))
st.success("Milestone 3 Complete")
