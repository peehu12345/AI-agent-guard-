import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Numeric, DateTime, Float, Boolean, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Decision(Base):
    __tablename__ = "decisions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id: Mapped[str] = mapped_column(String, ForeignKey("customers.customer_id"), nullable=False)
    transaction_id: Mapped[str] = mapped_column(String, ForeignKey("transactions.transaction_id"), nullable=False)
    recommendation_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    conflict_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ai_recommended_action: Mapped[str] = mapped_column(String, nullable=False)
    ai_confidence: Mapped[float] = mapped_column(Float, default=0.5)
    ai_risk_level: Mapped[str] = mapped_column(String, default="MEDIUM")
    ai_reasoning: Mapped[str] = mapped_column(String, nullable=False)
    triggered_policies: Mapped[list] = mapped_column(JSON, default=list)
    policy_decision: Mapped[str] = mapped_column(String, nullable=False)  # ALLOW, REVIEW, STOP
    final_action: Mapped[str] = mapped_column(String, nullable=False)
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=False)
    execution_status: Mapped[str] = mapped_column(String, default="PENDING")
    execution_result: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    recovered_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)
    reason: Mapped[str] = mapped_column(String, nullable=False)
    simulation_run_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
