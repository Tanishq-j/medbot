"""MedBot Agents Package."""

from app.agents.medical_team import (
    AGENT_NAMES,
    build_medical_team,
    build_legal_team,
    run_medical_workflow,
    run_legal_workflow,
)
from app.agents.tools import (
    clear_consulted_sources,
    get_last_consulted_sources,
    search_medical_library,
    search_legal_library,
)

__all__ = [
    "AGENT_NAMES",
    "build_medical_team",
    "build_legal_team",
    "run_medical_workflow",
    "run_legal_workflow",
    "search_medical_library",
    "search_legal_library",
    "get_last_consulted_sources",
    "clear_consulted_sources",
]
