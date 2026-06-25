import streamlit as st
import fitz
from PIL import Image
import io

from knowledge_repository import RepositoryManager
from executive_agent import ExecutiveAgent

# ----------------------------------------------------
# Streamlit Configuration
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

    repo = RepositoryManager()

    repo.initialize_database()

    st.session_state["repository"] = repo

# ----------------------------------------------------
# Executive Agent
# ----------------------------------------------------

if "executive_agent" not in st.session_state:

    st.session_state["executive_agent"] = ExecutiveAgent(

        st.secrets["OPENAI_API_KEY"],

        st.session_state["repository"]

    )

agent = st.session_state["executive_agent"]

# ----------------------------------------------------
# Upload PDF
# ----------------------------------------------------

uploaded_file = st.file_uploader(

    "Upload Executive Report",

    type=["pdf"]

)

# ----------------------------------------------------
# PDF Preview
# ----------------------------------------------------

if uploaded_file is not None:

    pdf = fitz.open(

        stream=uploaded_file.read(),

        filetype="pdf"

    )

    st.success(

        f"Loaded {pdf.page_count} pages."

    )

    page_no = st.selectbox(

        "Select Page",

        range(pdf.page_count)

    )

    page = pdf.load_page(page_no)

    pix = page.get_pixmap(

        matrix=fitz.Matrix(2,2)

    )

    img = pix.tobytes("png")

    st.image(

        img,

        caption=f"Page {page_no+1}",

        use_container_width=True

    )

# ----------------------------------------------------
# Build Knowledge Repository
# ----------------------------------------------------
if uploaded_file is not None:

    if st.button(

        "Build Executive Knowledge Repository"

    ):



    with st.spinner(

        "Analyzing report..."

    ):
        uploaded_file.seek(0)
        result = agent.process_report(

            uploaded_file

        )

        st.session_state["analysis_complete"] = True

        st.success(

            "Knowledge Repository Updated"

        )

        st.write(result)

# ----------------------------------------------------
# Executive Repository Dashboard
# ----------------------------------------------------

if st.session_state.get("analysis_complete", False):

    st.divider()

    st.subheader("Executive Repository")

    stats = agent.repository_statistics()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Current Report",
            stats["current_report"]
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

    st.subheader("Executive Copilot")

    question = st.text_input(

        "Ask anything about this report",

        placeholder="Example: What should I focus on?"

    )

    if st.button("Ask Executive Copilot"):

        if question.strip() == "":

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Reasoning..."
            ):

                result = agent.ask(
                    question
                )

                st.markdown(
                    result["answer"]
                )

# ----------------------------------------------------
# View Executive Objects
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
                f"Page : {obj.page}"
            )

            st.write(
                "Observations"
            )

            for obs in obj.observations:

                st.json(
                    vars(obs)
                )

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

        "Reset Session"

    ):

        agent.reset()

        st.session_state.clear()

        st.rerun()
