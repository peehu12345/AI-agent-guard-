"""Dashboard analytics API — powers the main dashboard."""
from fastapi import APIRouter, Depends
from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import (
    Decision, AuditLog, Conflict, SimulationRun,
    AgentRecommendation, HumanReview, Transaction, Customer
)

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/dashboard")
async def get_dashboard(db: AsyncSession = Depends(get_db)):
    """Main dashboard KPIs and summary data."""

    # Total transactions
    txn_count = (await db.execute(select(func.count(Transaction.id)))).scalar() or 0

    # Total revenue at risk
    revenue_at_risk = (await db.execute(
        select(func.sum(Transaction.amount)).where(Transaction.status == "FAILED")
    )).scalar() or 0

    # Decision stats
    decisions_total = (await db.execute(select(func.count(Decision.id)))).scalar() or 0
    allowed = (await db.execute(
        select(func.count(Decision.id)).where(Decision.policy_decision == "ALLOW")
    )).scalar() or 0
    reviewed = (await db.execute(
        select(func.count(Decision.id)).where(Decision.policy_decision == "REVIEW")
    )).scalar() or 0
    stopped = (await db.execute(
        select(func.count(Decision.id)).where(Decision.policy_decision == "STOP")
    )).scalar() or 0

    # Recovery stats
    gross_recovered = (await db.execute(
        select(func.sum(Decision.recovered_amount)).where(Decision.execution_result == "SUCCESS")
    )).scalar() or 0

    # Conflict stats
    conflicts_total = (await db.execute(select(func.count(Conflict.id)))).scalar() or 0

    # Human reviews pending
    reviews_pending = (await db.execute(
        select(func.count(HumanReview.id)).where(HumanReview.status == "PENDING")
    )).scalar() or 0

    # Customers
    customer_count = (await db.execute(select(func.count(Customer.id)))).scalar() or 0

    return {
        "total_transactions": txn_count,
        "revenue_at_risk": float(revenue_at_risk),
        "decisions_total": decisions_total,
        "actions_allowed": allowed,
        "actions_reviewed": reviewed,
        "actions_stopped": stopped,
        "gross_recovered": float(gross_recovered),
        "conflicts_detected": conflicts_total,
        "reviews_pending": reviews_pending,
        "total_customers": customer_count,
        "policy_override_rate": round((stopped / decisions_total * 100) if decisions_total > 0 else 0, 1),
        "conflict_rate": round((conflicts_total / txn_count * 100) if txn_count > 0 else 0, 1),
    }


@router.get("/decision-breakdown")
async def get_decision_breakdown(db: AsyncSession = Depends(get_db)):
    """Decision breakdown for pie/donut chart."""
    result = await db.execute(
        select(
            Decision.policy_decision,
            func.count(Decision.id).label("count")
        ).group_by(Decision.policy_decision)
    )
    rows = result.all()
    return [{"name": row[0], "value": row[1]} for row in rows]


@router.get("/agent-performance")
async def get_agent_performance(db: AsyncSession = Depends(get_db)):
    """Per-agent recommendation counts and stats."""
    result = await db.execute(
        select(
            AgentRecommendation.agent_id,
            func.count(AgentRecommendation.id).label("total_recommendations"),
            func.avg(AgentRecommendation.confidence).label("avg_confidence"),
            func.sum(AgentRecommendation.estimated_recovery).label("total_estimated_recovery"),
        ).group_by(AgentRecommendation.agent_id)
    )
    rows = result.all()
    return [
        {
            "agent_id": row[0],
            "total_recommendations": row[1],
            "avg_confidence": round(float(row[2] or 0), 3),
            "total_estimated_recovery": float(row[3] or 0),
        }
        for row in rows
    ]


@router.get("/policy-triggers")
async def get_policy_triggers(db: AsyncSession = Depends(get_db)):
    """Aggregated policy trigger frequencies from decisions."""
    result = await db.execute(select(Decision.triggered_policies))
    rows = result.scalars().all()

    counter = {}
    for policies in rows:
        if policies:
            for p in policies:
                counter[p] = counter.get(p, 0) + 1

    return [{"policy": k, "count": v} for k, v in sorted(counter.items(), key=lambda x: -x[1])]


@router.get("/risk-distribution")
async def get_risk_distribution(db: AsyncSession = Depends(get_db)):
    """Risk level distribution across transactions."""
    result = await db.execute(
        select(
            Transaction.risk_level,
            func.count(Transaction.id).label("count")
        ).group_by(Transaction.risk_level)
    )
    rows = result.all()
    return [{"risk_level": row[0], "count": row[1]} for row in rows]


@router.get("/recent-activity")
async def get_recent_activity(db: AsyncSession = Depends(get_db)):
    """Recent audit log entries for the activity feed."""
    result = await db.execute(
        select(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .limit(50)
    )
    logs = result.scalars().all()
    return [
        {
            "id": log.id,
            "event_type": log.event_type,
            "transaction_id": log.transaction_id,
            "customer_id": log.customer_id,
            "agent_ids": log.agent_ids,
            "conflict_detected": log.conflict_detected,
            "ai_recommendation": log.ai_recommendation,
            "policy_decision": log.policy_decision,
            "final_action": log.final_action,
            "execution_result": log.execution_result,
            "amount": float(log.amount) if log.amount else None,
            "risk_level": log.risk_level,
            "reason": log.reason,
            "created_at": log.created_at.isoformat() if log.created_at else None,
        }
        for log in logs
    ]
