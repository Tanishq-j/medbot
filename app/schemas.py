"""Pydantic schemas for MedBot API requests and responses."""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class MedicalQuestionRequest(BaseModel):
    """Schema for incoming user medical queries."""
    question: str = Field(
        ...,
        min_length=5,
        max_length=2000,
        description="The medical inquiry, symptoms, or clinical question to analyze.",
        examples=["What are the recommended first-line lifestyle modifications for Stage 1 Hypertension?"]
    )

    @field_validator("question")
    @classmethod
    def validate_question_content(cls, value: str) -> str:
        trimmed = value.strip()
        if len(trimmed) < 5:
            raise ValueError("Question must contain at least 5 non-whitespace characters.")
        return trimmed


# Backwards compatibility alias
LegalQuestionRequest = MedicalQuestionRequest


class MedBotResponse(BaseModel):
    """Schema for multi-agent medical guidance response."""
    status: str = Field(default="success", description="Status of the analysis.")
    question: str = Field(..., description="The original question submitted.")
    answer: str = Field(..., description="Synthesized, reviewed clinical answer.")
    category: Optional[str] = Field(default=None, description="Identified clinical domain or specialty.")
    sources: List[str] = Field(default_factory=list, description="Clinical reference guidelines or library sources cited.")
    disclaimer: str = Field(..., description="Mandatory medical disclaimer.")


# Backwards compatibility alias
LegalBotResponse = MedBotResponse


class HealthResponse(BaseModel):
    """Schema for application health check endpoint."""
    status: str = Field(default="healthy")
    app_name: str
    groq_configured: bool
    model: str
    agents: List[str]
