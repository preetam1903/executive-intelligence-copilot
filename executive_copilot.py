import streamlit as st
import fitz

from knowledge_repository import RepositoryManager
from executive_agent import ExecutiveAgent
from chart_detector import ChartDetector
from header_agent import HeaderAgent
from chart_analysis_agent import ChartAnalysisAgent
#from plot_detector import PlotDetector
from bar_extractor import BarExtractor
from plot_analyzer import PlotAnalyzer
# ----------------------------------------------------
# Streamlit
# ----------------------------------------------------

st.set_page_config(

    page_title="Executive Intelligence Copilot",

    layout="wide"

)

st.title("Executive Intelligence Copilot")


# ----------------------------------------------------
# Repository
# ----------------------------------------------------

if "repository" not in st.session_state:

    repository = RepositoryManager()

    repository.initialize_database()

    st.session_state["repository"] = repository


# ----------------------------------------------------
# Executive Agent
# ----------------------------------------------------

if "agent" not in st.session_state:

    st.session_state["agent"] = ExecutiveAgent(

        st.secrets["OPENAI_API_KEY"],

        st.session_state["repository"]

    )

agent = st.session_state["agent"]


# ----------------------------------------------------
# Session
# ----------------------------------------------------

if "analysis_complete" not in st.session_state:

    st.session_state["analysis_complete"] = False


# ----------------------------------------------------
# Upload
# ----------------------------------------------------

uploaded_file = st.file_uploader(

    "Upload Executive Report",

    type=["pdf"]

)


# ----------------------------------------------------
# Preview
# ----------------------------------------------------

if uploaded_file is not None:

    try:

        pdf = fitz.open(

            stream=uploaded_file.read(),

            filetype="pdf"

        )

        st.write("PDF opened successfully")

        st.write("Pages:", pdf.page_count)

    except Exception as e:

        st.error(str(e))

        st.stop()

    left, right = st.columns([3, 1])

    with left:

        if pdf.page_count > 0:

            st.write("Page Count:", pdf.page_count)
            st.write("Type:", type(pdf.page_count))

            page_number = st.number_input(

                "Page",

                min_value=1,

                max_value=pdf.page_count,

                value=1,

                step=1

            )

            page = pdf.load_page(int(page_number) - 1)

            pix = page.get_pixmap(

                matrix=fitz.Matrix(2, 2)

            )

            st.image(

                pix.tobytes("png"),

                use_container_width=True

            )

        else:

            st.error(

                "This PDF contains no pages or could not be read."

            )

    with right:

        st.metric(

            "Pages",

            pdf.page_count

        )

        st.metric(

            "Report",

            uploaded_file.name

        )

    pdf.close()

    uploaded_file.seek(0)


# ----------------------------------------------------
# Build Repository
# ----------------------------------------------------

if uploaded_file is not None:

    if st.button(

        "Build Executive Knowledge Repository",

        use_container_width=True

    ):

        uploaded_file.seek(0)

        with st.spinner(

            "Analyzing report..."

        ):
            detector = ChartDetector()
            #plot_detector = PlotDetector()

            pages = detector.convert_pdf_to_images(uploaded_file)
            uploaded_file.seek(0)
            
            header_agent = HeaderAgent(st.secrets["OPENAI_API_KEY"])
            analysis_agent = ChartAnalysisAgent(
                st.secrets["OPENAI_API_KEY"]
            )
            bar_extractor = BarExtractor()
            plot_analyzer = PlotAnalyzer()

            

            
            import json

            for page_index, page in enumerate(pages):

                st.subheader(f"Page {page_index + 1}")

                headers_json = header_agent.detect_headers(page)

                st.json(headers_json)
                st.subheader("Raw Header JSON")

                st.code(headers_json)

                charts = json.loads(headers_json)

                for chart in charts:

                    chart_image = detector.crop_chart(
                        page,
                        chart["bbox"]
                    )
                    st.write("Bounding Box")

                    st.write(chart["bbox"])

# Crop only the plotting area
                    #plot_image = plot_detector.detect_plot_area(
                        #chart_image
                    #)

