"""Streamlit Frontend for MedBot — Multi-Agent Medical Assistant.

Assignment 10, GenAI Lab, CSE(AI/ML) KITCoEK
Permanent dark theme with prescription/report image upload and clinical guidance.
"""

import os
import sys
from pathlib import Path

# Ensure root directory is on Python path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import streamlit as st
from app import config
from app.agents.medical_team import AGENT_NAMES, run_medical_workflow
from app.data.sample_documents import SAMPLE_MEDICAL_DOCUMENTS

# Page configuration
st.set_page_config(
    page_title="MedBot — Multi-Agent Medical Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar: Branding, System Overview & Engine Status
with st.sidebar:
    st.title("🩺 MedBot")
    st.caption("Multi-Agent Medical Assistant")
    st.markdown(
        "<div style='font-size: 0.85rem; color: #60a5fa; font-weight: 600; line-height: 1.4; margin-top: -4px; margin-bottom: 12px;'>"
        "Assignment 10, GenAI Lab, CSE(AI/ML)&nbsp;&nbsp;KITCoEK"
        "</div>",
        unsafe_allow_html=True,
    )
    st.divider()

    # Engine Status
    st.subheader("System Status")
    is_ready = config.is_provider_configured()
    active_model = config.get_active_model_name()
    if is_ready:
        st.success(f"● Connected: {active_model}")
        st.caption(f"Provider: `{config.MODEL_PROVIDER.upper()}`")
    else:
        st.error(f"● {config.MODEL_PROVIDER.capitalize()} API Key Missing")
        if config.MODEL_PROVIDER == "google":
            st.info("Please add `GEMINI_API_KEY` to `.env` (free from [Google AI Studio](https://aistudio.google.com/apikey)).")
        else:
            st.info("Please set `GROQ_API_KEY` in `.env`.")

    st.divider()

    # The 3 Agno Agents
    st.subheader("Collaborating Agno Agents")
    st.markdown(
        """
        1. **Medical Query Analyzer**  
           *Classifies clinical specialty, extracts patient vitals, and frames key issues.*
        
        2. **Medical Research Agent**  
           *Searches evidence-based clinical guidelines, dosing limits, and safety standards.*
        
        3. **Medical Answer Reviewer**  
           *Cross-examines claims, eliminates inaccuracies, and synthesizes clinical guidance.*
        """
    )

    st.divider()

    # Grounding Clinical Library
    with st.expander("📚 Grounding Clinical Library", expanded=False):
        for doc in SAMPLE_MEDICAL_DOCUMENTS:
            st.markdown(f"**{doc['title']}**")
            st.caption(f"Category: {doc['category']}")
            st.caption(doc["summary"])
            st.markdown("---")


# Permanent Professional Dark Theme Stylesheet (Light mode disabled)
st.markdown(
    """
    <style>
    #MainMenu { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    footer { display: none !important; }

    header {
        background: transparent !important;
    }
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"] {
        visibility: visible !important;
        display: flex !important;
        color: #93c5fd !important;
        z-index: 999999 !important;
    }

    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    .medical-banner {
        background-color: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.25);
        color: #fde68a;
        padding: 10px 16px;
        border-radius: 6px;
        font-size: 0.88rem;
        margin-bottom: 20px;
    }
    .academic-tag {
        display: inline-block;
        background-color: rgba(59, 130, 246, 0.12);
        color: #93c5fd;
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .memo-card-header {
        background: #111827;
        border: 1px solid #1e293b;
        border-radius: 8px 8px 0 0;
        padding: 12px 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #3b82f6;
    }
    .memo-tag {
        background-color: rgba(59, 130, 246, 0.15);
        color: #93c5fd;
        border: 1px solid rgba(59, 130, 246, 0.35);
        font-weight: 700;
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 4px;
        letter-spacing: 0.05em;
    }
    .audit-seal {
        background-color: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #34d399;
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 0.84rem;
        font-weight: 600;
        margin-top: 18px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .evidence-badge {
        background-color: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #c7d2fe;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.82rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 12px;
    }
    .disclaimer-foot {
        color: #94a3b8;
        font-size: 0.78rem;
        line-height: 1.45;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Session state for inquiry, image & answer persistence
if "question_text" not in st.session_state:
    st.session_state.question_text = ""
if "response_data" not in st.session_state:
    st.session_state.response_data = None
if "attached_doc_name" not in st.session_state:
    st.session_state.attached_doc_name = None


# Main Page Content
st.title("Clinical Inquiry & Medical Guidance")
st.markdown(
    '<div class="academic-tag">Assignment 10, GenAI Lab, CSE(AI/ML) &nbsp;&bull;&nbsp; KITCoEK</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="medical-banner">'
    '<strong>Notice:</strong> MedBot is an educational assistant designed for GenAI & ML DevOps coursework. '
    'It provides clinical information and practice guideline analysis, but does not provide formal medical diagnosis, treatment, or prescription.'
    '</div>',
    unsafe_allow_html=True,
)

# Common clinical scenario buttons
st.write("**Common Clinical Scenarios:**")
col1, col2 = st.columns(2)
with col1:
    if st.button("🩺 Stage 1 Hypertension & BP Monitoring", use_container_width=True):
        st.session_state.question_text = (
            "What are the diagnostic thresholds, first-line lifestyle interventions, "
            "and target blood pressure readings for Stage 1 Hypertension under ACC/AHA guidelines?"
        )
    if st.button("🩸 Type 2 Diabetes HbA1c & Hypoglycemia Protocol", use_container_width=True):
        st.session_state.question_text = (
            "What are the target HbA1c goals for non-pregnant adults with Type 2 Diabetes, "
            "and what are the exact steps of the 'Rule of 15' for acute hypoglycemia?"
        )

with col2:
    if st.button("💊 Paracetamol vs NSAID Safety & Organ Risks", use_container_width=True):
        st.session_state.question_text = (
            "What are the maximum safe daily limits for paracetamol to prevent hepatotoxicity, "
            "and what are the primary renal and gastrointestinal contraindications for NSAIDs?"
        )
    if st.button("🚨 Acute Chest Pain & Stroke Red Flag Triage", use_container_width=True):
        st.session_state.question_text = (
            "What are the critical red flag signs of Acute Coronary Syndrome and the FAST protocol criteria "
            "that mandate immediate emergency activation?"
        )

st.write("")

# Query Input Form with Media Upload
with st.form("inquiry_form"):
    user_query = st.text_area(
        "Enter your medical inquiry, symptoms, or medication question:",
        value=st.session_state.question_text,
        height=130,
        placeholder="E.g., What are the lifestyle and monitoring recommendations for newly diagnosed high blood pressure (135/85 mmHg)?",
        max_chars=2000,
    )

    # Document Image Upload
    uploaded_image = st.file_uploader(
        "📷 Upload Prescription, Lab Report, or Clinical Scan (Optional):",
        type=["png", "jpg", "jpeg", "webp"],
        help="Attach a photo of a prescription, laboratory report, discharge summary, or vital signs log.",
    )

    if uploaded_image:
        st.caption(f"📎 Attached file: `{uploaded_image.name}` ({uploaded_image.size // 1024} KB)")

    btn_col1, btn_col2, _ = st.columns([1.5, 1, 4])
    with btn_col1:
        submitted = st.form_submit_button("Analyze Clinical Issue", type="primary", use_container_width=True)
    with btn_col2:
        cleared = st.form_submit_button("Clear", use_container_width=True)

if cleared:
    st.session_state.question_text = ""
    st.session_state.response_data = None
    st.session_state.attached_doc_name = None
    st.rerun()

if submitted:
    cleaned_query = user_query.strip()
    if not cleaned_query and not uploaded_image:
        st.error("Please enter a medical question or upload a clinical document photo to analyze.")
    elif cleaned_query and len(cleaned_query) < 5 and not uploaded_image:
        st.error("Please enter a medical inquiry with at least 5 characters.")
    elif not config.is_provider_configured():
        st.error(f"API Key for {config.MODEL_PROVIDER.upper()} is not configured. Please add your key to `.env`.")
    else:
        # If question is empty but image provided, default query
        if not cleaned_query and uploaded_image:
            cleaned_query = f"Examine this attached clinical report ({uploaded_image.name}), extract vital indicators and values, and provide clinical analysis under evidence-based medical guidelines."

        st.session_state.question_text = cleaned_query
        st.session_state.attached_doc_name = uploaded_image.name if uploaded_image else None

        # Read image data if provided
        img_bytes = uploaded_image.getvalue() if uploaded_image else None
        img_name = uploaded_image.name if uploaded_image else None
        img_mime = uploaded_image.type if uploaded_image else None

        # Multi-agent coordination progress
        progress_placeholder = st.empty()
        with progress_placeholder.container():
            if img_bytes:
                st.info("Analyzing clinical evidence & coordinating Agno Medical Team (Analyzer ➔ Researcher ➔ Reviewer)...")
            else:
                st.info("Coordinating Agno Medical Team (Analyzer ➔ Researcher ➔ Reviewer)...")

        try:
            with st.spinner("Multi-agent team researching clinical practice guidelines and reviewing memo..."):
                result = run_medical_workflow(
                    cleaned_query,
                    image_bytes=img_bytes,
                    image_filename=img_name,
                    image_mime_type=img_mime,
                )
                st.session_state.response_data = result
        except Exception as e:
            st.error(f"Error during clinical reasoning: {str(e)}")
        finally:
            progress_placeholder.empty()


# Display Response
if st.session_state.response_data:
    resp = st.session_state.response_data
    answer_text = resp.get("answer", "")
    sources = resp.get("sources", [])

    st.write("---")

    # Clinical Memorandum Card
    st.markdown(
        """
        <div class="memo-card-header">
            <div>
                <span class="memo-tag">CLINICAL ADVISORY MEMORANDUM</span>
                <span style="font-size: 0.85rem; font-weight: 600; margin-left: 10px;">Practice Guideline Findings</span>
            </div>
            <div style="font-size: 0.78rem; opacity: 0.8;">
                Team: Analyzer &bull; Researcher &bull; Reviewer
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Document Evidence Badge if image was analyzed
    if st.session_state.attached_doc_name:
        st.markdown(
            f'<div class="evidence-badge">📎 <strong>Analyzed Evidence:</strong> {st.session_state.attached_doc_name}</div>',
            unsafe_allow_html=True,
        )

    # Sources panel
    if sources:
        with st.expander(f"📚 Grounding Clinical Sources Consulted ({len(sources)})", expanded=True):
            for s in sources:
                st.markdown(f"- **{s}**")

    # Answer Markdown
    st.markdown("### Clinical Analysis & Review")
    st.markdown(answer_text)

    # Verification seal
    st.markdown(
        f"""
        <div class="audit-seal">
            <span>✓</span>
            <span>Audited by Medical Answer Reviewer &bull; Grounded in evidence-based practice guidelines</span>
        </div>
        <p class="disclaimer-foot">
            <strong>Disclaimer:</strong> {config.MEDICAL_DISCLAIMER}
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Download answer option
    evidence_note = f"\nEvidence: {st.session_state.attached_doc_name}\n" if st.session_state.attached_doc_name else ""
    st.download_button(
        label="Download Clinical Memo (.txt)",
        data=(
            f"CLINICAL ADVISORY MEMORANDUM\n\nInquiry:\n{st.session_state.question_text}\n"
            f"{evidence_note}\nAnswer:\n{answer_text}\n\nSources:\n"
            + "\n".join(sources)
            + f"\n\n{config.MEDICAL_DISCLAIMER}"
        ),
        file_name="clinical_guidance_memo.txt",
        mime="text/plain",
    )
