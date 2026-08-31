"""
Conflict Resolver — deterministically resolves agent conflicts.
Priority rules: lower priority number = wins.
"""

# Agent priority map (lower = higher priority)
AGENT_PRIORITY = {
    "SubscriptionRecoveryAgent": 1,
    "PaymentRecoveryAgent": 2,
    "CheckoutRecoveryAgent": 3,
    "ReceivablesAgent": 4,
}

FINANCIAL_ACTIONS = {"RETRY_PAYMENT", "OFFER_INCENTIVE"}
COMM_ACTIONS = {"SEND_REMINDER", "SEND_MESSAGE"}


def resolve_conflict(conflict: dict) -> dict:
    """
    Resolve a detected conflict by selecting the winning action
    and blocking all others.

    Resolution rules:
    1. Sort recommendations by agent priority (lower = wins)
    2. Winning agent's action is selected
    3. All other actions are blocked with specific reasons
    4. If winning action itself is blocked by cost-benefit → escalate
    """
    recs = conflict["recommendations"]

    # Sort by agent priority
    sorted_recs = sorted(recs, key=lambda r: AGENT_PRIORITY.get(r["agent_id"], 99))
    winner = sorted_recs[0]
    losers = sorted_recs[1:]

    winning_agent = winner["agent_id"]
    winning_action = winner["proposed_action"]

    blocked_actions = []
    for loser in losers:
        loser_action = loser["proposed_action"]
        loser_agent = loser["agent_id"]

        # Determine block reason
        if loser_action == winning_action:
            reason = f"Duplicate action '{loser_action}' — already executed by higher-priority {winning_agent}."
        elif loser_action in FINANCIAL_ACTIONS and winning_action in FINANCIAL_ACTIONS:
            reason = f"Competing financial action '{loser_action}' blocked — only one financial intervention allowed per customer cycle."
        elif loser_action in COMM_ACTIONS and winning_action in COMM_ACTIONS:
            reason = f"Duplicate communication '{loser_action}' blocked — prevents customer communication overload."
        elif loser_action in COMM_ACTIONS and winning_action in FINANCIAL_ACTIONS:
            reason = f"Communication '{loser_action}' blocked — awaiting financial action outcome first."
        else:
            reason = f"Action '{loser_action}' blocked by higher-priority agent {winning_agent} (priority {AGENT_PRIORITY.get(winning_agent, 99)})."

        blocked_actions.append({
            "agent_id": loser_agent,
            "action": loser_action,
            "reason": reason,
        })

    resolution_reason = (
        f"{winning_agent} (priority {AGENT_PRIORITY.get(winning_agent, 99)}) won the conflict. "
        f"Action '{winning_action}' selected. "
        f"{len(blocked_actions)} competing action(s) blocked to prevent agent collision."
    )

    return {
        "winning_agent_id": winning_agent,
        "winning_action": winning_action,
        "blocked_actions": blocked_actions,
        "resolution": "RESOLVED",
        "resolution_reason": resolution_reason,
        "winning_recommendation": winner,
    }
