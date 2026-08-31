import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, DateTime, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    customer_id: Mapped[str] = mapped_column(String, ForeignKey("customers.customer_id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String, default="INR")
    status: Mapped[str] = mapped_column(String, default="FAILED")  # FAILED, PENDING, RECOVERED, STOPPED
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    recovery_probability: Mapped[float] = mapped_column(Float, default=0.5)
    intervention_cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)
    risk_level: Mapped[str] = mapped_column(String, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
