"""
Deterministic Policy Engine — Final Authority.
The LLM recommends. The Policy Engine decides.
"""
from dataclasses import dataclass, field


@dataclass
class PolicyDecision:
    decision: str  # ALLOW, REVIEW, STOP
    reason: str
    triggered_policies: list = field(default_factory=list)
    risk_level: str = "LOW"
    overrides_ai: bool = False


def _get_policy_value(policies: list, name: str, default: str) -> str:
    """Get a policy's parameter_value by name from the policy list."""
    for p in policies:
        if p.get("name") == name and p.get("is_active", True):
            return p.get("parameter_value", default)
    return default


class PolicyEngine:
    """
    Central policy engine with deterministic, ordered rule evaluation.
    Hard rules run first and cannot be overridden by AI recommendations.
    Soft rules trigger human review.
    """

    def evaluate(self, context: dict, ai_recommendation: dict, db_policies: list) -> PolicyDecision:
        action = ai_recommendation.get("recommended_action", "STOP")
        confidence = float(ai_recommendation.get("confidence", 0.5))
        amount = float(context.get("amount", 0))
        retry_count = int(context.get("retry_count", 0))
        prob = float(context.get("recovery_probability", 0.5))
        intervention_cost = float(context.get("intervention_cost", 0))

        # ────────────────────────────────────────────────
        # HARD RULES — run first, cannot be bypassed
        # ────────────────────────────────────────────────

        # Rule 1: Customer opted out → STOP everything
        if context.get("customer_opt_out", False):
            return PolicyDecision(
                decision="STOP",
                reason="Customer has opted out of all communications.",
                triggered_policies=["CUSTOMER_OPT_OUT"],
                risk_level="LOW",
                overrides_ai=True,
            )

        # Rule 2: Max retry limit
        max_retries = int(_get_policy_value(db_policies, "MAX_RETRY_LIMIT", "2"))
        if action == "RETRY_PAYMENT" and retry_count >= max_retries:
            return PolicyDecision(
                decision="STOP",
                reason=f"Payment retry limit of {max_retries} has been reached (current: {retry_count}).",
                triggered_policies=["MAX_RETRY_LIMIT"],
                risk_level="MEDIUM",
                overrides_ai=True,
            )

        # Rule 3: Unsafe / unknown action
        unsafe_actions = ["UNKNOWN", "HACK", "BYPASS", "FORCE"]
        if action in unsafe_actions:
            return PolicyDecision(
                decision="STOP",
                reason=f"Action '{action}' is not a recognized safe action.",
                triggered_policies=["UNSAFE_ACTION_BLOCK"],
                risk_level="CRITICAL",
                overrides_ai=True,
            )

        # Rule 4: Duplicate communication — contacted within N hours
        comm_actions = ["SEND_REMINDER", "SEND_MESSAGE"]
        if action in comm_actions:
            freq_hours = float(_get_policy_value(db_policies, "CONTACT_FREQUENCY_LIMIT", "24"))
            last_contact_hours = float(context.get("last_contact_hours_ago", 9999))
            if last_contact_hours < freq_hours:
                return PolicyDecision(
                    decision="STOP",
                    reason=(
                        f"Customer was contacted {last_contact_hours:.0f}h ago "
                        f"(minimum gap: {freq_hours:.0f}h). Blocking duplicate communication."
                    ),
                    triggered_policies=["CONTACT_FREQUENCY_LIMIT"],
                    risk_level="LOW",
                    overrides_ai=True,
                )

        # Rule 5: Cost-benefit analysis for OFFER_INCENTIVE
        if action == "OFFER_INCENTIVE":
            incentive_cost = amount * 0.10
            total_cost = intervention_cost + incentive_cost
            expected_recovery = prob * amount
            if total_cost > expected_recovery:
                return PolicyDecision(
                    decision="STOP",
                    reason=(
                        f"Intervention cost (Rs. {total_cost:,.0f}) exceeds "
                        f"expected recovery (Rs. {expected_recovery:,.0f}). "
                        f"Action not financially justified."
                    ),
                    triggered_policies=["COST_BENEFIT_ANALYSIS"],
                    risk_level="MEDIUM",
                    overrides_ai=True,
                )

        # ────────────────────────────────────────────────
        # SOFT RULES — trigger REVIEW (human oversight)
        # ────────────────────────────────────────────────
        triggered = []

        # Soft Rule 1: High-value transaction
        high_value = float(_get_policy_value(db_policies, "HIGH_VALUE_TRANSACTION", "50000"))
        if amount > high_value:
            triggered.append("HIGH_VALUE_TRANSACTION")

        # Soft Rule 2: Low AI confidence
        min_conf = float(_get_policy_value(db_policies, "LOW_AI_CONFIDENCE", "0.5"))
        if confidence < min_conf:
            triggered.append("LOW_AI_CONFIDENCE")

        # Soft Rule 3: Unresolved conflict escalation
        if context.get("conflict_detected") and context.get("conflict_unresolved"):
            triggered.append("AGENT_CONFLICT_ESCALATION")

        if triggered:
            risk = "HIGH" if "HIGH_VALUE_TRANSACTION" in triggered else "MEDIUM"
            return PolicyDecision(
                decision="REVIEW",
                reason=f"Human review required due to: {', '.join(triggered)}.",
                triggered_policies=triggered,
                risk_level=risk,
                overrides_ai=False,
            )

        # ────────────────────────────────────────────────
        # ALL CHECKS PASSED → ALLOW
        # ────────────────────────────────────────────────
        return PolicyDecision(
            decision="ALLOW",
            reason="All policy checks passed. Action approved for execution.",
            triggered_policies=[],
            risk_level="LOW",
            overrides_ai=False,
        )
