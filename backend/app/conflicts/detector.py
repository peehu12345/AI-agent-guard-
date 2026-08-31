"""
Conflict Detector — identifies when multiple agents target the same customer/transaction.
This is AgentGuard's KILLER DIFFERENTIATOR.
"""
from collections import defaultdict
from itertools import combinations


FINANCIAL_ACTIONS = {"RETRY_PAYMENT", "OFFER_INCENTIVE"}
COMM_ACTIONS = {"SEND_REMINDER", "SEND_MESSAGE"}


def detect_conflicts(recommendations: list[dict]) -> list[dict]:
    """
    Given a list of agent recommendations (potentially from multiple agents for the same customer),
    detect all conflicts.
    
    Returns a list of conflict dicts.
    """
    # Group recommendations by customer_id
    by_customer: dict[str, list[dict]] = defaultdict(list)
    for rec in recommendations:
        by_customer[rec["customer_id"]].append(rec)

    conflicts = []

    for customer_id, recs in by_customer.items():
        if len(recs) < 2:
            continue  # No conflict possible with a single recommendation

        # Collect basic info for conflict reporting
        agent_ids = [r["agent_id"] for r in recs]
        actions = [r["proposed_action"] for r in recs]
        transaction_id = recs[0].get("transaction_id")

        # Check each conflict type
        conflict_types = []

        # 1. DUPLICATE_ACTION: same action from 2+ agents
        action_counts = defaultdict(list)
        for r in recs:
            action_counts[r["proposed_action"]].append(r["agent_id"])
        duplicates = {a: agents for a, agents in action_counts.items() if len(agents) > 1}
        if duplicates:
            conflict_types.append("DUPLICATE_ACTION")

        # 2. COMPETING_FINANCIAL: multiple financial actions
        financial_recs = [r for r in recs if r["proposed_action"] in FINANCIAL_ACTIONS]
        if len(financial_recs) > 1:
            conflict_types.append("COMPETING_FINANCIAL")

        # 3. DUPLICATE_COMMUNICATION: multiple comm actions
        comm_recs = [r for r in recs if r["proposed_action"] in COMM_ACTIONS]
        if len(comm_recs) > 1:
            conflict_types.append("DUPLICATE_COMMUNICATION")

        # 4. PRIORITY_CLASH: escalate vs. non-escalate disagreement
        has_escalate = any(r["proposed_action"] == "ESCALATE_HUMAN" for r in recs)
        has_non_escalate = any(r["proposed_action"] not in {"ESCALATE_HUMAN", "STOP"} for r in recs)
        if has_escalate and has_non_escalate:
            conflict_types.append("PRIORITY_CLASH")

        if not conflict_types:
            continue  # No conflicts for this customer

        # Pick primary conflict type
        primary_type = conflict_types[0]

        conflicts.append({
            "customer_id": customer_id,
            "transaction_id": transaction_id,
            "conflicting_agent_ids": agent_ids,
            "conflicting_actions": actions,
            "conflict_type": primary_type,
            "conflict_types_all": conflict_types,
            "recommendations": recs,
        })

    return conflicts
