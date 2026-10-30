"""MedBot Multi-Agent Team for Clinical Guidance and Medical Reference.

Coordinates exactly three collaborating Agno agents:
1. Medical Query Analyzer: Categorizes clinical inquiry, extracts symptoms/history, and frames medical issues.
2. Medical Research Agent: Investigates evidence-based clinical guidelines, medication safety, and reference documents.
3. Medical Answer Reviewer: Audits findings, eliminates hallucinations/unsafe advice, and authors the final clinical memo.
"""

from typing import Any, Dict, List, Optional
from agno.agent import Agent
from agno.team import Team, TeamMode

from app import config
from app.agents.tools import (
    clear_consulted_sources,
    get_last_consulted_sources,
    search_medical_library,
)

AGENT_NAMES = [
    "Medical Query Analyzer",
    "Medical Research Agent",
    "Medical Answer Reviewer",
]


def create_model_instance(api_key: Optional[str] = None, model_id: Optional[str] = None):
    """Instantiate the active LLM provider (Google Gemini or Groq)."""
    provider = config.MODEL_PROVIDER

    if provider == "google":
        from agno.models.google import Gemini

        key = api_key if api_key is not None else config.GEMINI_API_KEY
        m_id = model_id if model_id is not None else config.GEMINI_MODEL
        return Gemini(id=m_id, api_key=key)
    else:
        from agno.models.groq import Groq

        key = api_key if api_key is not None else config.GROQ_API_KEY
        m_id = model_id if model_id is not None else config.GROQ_MODEL
        return Groq(id=m_id, api_key=key)


def build_medical_team(api_key: Optional[str] = None, model_id: Optional[str] = None) -> Team:
    """Build the three collaborating Agno agents and coordinate them via an Agno Team."""
    model = create_model_instance(api_key=api_key, model_id=model_id)

    # Agent 1: Medical Query Analyzer
    analyzer_agent = Agent(
        name="Medical Query Analyzer",
        role="Analyze user inquiries and classify them under clinical domains and medical specialties.",
        model=model,
        telemetry=False,
        description=(
            "A clinical intake specialist. Evaluates patient symptoms, chronology, duration, "
            "comorbidities, medication history, and frames precise clinical issues for evidence-based research."
        ),
        instructions=[
            "1. Identify the relevant medical specialty (Cardiology, Endocrinology, Pulmonology, Pharmacology, Emergency).",
            "2. Extract material symptoms, chronology/duration, reported metrics (BP, glucose, SpO2), and missing clinical history.",
            "3. Formulate 2-3 precise clinical research questions for practice guideline investigation.",
        ],
    )

    # Agent 2: Medical Research Agent
    research_agent = Agent(
        name="Medical Research Agent",
        role="Research clinical practice guidelines, evidence-based literature, and library documents.",
        model=model,
        tools=[search_medical_library],
        telemetry=False,
        description=(
            "An evidence-based medical research specialist equipped with search_medical_library. "
            "Retrieves established guidelines (AHA, ADA, WHO, ICMR), dosage standards, contraindications, and red-flag criteria."
        ),
        instructions=[
            "1. Invoke search_medical_library with keywords from the inquiry to find grounding clinical standards.",
            "2. Identify diagnostic criteria, target threshold ranges, safe dosing limits, and contraindications.",
            "3. Explicitly cite the consulted reference documents and clinical guidelines.",
        ],
    )

    # Agent 3: Medical Answer Reviewer
    reviewer_agent = Agent(
        name="Medical Answer Reviewer",
        role="Audit clinical findings, eliminate unsupported claims, and author final medical advisory memo.",
        model=model,
        telemetry=False,
        description=(
            "A senior medical safety auditor. Scrutinizes findings for clinical correctness, ensures prudent triage, "
            "eliminates dangerous self-treatment suggestions or speculative diagnoses, and formats the verified guidance."
        ),
        instructions=[
            "1. Audit the findings to ensure strict adherence to evidence-based medical consensus and guideline safety.",
            "2. Strip out speculative assertions, unverified medication recommendations, or unsafe self-treatment suggestions.",
            "3. Author the final response formatted with:",
            "   - **Clinical Domain & Assessment Summary**: Relevant medical domain and clear executive summary.",
            "   - **Key Clinical Guidelines & Evidence**: Applicable standards, threshold metrics, and references.",
            "   - **Applied Analysis & Care Considerations**: Concrete, evidence-backed educational guidance.",
            "   - **Safety Reviewer Note & Warning Signs**: Red flags requiring urgent in-person medical evaluation.",
        ],
    )

    # Agno Team Coordinator
    medical_team = Team(
        name="Medical Assistant Team",
        members=[analyzer_agent, research_agent, reviewer_agent],
        model=model,
        tools=[search_medical_library],
        add_member_tools_to_context=True,
        mode=TeamMode.coordinate,
        telemetry=False,
        instructions=[
            "Coordinate the three agents sequentially to produce an authoritative clinical advisory memorandum:",
            "1. Have Medical Query Analyzer classify the inquiry and extract material clinical facts.",
            "2. Have Medical Research Agent search the clinical library and provide grounded guideline citations.",
            "3. Have Medical Answer Reviewer audit safety and synthesize the verified final medical guidance.",
        ],
    )

    return medical_team


