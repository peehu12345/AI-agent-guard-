from app.agents.base_agent import BaseAgent


class CheckoutRecoveryAgent(BaseAgent):
    agent_id = "CheckoutRecoveryAgent"
    priority = 3

    def can_handle(self, context: dict) -> bool:
        # Handles first-time checkout failures
        return context.get("status", "FAILED") == "FAILED" and context.get("retry_count", 0) == 0

    def generate_recommendation(self, context: dict) -> dict:
        amount = float(context.get("amount", 0))
        prob = context.get("recovery_probability", 0.5)
        confidence = 0.65

        if amount > 10000 and prob < 0.6:
            # High value, low probability — offer incentive to win back
            action = "OFFER_INCENTIVE"
            incentive = amount * 0.10
            reasoning = (
                f"High-value checkout abandonment (Rs. {amount:,.0f}). "
                f"Recovery probability is low ({prob:.0%}). "
                f"Offering Rs. {incentive:,.0f} (10%) incentive to complete purchase."
            )
        else:
            action = "SEND_MESSAGE"
            reasoning = (
                f"Checkout failed for Rs. {amount:,.0f}. Sending recovery message with "
                f"direct payment link. Recovery probability: {prob:.0%}."
            )

        return self._make_recommendation(context, action, confidence, reasoning)
