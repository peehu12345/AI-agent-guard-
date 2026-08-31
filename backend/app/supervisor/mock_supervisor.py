"""
Mock AI Supervisor — deterministic fallback when Gemini API is unavailable.
Used for bulk simulation to avoid rate limits.
"""
from app.supervisor.schemas import SupervisorResponse


def mock_analyze(context: dict) -> SupervisorResponse:
    """
    Deterministic contextual reasoning without LLM.
    Mirrors what a well-prompted LLM would recommend.
    """
    retry_count = int(context.get("retry_count", 0))
    prob = float(context.get("recovery_probability", 0.5))
    amount = float(context.get("amount", 0))
    opt_out = context.get("customer_opt_out", False)
    intervention_cost = float(context.get("intervention_cost", 0))
    prev_payments = int(context.get("previous_successful_payments", 0))
    last_contact = float(context.get("last_contact_hours_ago", 9999))

    # Opt-out → stop immediately
    if opt_out:
        return SupervisorResponse(
            recommended_action="STOP",
            confidence=0.99,
            reason="Customer has opted out of all communications. No action permitted.",
            risk_level="LOW",
            requires_human_review=False,
        )

    # High-value transaction → human review
    if amount > 50000:
        return SupervisorResponse(
            recommended_action="ESCALATE_HUMAN",
            confidence=0.80,
            reason=f"High-value transaction (Rs. {amount:,.0f}) requires human authorization before action.",
            risk_level="HIGH",
            requires_human_review=True,
        )

    # Low recovery probability → stop
    if prob < 0.3:
        return SupervisorResponse(
            recommended_action="STOP",
            confidence=0.75,
            reason=f"Recovery probability is very low ({prob:.0%}). Action not cost-effective.",
            risk_level="MEDIUM",
            requires_human_review=False,
        )

    # Cost exceeds benefit
    expected_recovery = prob * amount
    if intervention_cost > expected_recovery:
        return SupervisorResponse(
            recommended_action="STOP",
            confidence=0.80,
            reason=(
                f"Intervention cost (Rs. {intervention_cost:,.0f}) exceeds "
                f"expected recovery (Rs. {expected_recovery:,.0f})."
            ),
            risk_level="MEDIUM",
            requires_human_review=False,
        )

    # Too many retries → escalate
    if retry_count >= 2:
        return SupervisorResponse(
            recommended_action="ESCALATE_HUMAN",
            confidence=0.60,
            reason=f"Payment has failed {retry_count} times. Automated recovery exhausted.",
            risk_level="HIGH",
            requires_human_review=True,
        )

    # Good candidate for retry
    if retry_count == 0 and prob > 0.7:
        return SupervisorResponse(
            recommended_action="RETRY_PAYMENT",
            confidence=0.85,
            reason=(
                f"First failure with high recovery probability ({prob:.0%}). "
                f"Customer has {prev_payments} prior successful payments. Immediate retry recommended."
            ),
            risk_level="LOW",
            requires_human_review=False,
        )

    if retry_count == 1 and prob > 0.5:
        return SupervisorResponse(
            recommended_action="RETRY_PAYMENT",
            confidence=0.70,
            reason=(
                f"Second attempt justified — recovery probability {prob:.0%} remains above threshold. "
                f"Customer history supports another retry."
            ),
            risk_level="MEDIUM",
            requires_human_review=False,
        )

    # Recently contacted → reminder might work
    if last_contact > 24 and prev_payments > 0:
        return SupervisorResponse(
            recommended_action="SEND_REMINDER",
            confidence=0.65,
            reason=(
                f"Customer hasn't been contacted in {last_contact:.0f}h. "
                f"Sending payment reminder with {prev_payments} prior successful payments on record."
            ),
            risk_level="LOW",
            requires_human_review=False,
        )

    # Default — gentle message
    return SupervisorResponse(
        recommended_action="SEND_MESSAGE",
        confidence=0.65,
        reason="Standard recovery message recommended based on customer context and transaction history.",
        risk_level="LOW",
        requires_human_review=False,
    )
