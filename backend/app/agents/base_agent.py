"""Base agent class for all AgentGuard simulated agents."""
from abc import ABC, abstractmethod
from typing import Optional


VALID_ACTIONS = ["RETRY_PAYMENT", "SEND_REMINDER", "SEND_MESSAGE", "OFFER_INCENTIVE", "ESCALATE_HUMAN", "STOP"]

ACTION_COSTS = {
    "RETRY_PAYMENT": 50.0,
    "SEND_REMINDER": 20.0,
    "SEND_MESSAGE": 30.0,
    "OFFER_INCENTIVE": None,  # 10% of amount — computed dynamically
    "ESCALATE_HUMAN": 200.0,
    "STOP": 0.0,
}


class BaseAgent(ABC):
    agent_id: str
    priority: int

    @abstractmethod
    def can_handle(self, context: dict) -> bool:
        """Returns True if this agent has jurisdiction over this transaction context."""

    @abstractmethod
    def generate_recommendation(self, context: dict) -> dict:
        """Generates a structured recommendation dict. Never executes anything."""

    def _estimate_recovery(self, amount: float, probability: float) -> float:
        return round(amount * probability, 2)

    def _estimate_cost(self, action: str, amount: float = 0.0) -> float:
        if action == "OFFER_INCENTIVE":
            return round(amount * 0.10, 2)
        return ACTION_COSTS.get(action, 100.0)

    def _make_recommendation(
        self,
        context: dict,
        action: str,
        confidence: float,
        reasoning: str,
    ) -> dict:
        amount = float(context.get("amount", 0))
        prob = float(context.get("recovery_probability", 0.5))
        return {
            "agent_id": self.agent_id,
            "transaction_id": context["transaction_id"],
            "customer_id": context["customer_id"],
            "proposed_action": action,
            "confidence": round(min(max(confidence, 0.0), 1.0), 3),
            "reasoning": reasoning,
            "estimated_recovery": self._estimate_recovery(amount, prob),
            "estimated_cost": self._estimate_cost(action, amount),
        }
