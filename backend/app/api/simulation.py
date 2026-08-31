"""Simulation API — trigger and monitor simulations."""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import SimulationRun
from app.simulation.engine import SimulationEngine

router = APIRouter(prefix="/api/simulation", tags=["Simulation"])

# Track the currently running simulation
_running_simulation_id = None


@router.post("/run")
async def run_simulation(background_tasks: BackgroundTasks):
    """Start a new simulation run in the background."""
    global _running_simulation_id

    engine = SimulationEngine(seed=42, num_customers=20, num_transactions=40)

    async def _run():
        global _running_simulation_id
        try:
            run_id = await engine.run()
            _running_simulation_id = run_id
        except Exception as e:
            _running_simulation_id = None
            raise

    background_tasks.add_task(_run)
    return {"message": "Simulation started", "status": "RUNNING"}


@router.get("/status")
async def simulation_status(db: AsyncSession = Depends(get_db)):
    """Get the latest simulation run status."""
    result = await db.execute(
        select(SimulationRun).order_by(SimulationRun.started_at.desc()).limit(1)
    )
    sim = result.scalar_one_or_none()
    if not sim:
        return {"status": "NO_RUNS", "message": "No simulation has been run yet"}

    return {
        "id": sim.id,
        "status": sim.status,
        "total_events": sim.total_events,
        "processed_events": sim.processed_events,
        "conflicts_detected": sim.conflicts_detected,
        "conflicts_resolved": sim.conflicts_resolved,
        "actions_allowed": sim.actions_allowed,
        "actions_reviewed": sim.actions_reviewed,
        "actions_stopped": sim.actions_stopped,
        "revenue_at_risk": float(sim.revenue_at_risk),
        "gross_recovered": float(sim.gross_recovered),
        "recovery_cost": float(sim.recovery_cost),
        "net_recovered": float(sim.net_recovered),
        "unsafe_actions_blocked": sim.unsafe_actions_blocked,
        "human_escalations": sim.human_escalations,
        "started_at": sim.started_at.isoformat() if sim.started_at else None,
        "completed_at": sim.completed_at.isoformat() if sim.completed_at else None,
    }
