"""Human Reviews API — list and process reviews."""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database import get_db
from app.models import HumanReview, Decision

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])


class ReviewAction(BaseModel):
    action: str  # APPROVE, REJECT, MODIFY
    notes: Optional[str] = None
    modified_action: Optional[str] = None


@router.get("")
async def list_reviews(db: AsyncSession = Depends(get_db)):
    """List all human reviews."""
    result = await db.execute(select(HumanReview).order_by(HumanReview.created_at.desc()))
    reviews = result.scalars().all()

    return [
        {
            "id": r.id,
            "decision_id": r.decision_id,
            "customer_id": r.customer_id,
            "transaction_id": r.transaction_id,
            "review_reason": r.review_reason,
            "status": r.status,
            "reviewer_action": r.reviewer_action,
            "reviewer_notes": r.reviewer_notes,
            "modified_action": r.modified_action,
            "reviewed_at": r.reviewed_at.isoformat() if r.reviewed_at else None,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in reviews
    ]


@router.post("/{review_id}/action")
async def process_review(
    review_id: str,
    body: ReviewAction,
    db: AsyncSession = Depends(get_db),
):
    """Process a human review (approve/reject/modify)."""
    review = await db.get(HumanReview, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review.status = body.action.upper() + "D" if body.action != "MODIFY" else "MODIFIED"
    review.reviewer_action = body.action
    review.reviewer_notes = body.notes
    review.modified_action = body.modified_action
    review.reviewed_at = datetime.utcnow()

    # Update the parent decision
    decision = await db.get(Decision, review.decision_id)
    if decision:
        if body.action == "APPROVE":
            decision.execution_status = "EXECUTED"
            decision.execution_result = "SUCCESS"
        elif body.action == "REJECT":
            decision.execution_status = "BLOCKED"
            decision.execution_result = "SKIPPED"
            decision.final_action = "STOP"
        elif body.action == "MODIFY":
            decision.final_action = body.modified_action or decision.final_action
            decision.execution_status = "EXECUTED"
            decision.execution_result = "SUCCESS"

    await db.commit()

    return {"message": f"Review {body.action}d successfully", "review_id": review_id}
