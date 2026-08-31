import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Conflict(Base):
    __tablename__ = "conflicts"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id: Mapped[str] = mapped_column(String, ForeignKey("customers.customer_id"), nullable=False)
    transaction_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("transactions.transaction_id"), nullable=True)
    conflicting_agent_ids: Mapped[list] = mapped_column(JSON, default=list)
    conflicting_actions: Mapped[list] = mapped_column(JSON, default=list)
    conflict_type: Mapped[str] = mapped_column(String, nullable=False)
    resolution: Mapped[str] = mapped_column(String, default="RESOLVED")
    winning_agent_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    winning_action: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    blocked_actions: Mapped[list] = mapped_column(JSON, default=list)
    resolution_reason: Mapped[str] = mapped_column(String, nullable=False)
    simulation_run_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
