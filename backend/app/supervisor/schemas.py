"""
AI Supervisor Schema — Structured input/output for the LLM layer.
"""
from typing import Optional
from pydantic import BaseModel, field_validator


VALID_ACTIONS = ["RETRY_PAYMENT", "SEND_REMINDER", "SEND_MESSAGE", "OFFER_INCENTIVE", "ESCALATE_HUMAN", "STOP"]
VALID_RISK_LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


class SupervisorResponse(BaseModel):
    recommended_action: str
    confidence: float
    reason: str
    risk_level: str
    requires_human_review: bool
    secondary_action: Optional[str] = None
    secondary_reason: Optional[str] = None

    @field_validator("recommended_action")
    @classmethod
    def validate_action(cls, v):
        if v not in VALID_ACTIONS:
            raise ValueError(f"Invalid action: {v}. Must be one of {VALID_ACTIONS}")
        return v

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v):
        return round(min(max(float(v), 0.0), 1.0), 3)

    @field_validator("risk_level")
    @classmethod
    def validate_risk(cls, v):
        if v not in VALID_RISK_LEVELS:
            return "MEDIUM"
        return v
