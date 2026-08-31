"""Agents API — list all registered agents."""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Agent

router = APIRouter(prefix="/api/agents", tags=["Agents"])


@router.get("")
async def list_agents(db: AsyncSession = Depends(get_db)):
    """List all registered agents."""
    result = await db.execute(select(Agent).order_by(Agent.priority))
    agents = result.scalars().all()

    return [
        {
            "id": a.id,
            "agent_id": a.agent_id,
            "display_name": a.display_name,
            "description": a.description,
            "priority": a.priority,
            "is_active": a.is_active,
        }
        for a in agents
    ]
