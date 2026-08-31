import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Numeric, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class AgentRecommendation(Base):
    __tablename__ = "agent_recommendations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id: Mapped[str] = mapped_column(String, ForeignKey("agents.agent_id"), nullable=False)
    transaction_id: Mapped[str] = mapped_column(String, ForeignKey("transactions.transaction_id"), nullable=False)
    customer_id: Mapped[str] = mapped_column(String, ForeignKey("customers.customer_id"), nullable=False)
    proposed_action: Mapped[str] = mapped_column(String, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    reasoning: Mapped[str] = mapped_column(String, nullable=False)
    estimated_recovery: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)
    estimated_cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)
    simulation_run_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("simulation_runs.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
