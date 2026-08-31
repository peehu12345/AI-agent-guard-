from app.agents.base_agent import BaseAgent


RISK_CONFIDENCE_MAP = {
    "LOW": 0.55,
    "MEDIUM": 0.65,
    "HIGH": 0.75,
    "CRITICAL": 0.85,
}


class ReceivablesAgent(BaseAgent):
    agent_id = "ReceivablesAgent"
    priority = 4

    def can_handle(self, context: dict) -> bool:
        # Handles high-value or high-risk transactions
        amount = float(context.get("amount", 0))
        risk = context.get("risk_level", "LOW")
        return amount > 25000 or risk in ["HIGH", "CRITICAL"]

    def generate_recommendation(self, context: dict) -> dict:
        amount = float(context.get("amount", 0))
        risk = context.get("risk_level", "MEDIUM")
        retry_count = context.get("retry_count", 0)
        confidence = RISK_CONFIDENCE_MAP.get(risk, 0.65)

        if risk in ["HIGH", "CRITICAL"] or (amount > 75000 and retry_count > 0):
            action = "ESCALATE_HUMAN"
            reasoning = (
                f"High-risk receivable (Rs. {amount:,.0f}, risk={risk}). "
                f"After {retry_count} failed attempts, escalating to human review "
                f"to protect against financial loss."
            )
        else:
            action = "SEND_REMINDER"
            reasoning = (
                f"Outstanding receivable of Rs. {amount:,.0f} with {risk} risk. "
                f"Sending formal payment reminder as first intervention."
            )

        return self._make_recommendation(context, action, confidence, reasoning)
