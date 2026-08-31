from app.agents.base_agent import BaseAgent


class PaymentRecoveryAgent(BaseAgent):
    agent_id = "PaymentRecoveryAgent"
    priority = 2

    def can_handle(self, context: dict) -> bool:
        # Handles failed payments under Rs. 1,00,000
        return context.get("status", "FAILED") == "FAILED" and float(context.get("amount", 0)) < 100000

    def generate_recommendation(self, context: dict) -> dict:
        retry_count = context.get("retry_count", 0)
        prob = context.get("recovery_probability", 0.5)
        amount = float(context.get("amount", 0))

        confidence = min(max(prob, 0.45), 0.90)

        if retry_count == 0:
            action = "RETRY_PAYMENT"
            reasoning = (
                f"First failure detected on Rs. {amount:,.0f} payment. "
                f"Immediate retry recommended — recovery probability {prob:.0%}."
            )
        elif retry_count == 1:
            action = "SEND_MESSAGE"
            confidence = max(confidence - 0.15, 0.45)
            reasoning = (
                f"First retry failed. Sending payment recovery message to customer "
                f"with link to update payment method. Amount: Rs. {amount:,.0f}."
            )
        else:
            action = "ESCALATE_HUMAN"
            confidence = 0.6
            reasoning = (
                f"Payment has failed {retry_count} times. Amount Rs. {amount:,.0f}. "
                f"Manual intervention required."
            )

        return self._make_recommendation(context, action, confidence, reasoning)