# Display both images
                    st.image(
                        chart_image,
                        caption=f"{chart['header']}  ({chart_image.width} x {chart_image.height})",
                        use_container_width=True
                    )

                    layout_info = {

                        "header": chart["header"],

                        "chart_type": chart["chart_type"],

                        "legend": chart["structure"]["legend"],

                        "x_axis": chart["structure"]["x_axis"],

                        "y_axis": chart["structure"]["y_axis"]

                    }
                    st.markdown("### Debug")

                    st.write("Header from Chart Object")

                    st.write(chart["header"])

                    st.write("Layout Sent To GPT")

                    st.json(layout_info)
                    bars = bar_extractor.detect_bars(
                        chart_image
                    )
                    plot = plot_analyzer.analyze(chart_image)

                    st.subheader("Detected Plot")

                    st.json(plot)
                    st.write("Plot Height :", plot["height"])
                    st.write("X Axis :", plot["x_axis"])

                    st.subheader("Detected Bars")

                    st.json(bars)

                    st.subheader("Chart Analysis")

                    st.json(analysis)

# ----------------------------------------------------
# Dashboard
# ----------------------------------------------------

if st.session_state["analysis_complete"]:

    st.divider()

    stats = agent.current_session()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Report",

            stats["report"]

        )

    with c2:

        st.metric(

            "Executive Objects",

            stats["executive_objects"]

        )

    with c3:

        st.metric(

            "Relationships",

            stats["relationships"]

        )

    st.divider()

    repository_stats = agent.repository_statistics()

    st.subheader("Knowledge Repository")

    st.json(

        repository_stats

    )

# ----------------------------------------------------
# Agent Health
# ----------------------------------------------------

    with st.expander(

        "Agent Health"

    ):

        st.json(

            agent.health_check()

        )

# ----------------------------------------------------
# Executive Chat
# ----------------------------------------------------

    st.divider()

    st.subheader(

        "Executive Copilot"

    )

    question = st.text_input(

        "Ask a question",

        placeholder="Example: What should I focus on?"

    )

    ask = st.button(

        "Ask Executive Copilot",

        use_container_width=True

    )

    if ask:

        if question.strip() == "":

            st.warning(

                "Enter a question."

            )

        else:

            with st.spinner(

                "Reasoning..."

            ):

                result = agent.ask(

                    question

                )

            st.success(

                "Analysis Complete"

            )

            st.markdown(

                result["answer"]

            )
                        # ============================================
            # AI X-Ray
            # ============================================

            st.divider()

            st.subheader("🔍 AI X-Ray")

            xray = agent.get_xray()

            summary = xray["summary"]

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric("Stages", summary["total_stages"])

            with c2:
                st.metric("Completed", summary["completed"])

            with c3:
                st.metric("Failed", summary["failed"])

            with c4:
                st.metric("Time (ms)", summary["total_time_ms"])

            st.divider()

            for i, stage in enumerate(xray["pipeline"], start=1):

                icon = "🟢"

                if stage["status"] == "Failed":
                    icon = "🔴"

                elif stage["status"] == "Running":
                    icon = "🟡"

                with st.expander(f"{icon} Step {i} : {stage['stage']}"):

                    left, right = st.columns(2)

                    with left:

                        st.write("**Status**")

                        st.success(stage["status"])

                        st.write("**Duration**")

                        st.write(f"{stage['duration_ms']} ms")

                    with right:

                        st.write("**Metrics**")

                        st.json(stage["metrics"])

                    if len(stage["notes"]) > 0:

                        st.write("### Notes")

                        for note in stage["notes"]:

                            st.info(note)

            

# ----------------------------------------------------
# Executive Objects
# ----------------------------------------------------

    with st.expander(

        "Executive Objects"

    ):

        for obj in agent.executive_objects:

            st.markdown(

                f"### {obj.title}"

            )

            st.write(

                f"Type : {obj.object_type}"

            )

            st.write(

                f"Business Area : {obj.business_area}"

            )

            st.write(

                f"Unit : {obj.unit}"

            )

            st.write(

                f"Time Period : {obj.time_period}"

            )

            st.write(

                f"Page : {obj.page}"

            )

            if obj.commentary:

                st.write(

                    "**Commentary**"

                )

                st.json(

                    obj.commentary

                )

            
            if obj.observations:

                st.write(

                    "**Observations**"

                )

                for obs in obj.observations:

                    st.json(

                        vars(obs)

                    )

    
            st.write("RAW OBJECT")

            st.json(vars(obj))


            st.divider()

# ----------------------------------------------------
# Relationships
# ----------------------------------------------------

    with st.expander(

        "Relationships"

    ):

        if len(agent.relationships) == 0:

            st.info(

                "No relationships detected."

            )

        else:

            st.json(

                agent.relationships

            )

# ----------------------------------------------------
# Reset
# ----------------------------------------------------

    st.divider()

    if st.button(

        "Reset Session",

        use_container_width=True

    ):

        agent.reset()

        for key in list(st.session_state.keys()):

            del st.session_state[key]

        st.rerun()

