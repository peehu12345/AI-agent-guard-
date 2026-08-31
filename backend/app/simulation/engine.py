"""
Simulation Engine — Orchestrates the full AgentGuard pipeline.
Generates synthetic data → agents propose → conflicts detected → AI supervises → policy decides → audit logged.
"""
import logging
import random
import uuid
from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import async_session_factory
from app.models import (
    Customer, Transaction, Agent, AgentRecommendation,
    Conflict, Policy, Decision, HumanReview, AuditLog, SimulationRun
)
from app.agents import ALL_AGENTS
from app.conflicts.detector import detect_conflicts
from app.conflicts.resolver import resolve_conflict
from app.supervisor.mock_supervisor import mock_analyze
from app.policies.engine import PolicyEngine
from app.simulation.data_generator import generate_customers, generate_transactions

logger = logging.getLogger(__name__)


class SimulationEngine:
    """
    Full pipeline simulation engine.
    Generates synthetic customers + transactions, runs agents, detects conflicts,
    supervises with AI, applies policies, and logs everything.
    """

    def __init__(self, seed: int = 42, num_customers: int = 20, num_transactions: int = 40):
        self.seed = seed
        self.num_customers = num_customers
        self.num_transactions = num_transactions
        self.rng = random.Random(seed)
        self.policy_engine = PolicyEngine()

    async def run(self) -> str:
        """Execute the full simulation pipeline. Returns the simulation_run_id."""
        async with async_session_factory() as session:
            # Create simulation run record
            run_id = str(uuid.uuid4())
            sim_run = SimulationRun(
                id=run_id,
                status="RUNNING",
                seed=self.seed,
                started_at=datetime.utcnow(),
            )
            session.add(sim_run)
            await session.commit()

            try:
                await self._execute_pipeline(session, run_id)
                # Update simulation run status
                sim_run.status = "COMPLETED"
                sim_run.completed_at = datetime.utcnow()
                await session.commit()
                logger.info(f"Simulation {run_id} completed successfully")
            except Exception as e:
                sim_run.status = "FAILED"
                sim_run.completed_at = datetime.utcnow()
                await session.commit()
                logger.error(f"Simulation {run_id} failed: {e}")
                raise

            return run_id

    async def _execute_pipeline(self, session: AsyncSession, run_id: str):
        """The core simulation pipeline."""
        # Load default policies
        result = await session.execute(select(Policy))
        policies_orm = result.scalars().all()
        db_policies = [
            {"name": p.name, "parameter_value": p.parameter_value, "is_active": p.is_active}
            for p in policies_orm
        ]

        # Step 1: Generate synthetic data
        logger.info("Step 1: Generating synthetic data...")
        customers_data = generate_customers(self.num_customers, self.rng)
        transactions_data = generate_transactions(customers_data, self.num_transactions, self.rng)

        # Build a lookup map
        customer_map = {}
        for cd in customers_data:
            c = Customer(**cd)
            session.add(c)
            customer_map[cd["customer_id"]] = cd

        for td in transactions_data:
            t = Transaction(**td)
            session.add(t)

        await session.commit()

        # Update sim stats
        sim_run = await session.get(SimulationRun, run_id)
        sim_run.total_events = len(transactions_data)
        total_at_risk = sum(float(t["amount"]) for t in transactions_data)
        sim_run.revenue_at_risk = Decimal(str(round(total_at_risk, 2)))
        await session.commit()

        # Step 2: Each agent proposes actions for each transaction
        logger.info("Step 2: Agents generating recommendations...")
        all_recommendations = []

        for txn in transactions_data:
            cust = customer_map.get(txn["customer_id"], {})
            context = {
                "transaction_id": txn["transaction_id"],
                "customer_id": txn["customer_id"],
                "amount": float(txn["amount"]),
                "status": txn["status"],
                "retry_count": txn["retry_count"],
                "recovery_probability": txn["recovery_probability"],
                "intervention_cost": float(txn["intervention_cost"]),
                "risk_level": txn["risk_level"],
                "customer_opt_out": cust.get("opt_out", False),
                "previous_successful_payments": cust.get("previous_successful_payments", 0),
                "last_contact_hours_ago": (
                    (datetime.utcnow() - cust["last_contact_at"]).total_seconds() / 3600
                    if cust.get("last_contact_at")
                    else 9999
                ),
            }

            for agent in ALL_AGENTS:
                if agent.can_handle(context):
                    rec = agent.generate_recommendation(context)
                    rec["_context"] = context  # stash for later use
                    all_recommendations.append(rec)

                    # Save to DB
                    db_rec = AgentRecommendation(
                        id=str(uuid.uuid4()),
                        agent_id=rec["agent_id"],
                        transaction_id=rec["transaction_id"],
                        customer_id=rec["customer_id"],
                        proposed_action=rec["proposed_action"],
                        confidence=rec["confidence"],
                        reasoning=rec["reasoning"],
                        estimated_recovery=Decimal(str(rec["estimated_recovery"])),
                        estimated_cost=Decimal(str(rec["estimated_cost"])),
                        simulation_run_id=run_id,
                    )
                    session.add(db_rec)

        await session.commit()

        # Step 3: Detect conflicts
        logger.info("Step 3: Detecting conflicts...")
        conflicts = detect_conflicts(all_recommendations)

        # Track which transactions had conflicts resolved
        resolved_txns = {}  # transaction_id -> winning recommendation

        for conflict_data in conflicts:
            resolution = resolve_conflict(conflict_data)

            db_conflict = Conflict(
                id=str(uuid.uuid4()),
                customer_id=conflict_data["customer_id"],
                transaction_id=conflict_data.get("transaction_id"),
                conflicting_agent_ids=conflict_data["conflicting_agent_ids"],
                conflicting_actions=conflict_data["conflicting_actions"],
                conflict_type=conflict_data["conflict_type"],
                resolution=resolution["resolution"],
                winning_agent_id=resolution["winning_agent_id"],
                winning_action=resolution["winning_action"],
                blocked_actions=resolution["blocked_actions"],
                resolution_reason=resolution["resolution_reason"],
                simulation_run_id=run_id,
            )
            session.add(db_conflict)

            txn_id = conflict_data.get("transaction_id")
            if txn_id:
                resolved_txns[txn_id] = resolution["winning_recommendation"]

            # Audit log for conflict
            session.add(AuditLog(
                id=str(uuid.uuid4()),
                event_type="CONFLICT",
                transaction_id=txn_id,
                customer_id=conflict_data["customer_id"],
                agent_ids=conflict_data["conflicting_agent_ids"],
                conflict_detected=True,
                reason=resolution["resolution_reason"],
                simulation_run_id=run_id,
            ))

        await session.commit()

        # Update conflict stats
        sim_run = await session.get(SimulationRun, run_id)
        sim_run.conflicts_detected = len(conflicts)
        sim_run.conflicts_resolved = len([c for c in conflicts])
        await session.commit()

        # Step 4: For each transaction, run AI supervisor + policy engine
        logger.info("Step 4: AI Supervisor + Policy Engine decisions...")

        stats = {
            "allowed": 0, "reviewed": 0, "stopped": 0,
            "gross_recovered": 0.0, "recovery_cost": 0.0,
            "unsafe_blocked": 0, "human_escalations": 0,
        }

        processed_txns = set()
        for rec in all_recommendations:
            txn_id = rec["transaction_id"]
            if txn_id in processed_txns:
                continue  # Already handled via conflict resolution
            processed_txns.add(txn_id)

            context = rec["_context"]

            # Use conflict winner if this txn had a conflict
            if txn_id in resolved_txns:
                winning_rec = resolved_txns[txn_id]
                context["conflict_detected"] = True
                context["conflict_unresolved"] = False
            else:
                winning_rec = rec

            # AI Supervisor analysis (mock for simulation speed)
            ai_result = mock_analyze(context)

            ai_recommendation = {
                "recommended_action": ai_result.recommended_action,
                "confidence": ai_result.confidence,
                "reason": ai_result.reason,
                "risk_level": ai_result.risk_level,
            }

            # Policy Engine — FINAL AUTHORITY
            policy_result = self.policy_engine.evaluate(context, ai_recommendation, db_policies)

            # Determine final action
            if policy_result.decision == "STOP":
                final_action = "STOP"
                execution_status = "BLOCKED"
                execution_result = "SKIPPED"
                recovered = 0.0
                stats["stopped"] += 1
                if policy_result.overrides_ai:
                    stats["unsafe_blocked"] += 1
            elif policy_result.decision == "REVIEW":
                final_action = ai_result.recommended_action
                execution_status = "AWAITING_REVIEW"
                execution_result = None
                recovered = 0.0
                stats["reviewed"] += 1
                stats["human_escalations"] += 1
            else:  # ALLOW
                final_action = ai_result.recommended_action
                execution_status = "EXECUTED"
                prob = float(context.get("recovery_probability", 0.5))
                amount = float(context.get("amount", 0))
                # Simulate execution outcome
                success = self.rng.random() < prob
                if success and final_action != "STOP":
                    recovered = round(amount * self.rng.uniform(0.7, 1.0), 2)
                    execution_result = "SUCCESS"
                else:
                    recovered = 0.0
                    execution_result = "FAILURE"
                stats["allowed"] += 1
                stats["gross_recovered"] += recovered
                cost = float(winning_rec.get("estimated_cost", 0))
                stats["recovery_cost"] += cost

            # Save decision
            decision_id = str(uuid.uuid4())
            db_decision = Decision(
                id=decision_id,
                customer_id=context["customer_id"],
                transaction_id=txn_id,
                ai_recommended_action=ai_result.recommended_action,
                ai_confidence=ai_result.confidence,
                ai_risk_level=ai_result.risk_level,
                ai_reasoning=ai_result.reason,
                triggered_policies=policy_result.triggered_policies,
                policy_decision=policy_result.decision,
                final_action=final_action,
                human_review_required=(policy_result.decision == "REVIEW"),
                execution_status=execution_status,
                execution_result=execution_result,
                recovered_amount=Decimal(str(recovered)),
                reason=policy_result.reason,
                simulation_run_id=run_id,
            )
            session.add(db_decision)

            # Create human review if needed
            if policy_result.decision == "REVIEW":
                session.add(HumanReview(
                    id=str(uuid.uuid4()),
                    decision_id=decision_id,
                    customer_id=context["customer_id"],
                    transaction_id=txn_id,
                    review_reason=policy_result.reason,
                    status="PENDING",
                ))

            # Audit log
            session.add(AuditLog(
                id=str(uuid.uuid4()),
                event_type="DECISION",
                transaction_id=txn_id,
                customer_id=context["customer_id"],
                agent_ids=[winning_rec["agent_id"]],
                conflict_detected=(txn_id in resolved_txns),
                ai_recommendation=ai_result.recommended_action,
                ai_confidence=ai_result.confidence,
                policy_decision=policy_result.decision,
                triggered_policies=policy_result.triggered_policies,
                final_action=final_action,
                execution_result=execution_result,
                recovered_amount=Decimal(str(recovered)),
                amount=Decimal(str(context.get("amount", 0))),
                risk_level=context.get("risk_level", "MEDIUM"),
                reason=policy_result.reason,
                simulation_run_id=run_id,
            ))

        await session.commit()

        # Final stats update
        sim_run = await session.get(SimulationRun, run_id)
        sim_run.processed_events = len(processed_txns)
        sim_run.actions_allowed = stats["allowed"]
        sim_run.actions_reviewed = stats["reviewed"]
        sim_run.actions_stopped = stats["stopped"]
        sim_run.gross_recovered = Decimal(str(round(stats["gross_recovered"], 2)))
        sim_run.recovery_cost = Decimal(str(round(stats["recovery_cost"], 2)))
        sim_run.net_recovered = Decimal(str(round(stats["gross_recovered"] - stats["recovery_cost"], 2)))
        sim_run.unsafe_actions_blocked = stats["unsafe_blocked"]
        sim_run.human_escalations = stats["human_escalations"]
        await session.commit()

        logger.info(f"Pipeline complete: {len(processed_txns)} transactions processed, "
                     f"{stats['allowed']} allowed, {stats['reviewed']} reviewed, {stats['stopped']} stopped")
