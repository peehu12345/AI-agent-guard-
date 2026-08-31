from app.agents.subscription_recovery import SubscriptionRecoveryAgent
from app.agents.payment_recovery import PaymentRecoveryAgent
from app.agents.checkout_recovery import CheckoutRecoveryAgent
from app.agents.receivables import ReceivablesAgent
from app.agents.base_agent import BaseAgent

ALL_AGENTS: list[BaseAgent] = [
    SubscriptionRecoveryAgent(),
    PaymentRecoveryAgent(),
    CheckoutRecoveryAgent(),
    ReceivablesAgent(),
]

__all__ = ["ALL_AGENTS", "BaseAgent"]
