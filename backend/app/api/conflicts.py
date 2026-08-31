"""Conflicts API — list all conflicts."""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Conflict

router = APIRouter(prefix="/api/conflicts", tags=["Conflicts"])


@router.get("")
async def list_conflicts(db: AsyncSession = Depends(get_db)):
    """List all detected conflicts."""
    result = await db.execute(select(Conflict).order_by(Conflict.created_at.desc()))
    conflicts = result.scalars().all()

    return [
        {
            "id": c.id,
            "customer_id": c.customer_id,
            "transaction_id": c.transaction_id,
            "conflicting_agent_ids": c.conflicting_agent_ids,
            "conflicting_actions": c.conflicting_actions,
            "conflict_type": c.conflict_type,
            "resolution": c.resolution,
            "winning_agent_id": c.winning_agent_id,
            "winning_action": c.winning_action,
            "blocked_actions": c.blocked_actions,
            "resolution_reason": c.resolution_reason,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in conflicts
    ]
