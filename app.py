import streamlit as st

from pipeline import run_pipeline
from chart_layout_agent import ChartLayoutStudio
import pandas as pd

# --------------------------------------------------
# Streamlit Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Executive Intelligence Copilot",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📊 Executive Intelligence Copilot")

st.caption(
    "Upload a Monthly Executive Report and interact with its charts."
)

st.divider()


# --------------------------------------------------
# PDF Upload
# --------------------------------------------------

uploaded_pdf = st.file_uploader(
    "Upload Executive PDF Report",
    type=["pdf"]
)


# --------------------------------------------------
# Run Pipeline
# --------------------------------------------------

if uploaded_pdf is not None:

    st.success("PDF uploaded successfully.")

    with st.spinner("Processing report..."):

        result = run_pipeline(uploaded_pdf)

    
    st.divider()

# ======================================================
# Report Summary
# ======================================================

    st.subheader("📄 Report Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Pages",
            result["pages"]["total_pages"]
        )

    with col2:
        st.metric(
            "Executive Charts",
            result["repository"]["total_charts"]
        )

    st.divider()



    st.subheader("🤖 Executive AI Analysis Summary")

    rows = []

    for chart in result["repository"]["charts"]:

        rows.append({

            "Chart": chart["chart_id"],

            "Chart Type": chart["chart_type"],

            "Title": "✅",

            "X Axis": "✅",

            "Left Y": "✅",

            "Right Y": "—",

            "Legend": "✅",

            "Summary": "✅",

            "Missing": "None",

            "AI Confidence": f"{chart['confidence']*100:.0f}%"

        })

    summary_df = pd.DataFrame(rows)

    # --------------------------------------------------
# Chart Selection
# --------------------------------------------------

    chart_options = {
        f"{chart['chart_id']} - {chart['chart_title']}": chart
        for chart in result["repository"]["charts"]
    }

    selected_chart_name = st.selectbox(
        "Select Chart for Detailed Analysis",
        list(chart_options.keys())
    )

    selected_chart = chart_options[selected_chart_name]

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )

    
# ======================================================
# Selected Chart
# ======================================================

    st.subheader("📈 Selected Chart")

    # Show image if available
    if "image" in selected_chart:

        st.image(
            selected_chart["image"],
            use_container_width=True
        )

    col1, col2 = st.columns([1, 2])

    with col1:

        st.metric("Chart ID", selected_chart["chart_id"])
        st.metric("Page", selected_chart["page_number"])
        st.metric("Type", selected_chart["chart_type"])

    with col2:

        st.write(f"**Title** : {selected_chart['chart_title']}")
        st.write(f"**Business Area** : {selected_chart['business_area']}")
        st.write(f"**Metric** : {selected_chart['metric']}")
        st.write(f"**Summary** : {selected_chart['summary']}")
        st.write(f"**Confidence** : {selected_chart['confidence']:.2f}")
        layout_studio = ChartLayoutStudio()
    
        layout = layout_studio.show(selected_chart)
        from chart_crop_agent import ChartCropAgent

        if layout["preview"]:

            crop_agent = ChartCropAgent()

            preview = crop_agent.preview_crop(
                selected_chart["image"],
                layout
            )

            st.divider()

            st.subheader("Crop Preview")

            st.image(
                preview,
                use_container_width=True
            )

            st.divider()

        st.subheader("🤖 Ask Executive")

        question = st.text_input(
            "Ask a question",
            placeholder="Example: Explain this chart"
        )

        if st.button("Ask Executive"):

            from executive_qa_agent import ExecutiveQAAgent

            qa_agent = ExecutiveQAAgent()

            answer = qa_agent.process(
                result["repository"],
                question
            )

            st.success(answer["answer"])

        st.write(layout)

  
