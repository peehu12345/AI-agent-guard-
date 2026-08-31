"""Decisions API — list all decisions with filtering."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database import get_db
from app.models import Decision

router = APIRouter(prefix="/api/decisions", tags=["Decisions"])


@router.get("")
async def list_decisions(
    policy_decision: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    offset: int = Query(0),
    db: AsyncSession = Depends(get_db),
):
    """List decisions with optional filtering by policy_decision."""
    query = select(Decision).order_by(Decision.created_at.desc())

    if policy_decision:
        query = query.where(Decision.policy_decision == policy_decision)

    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    decisions = result.scalars().all()

    return [
        {
            "id": d.id,
            "customer_id": d.customer_id,
            "transaction_id": d.transaction_id,
            "ai_recommended_action": d.ai_recommended_action,
            "ai_confidence": d.ai_confidence,
            "ai_risk_level": d.ai_risk_level,
            "ai_reasoning": d.ai_reasoning,
            "triggered_policies": d.triggered_policies,
            "policy_decision": d.policy_decision,
            "final_action": d.final_action,
            "human_review_required": d.human_review_required,
            "execution_status": d.execution_status,
            "execution_result": d.execution_result,
            "recovered_amount": float(d.recovered_amount) if d.recovered_amount else 0,
            "reason": d.reason,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        }
        for d in decisions
    ]
