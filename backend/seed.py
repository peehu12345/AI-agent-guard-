"""
Seed script — populates the database with 4 agents, default policies,
and runs an initial simulation.
"""
import asyncio
import uuid
from datetime import datetime

from app.database import create_tables, async_session_factory
from app.models import Agent, Policy
from app.simulation.engine import SimulationEngine


AGENTS = [
    {
        "agent_id": "SubscriptionRecoveryAgent",
        "display_name": "Subscription Recovery Agent",
        "description": "Recovers failed subscription payments using retry and reminder strategies. Prioritizes customers with proven payment history.",
        "priority": 1,
    },
    {
        "agent_id": "PaymentRecoveryAgent",
        "display_name": "Payment Recovery Agent",
        "description": "Handles general payment failures under Rs. 1,00,000. Uses progressive escalation from retry to message to human review.",
        "priority": 2,
    },
    {
        "agent_id": "CheckoutRecoveryAgent",
        "display_name": "Checkout Recovery Agent",
        "description": "Targets first-time checkout failures with recovery messages and incentives for high-value abandonments.",
        "priority": 3,
    },
    {
        "agent_id": "ReceivablesAgent",
        "display_name": "Receivables Agent",
        "description": "Manages high-value (>Rs. 25,000) or high-risk receivables. Escalates critical cases to human review for financial protection.",
        "priority": 4,
    },
]

POLICIES = [
    {
        "name": "MAX_RETRY_LIMIT",
        "description": "Maximum number of payment retries allowed before blocking further retry attempts.",
        "rule_type": "HARD",
        "parameter_key": "max_retries",
        "parameter_value": "2",
        "action_on_trigger": "STOP",
    },
    {
        "name": "CUSTOMER_OPT_OUT",
        "description": "Blocks all actions for customers who have opted out of communications.",
        "rule_type": "HARD",
        "parameter_key": "opt_out",
        "parameter_value": "true",
        "action_on_trigger": "STOP",
    },
    {
        "name": "CONTACT_FREQUENCY_LIMIT",
        "description": "Minimum hours between customer contacts to prevent communication overload.",
        "rule_type": "HARD",
        "parameter_key": "min_hours",
        "parameter_value": "24",
        "action_on_trigger": "STOP",
    },
    {
        "name": "UNSAFE_ACTION_BLOCK",
        "description": "Blocks any unrecognized or unsafe actions proposed by agents.",
        "rule_type": "HARD",
        "parameter_key": "unsafe_actions",
        "parameter_value": "UNKNOWN,HACK,BYPASS,FORCE",
        "action_on_trigger": "STOP",
    },
    {
        "name": "COST_BENEFIT_ANALYSIS",
        "description": "Blocks actions where intervention cost exceeds expected recovery amount.",
        "rule_type": "HARD",
        "parameter_key": "cost_threshold",
        "parameter_value": "1.0",
        "action_on_trigger": "STOP",
    },
    {
        "name": "HIGH_VALUE_TRANSACTION",
        "description": "Requires human review for transactions above the threshold amount.",
        "rule_type": "SOFT",
        "parameter_key": "threshold",
        "parameter_value": "50000",
        "action_on_trigger": "REVIEW",
    },
    {
        "name": "LOW_AI_CONFIDENCE",
        "description": "Requires human review when AI confidence is below the minimum threshold.",
        "rule_type": "SOFT",
        "parameter_key": "min_confidence",
        "parameter_value": "0.5",
        "action_on_trigger": "REVIEW",
    },
    {
        "name": "AGENT_CONFLICT_ESCALATION",
        "description": "Escalates to human review when unresolved conflicts exist between agents.",
        "rule_type": "SOFT",
        "parameter_key": "escalate",
        "parameter_value": "true",
        "action_on_trigger": "REVIEW",
    },
]


async def seed():
    print("[AgentGuard Seed Script]")
    print("=" * 50)

    # Create tables
    print("Creating database tables...")
    await create_tables()

    async with async_session_factory() as session:
        # Seed agents
        print("Seeding agents...")
        for agent_data in AGENTS:
            agent = Agent(id=str(uuid.uuid4()), **agent_data)
            session.add(agent)
            print(f"   [Agent] {agent_data['display_name']} (priority {agent_data['priority']})")

        # Seed policies
        print("Seeding policies...")
        for policy_data in POLICIES:
            policy = Policy(
                id=str(uuid.uuid4()),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                **policy_data,
            )
            session.add(policy)
            print(f"   [Policy] {policy_data['name']} ({policy_data['rule_type']})")

        await session.commit()

    # Run initial simulation
    print("\nRunning initial simulation...")
    engine = SimulationEngine(seed=42, num_customers=20, num_transactions=40)
    run_id = await engine.run()
    print(f"   Simulation completed: {run_id}")

    print("\nSeed complete! AgentGuard is ready.")
    print("   Run the server with: uvicorn app.main:app --reload")


if __name__ == "__main__":
    asyncio.run(seed())
