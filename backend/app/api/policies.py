"""Policies API — list and toggle policies."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Policy

router = APIRouter(prefix="/api/policies", tags=["Policies"])


@router.get("")
async def list_policies(db: AsyncSession = Depends(get_db)):
    """List all policies."""
    result = await db.execute(select(Policy).order_by(Policy.rule_type, Policy.name))
    policies = result.scalars().all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "rule_type": p.rule_type,
            "parameter_key": p.parameter_key,
            "parameter_value": p.parameter_value,
            "action_on_trigger": p.action_on_trigger,
            "is_active": p.is_active,
        }
        for p in policies
    ]


@router.patch("/{policy_id}/toggle")
async def toggle_policy(policy_id: str, db: AsyncSession = Depends(get_db)):
    """Toggle a policy's active status."""
    policy = await db.get(Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    policy.is_active = not policy.is_active
    await db.commit()

    return {"id": policy.id, "name": policy.name, "is_active": policy.is_active}
