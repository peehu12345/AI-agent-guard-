import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class HumanReview(Base):
    __tablename__ = "human_reviews"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    decision_id: Mapped[str] = mapped_column(String, ForeignKey("decisions.id"), nullable=False)
    customer_id: Mapped[str] = mapped_column(String, ForeignKey("customers.customer_id"), nullable=False)
    transaction_id: Mapped[str] = mapped_column(String, ForeignKey("transactions.transaction_id"), nullable=False)
    review_reason: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="PENDING")  # PENDING, APPROVED, REJECTED, MODIFIED
    reviewer_action: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    reviewer_notes: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    modified_action: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
