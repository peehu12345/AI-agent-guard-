import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Boolean, Numeric, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    customer_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)
    opt_out: Mapped[bool] = mapped_column(Boolean, default=False)
    previous_successful_payments: Mapped[int] = mapped_column(Integer, default=0)
    last_contact_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