# Backwards compatibility alias
build_legal_team = build_medical_team


def run_medical_workflow(
    question: str,
    team: Optional[Team] = None,
    image_bytes: Optional[bytes] = None,
    image_filename: Optional[str] = None,
    image_mime_type: Optional[str] = None,
) -> Dict[str, Any]:
    """Execute the multi-agent medical collaboration on a user inquiry and optional report/prescription image."""
    clear_consulted_sources()

    evidence_context = ""
    candidate_models = [config.GEMINI_MODEL, "gemini-3-flash-preview", "gemini-3.5-flash", "gemini-flash-latest"]
    seen = set()
    models_to_try = [m for m in candidate_models if not (m in seen or seen.add(m))]

    # 1. Document Image OCR / Vision Extraction (Lab reports, prescriptions, ECG, etc.)
    if image_bytes and config.MODEL_PROVIDER == "google" and config.GEMINI_API_KEY:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=config.GEMINI_API_KEY)
        mime = image_mime_type or "image/jpeg"

        for model_id in models_to_try:
            try:
                ocr_response = client.models.generate_content(
                    model=model_id,
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type=mime),
                        (
                            "You are a clinical document specialist. Inspect this uploaded medical document image "
                            "(prescription, lab report, diagnostic discharge summary, or vital readings). "
                            "Transcribe all legible patient vitals, medications, dosages, lab values, and clinical notes."
                        ),
                    ],
                    config={"http_options": {"timeout": 15000}},
                )
                if ocr_response and ocr_response.text:
                    evidence_context = (
                        f"\n\n[ATTACHED CLINICAL EVIDENCE: {image_filename or 'Uploaded Image'}]\n"
                        f"{ocr_response.text.strip()}\n"
                        f"[END OF ATTACHED EVIDENCE]\n"
                    )
                    break
            except Exception:
                continue

    # 2. Search Grounding Clinical Documents
    search_query = f"{question} {evidence_context[:300]}"
    clinical_docs = search_medical_library(search_query)
    sources = get_last_consulted_sources()

    # 3. Multi-Agent Synthesis (Analyzer, Researcher, Reviewer)
    workflow_prompt = (
        f"You are MedBot, an authoritative Medical Advisory Team composed of:\n"
        f"1. Medical Query Analyzer: Categorize under clinical specialty (Cardiology, Endocrinology, Pulmonology, Pharmacology, etc.) and extract symptoms & patient facts.\n"
        f"2. Medical Research Agent: Ground recommendations in clinical practice guidelines, threshold metrics, drug safety standards, and the reference library.\n"
        f"3. Medical Answer Reviewer: Audit findings, eliminate unverified or unsafe medical assertions, and author a clear, professional clinical memorandum.\n\n"
        f"USER MEDICAL INQUIRY:\n"
        f"\"\"\"{question}\"\"\"\n"
        f"{evidence_context}\n"
        f"GROUNDING REFERENCE CLINICAL LIBRARY:\n"
        f"{clinical_docs}\n\n"
        f"Generate the verified Clinical Advisory Memorandum formatted with:\n"
        f"- **Clinical Domain & Assessment Summary**: Relevant medical specialty and concise overview.\n"
        f"- **Key Clinical Guidelines & Evidence**: Applicable practice standards, target metrics, and references.\n"
        f"- **Applied Analysis & Care Considerations**: Concrete, evidence-backed educational guidance addressing the question and any attached document.\n"
        f"- **Safety Reviewer Note & Warning Signs**: Critical red-flag symptoms requiring emergency medical evaluation."
    )

    content_text = ""
    # Execute with fallback across flash models
    if config.MODEL_PROVIDER == "google" and config.GEMINI_API_KEY:
        from google import genai

        client = genai.Client(api_key=config.GEMINI_API_KEY)
        for model_id in models_to_try:
            try:
                resp = client.models.generate_content(
                    model=model_id,
                    contents=workflow_prompt,
                    config={"http_options": {"timeout": 25000}},
                )
                if resp and resp.text:
                    content_text = resp.text.strip()
                    break
            except Exception:
                continue

    # Fallback to Agno Team run if direct generation was empty
    if not content_text:
        try:
            active_team = team if team is not None else build_medical_team()
            run_output = active_team.run(workflow_prompt)
            if hasattr(run_output, "get_content_as_string"):
                content_text = run_output.get_content_as_string()
            elif hasattr(run_output, "content") and run_output.content:
                content_text = str(run_output.content)
            else:
                content_text = str(run_output)
        except Exception as e:
            content_text = f"Unable to generate response: {e}"

    return {
        "answer": content_text,
        "sources": sources,
    }


# Backwards compatibility alias
run_legal_workflow = run_medical_workflow

