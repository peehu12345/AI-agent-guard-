"""
Gemini API client for the AI Supervisor.
Uses google-genai SDK with structured JSON output via Pydantic schema.
Falls back gracefully on any failure.
"""
import asyncio
import logging
from typing import Optional
from app.supervisor.schemas import SupervisorResponse
from app.config import settings

logger = logging.getLogger(__name__)

_client = None


def _get_client():
    global _client
    if _client is None and settings.gemini_api_key:
        try:
            from google import genai
            _client = genai.Client(api_key=settings.gemini_api_key)
        except Exception as e:
            logger.warning(f"Failed to initialize Gemini client: {e}")
    return _client


SUPERVISOR_PROMPT_TEMPLATE = """You are AgentGuard's AI Supervisor — an advisory system for autonomous payment agent governance.

Analyze the following transaction context and recommend the SAFEST action. You are ADVISORY ONLY — a deterministic policy engine will make the final decision.

Transaction Context:
- Customer ID: {customer_id}
- Transaction Amount: Rs. {amount:,.0f}
- Payment Status: {status}
- Retry Count: {retry_count} (max allowed: 2)
- Previous Successful Payments: {previous_successful_payments}
- Recovery Probability: {recovery_probability:.0%}
- Intervention Cost: Rs. {intervention_cost:,.0f}
- Last Customer Contact: {last_contact_hours_ago:.0f} hours ago
- Customer Opted Out: {customer_opt_out}
- Risk Level: {risk_level}
- Conflict Detected: {conflict_detected}

Available Actions: RETRY_PAYMENT, SEND_REMINDER, SEND_MESSAGE, OFFER_INCENTIVE, ESCALATE_HUMAN, STOP

Respond with structured JSON matching the exact schema provided. Prioritize customer safety and financial prudence."""


async def gemini_analyze(context: dict) -> Optional[SupervisorResponse]:
    """
    Call Gemini API for AI supervisor analysis.
    Returns None on any failure — caller falls back to mock.
    """
    client = _get_client()
    if not client:
        return None

    try:
        prompt = SUPERVISOR_PROMPT_TEMPLATE.format(
            customer_id=context.get("customer_id", "N/A"),
            amount=float(context.get("amount", 0)),
            status=context.get("status", "FAILED"),
            retry_count=context.get("retry_count", 0),
            previous_successful_payments=context.get("previous_successful_payments", 0),
            recovery_probability=float(context.get("recovery_probability", 0.5)),
            intervention_cost=float(context.get("intervention_cost", 0)),
            last_contact_hours_ago=float(context.get("last_contact_hours_ago", 9999)),
            customer_opt_out=context.get("customer_opt_out", False),
            risk_level=context.get("risk_level", "MEDIUM"),
            conflict_detected=context.get("conflict_detected", False),
        )

        from google import genai
        response = await asyncio.wait_for(
            asyncio.to_thread(
                client.models.generate_content,
                model="gemini-2.0-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": SupervisorResponse,
                },
            ),
            timeout=8.0,
        )

        import json
        data = json.loads(response.text)
        return SupervisorResponse(**data)

    except asyncio.TimeoutError:
        logger.warning("Gemini API timed out — using mock supervisor")
        return None
    except Exception as e:
        logger.warning(f"Gemini API error: {e} — using mock supervisor")
        return None
