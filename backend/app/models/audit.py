import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Numeric, DateTime, Float, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    transaction_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    customer_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    agent_ids: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    conflict_detected: Mapped[bool] = mapped_column(Boolean, default=False)
    ai_recommendation: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ai_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    policy_decision: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    triggered_policies: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    final_action: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    execution_result: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    recovered_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    risk_level: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    extra_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    simulation_run_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
