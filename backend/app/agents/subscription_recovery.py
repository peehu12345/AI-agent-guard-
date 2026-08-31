from app.agents.base_agent import BaseAgent


class SubscriptionRecoveryAgent(BaseAgent):
    agent_id = "SubscriptionRecoveryAgent"
    priority = 1

    def can_handle(self, context: dict) -> bool:
        # Handles customers with a history of successful subscription payments
        return context.get("previous_successful_payments", 0) >= 2

    def generate_recommendation(self, context: dict) -> dict:
        retry_count = context.get("retry_count", 0)
        prob = context.get("recovery_probability", 0.5)
        prev_payments = context.get("previous_successful_payments", 0)

        # Confidence based on payment history
        confidence = min(0.5 + (prev_payments / 20), 0.95)

        if retry_count < 2 and prob > 0.5:
            action = "RETRY_PAYMENT"
            reasoning = (
                f"Customer has {prev_payments} prior successful payments. "
                f"Recovery probability {prob:.0%}. Retry attempt {retry_count + 1} of 2 allowed."
            )
        elif retry_count == 1:
            action = "SEND_REMINDER"
            confidence = max(confidence - 0.1, 0.5)
            reasoning = (
                f"First retry already attempted. Sending reminder to customer with "
                f"{prev_payments} successful payment history before final retry."
            )
        else:
            action = "ESCALATE_HUMAN"
            confidence = 0.6
            reasoning = (
                f"Retry limit reached after {retry_count} attempts. "
                f"Escalating to human review given customer's subscription history."
            )

        return self._make_recommendation(context, action, confidence, reasoning)
