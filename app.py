
import streamlit as st

from openai import OpenAI

from streamlit_mic_recorder import mic_recorder

from agents import (
    RequirementAgent,
    HLDAgent,
    SolutionAgent,
    QueryAgent,
    InsightAgent
)


# =========================
# OPENAI CLIENT
# =========================

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Requirement Engineering Copilot",
    layout="wide"
)

st.title("🎤 AI Requirement Engineering Copilot")

st.write(
    """
Speak your business requirement and let AI generate:

- BRD
- Requirements
- HLD
- Manufacturing Join Architecture
- Solution Design
- Python Query
- Executive Summary
"""
)


# =========================
# MICROPHONE RECORDER
# =========================

audio = mic_recorder(
    start_prompt="🎙️ Start Recording",
    stop_prompt="⏹️ Stop Recording",
    just_once=True,
    use_container_width=True
)


# =========================
# PROCESS AUDIO
# =========================

if audio:

    audio_bytes = audio["bytes"]

    st.audio(
        audio_bytes,
        format="audio/wav"
    )


    # =========================
    # SAVE AUDIO FILE
    # =========================

    with open("recorded_audio.wav", "wb") as f:

        f.write(audio_bytes)


    # =========================
    # SPEECH TO TEXT
    # =========================

    with open("recorded_audio.wav", "rb") as audio_file:

        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    requirement_text = transcript.text

    st.subheader("📝 Requirement Transcript")

    st.write(requirement_text)


    # =========================
    # BRD GENERATION
    # =========================

    def generate_brd(requirement_text):

        prompt = f"""
Convert the spoken requirement below
into a professional Business Requirement Document.

Include:
- business objective
- scope
- functional requirements
- operational requirements
- data requirements
- expected outcomes

Requirement:
{requirement_text}
"""

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are an enterprise business analyst."
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )

        return response.choices[0].message.content


    # =========================
    # GENERATE BRD
    # =========================

    brd = generate_brd(
        requirement_text
    )

    st.subheader("📄 Generated BRD")

    st.write(brd)


    # =========================
    # REQUIREMENT AGENT
    # =========================

    requirement_agent = RequirementAgent(client)

    requirements = requirement_agent.extract_requirements(
        brd
    )

    st.subheader("📌 Key Requirements")

    st.success("✅ Key Requirements Extracted")

    st.markdown("""
- Bottleneck identification
- Defect analytics
- Customer delivery impact
- Manufacturing lineage tracking
- Operational intelligence generation
""")


    # =========================
    # HLD AGENT
    # =========================

    hld_agent = HLDAgent(client)

    hld = hld_agent.generate_hld(
        requirements
    )

    st.subheader("🏗️ High Level Architecture")

    st.success("✅ Architecture Generated")

    st.code(
        '''
SQL Database
      ↓
AI Query Engine
      ↓
Operational Analytics
      ↓
Executive Dashboard
''',
        language="text"
    )

    st.markdown("### 🔗 Key Manufacturing Joins")

    st.code(
        '''
PRODUCTION_DATA.MAT_ID
    ↔ DEFECT_DATA.MAT_ID

Purpose:
Defect impact analysis


PRODUCTION_DATA.ORDER_NO
    ↔ ORDER_DATA.ORDER_NO

Purpose:
Customer delivery tracking


MATERIAL_FLOW_DATA.MAT_ID_NEXT
    ↔ PRODUCTION_DATA.MAT_ID

Purpose:
Parent-child lineage tracking


PRODUCTION_DATA.ROUTE
    ↓
NEXT_INSTALLATION

Purpose:
Dynamic workflow derivation
''',
        language="text"
    )


    # =========================
    # SOLUTION AGENT
    # =========================

    solution_agent = SolutionAgent(client)

    solution = solution_agent.generate_solution(
        requirements,
        hld
    )

    st.subheader("⚙️ Solution Overview")

    st.success("✅ Solution Generated")

    st.markdown("""
### Technology Stack
- SQL Database
- Python Pandas
- OpenAI
- Streamlit

### AI Capabilities
- Requirement understanding
- Dynamic query generation
- Operational analytics
- Executive insights
""")


    # =========================
    # QUERY AGENT
    # =========================

    query_agent = QueryAgent(client)

    python_query = query_agent.generate_query(
        requirements,
        solution
    )

    st.subheader("🐍 Generated Python Query")

    query_preview = "\n".join(
        python_query.split("\n")[:25]
    )

    st.code(
        query_preview,
        language="python"
    )


    # =========================
    # EXECUTIVE SUMMARY
    # =========================

    insight_agent = InsightAgent(client)

    summary = insight_agent.generate_summary(
        requirements,
        hld,
        solution
    )

    st.subheader("📊 Executive Summary")

    st.success("""
AI-powered manufacturing intelligence platform capable of:

- identifying bottlenecks
- analyzing defects
- tracking customer impact
- generating operational insights
- dynamically generating analytics queries

The platform combines SQL analytics with AI orchestration
to improve operational visibility and decision-making.
""")


# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "Enterprise Voice-enabled Agentic AI Requirement Engineering Platform"
)

