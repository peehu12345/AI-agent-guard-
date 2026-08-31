import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Numeric, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status: Mapped[str] = mapped_column(String, default="RUNNING")  # RUNNING, COMPLETED, FAILED
    total_events: Mapped[int] = mapped_column(Integer, default=0)
    processed_events: Mapped[int] = mapped_column(Integer, default=0)
    conflicts_detected: Mapped[int] = mapped_column(Integer, default=0)
    conflicts_resolved: Mapped[int] = mapped_column(Integer, default=0)
    actions_allowed: Mapped[int] = mapped_column(Integer, default=0)
    actions_reviewed: Mapped[int] = mapped_column(Integer, default=0)
    actions_stopped: Mapped[int] = mapped_column(Integer, default=0)
    revenue_at_risk: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)
    gross_recovered: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)
    recovery_cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)
    net_recovered: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)
    unsafe_actions_blocked: Mapped[int] = mapped_column(Integer, default=0)
    human_escalations: Mapped[int] = mapped_column(Integer, default=0)
    seed: Mapped[int] = mapped_column(Integer, default=42)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
