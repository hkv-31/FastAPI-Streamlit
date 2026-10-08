import logging

from fastapi import APIRouter, Depends, HTTPException

from backend.feedback_models import FeedbackRequest, FeedbackResponse
from backend.feedback_store import add_feedback, get_stats
from rate_limiter import check_rate_limit
from security import require_api_key

logger = logging.getLogger("api_security")

router = APIRouter(prefix="/feedback", tags=["Feedback"])

_PROTECTED = [Depends(require_api_key), Depends(check_rate_limit)]


@router.post("", response_model=FeedbackResponse, dependencies=_PROTECTED)
def submit_feedback(request: FeedbackRequest):
    if request.rating not in {"positive", "negative"}:
        raise HTTPException(
            status_code=400,
            detail="Rating must be 'positive' or 'negative'",
        )

    add_feedback(
        request.prompt,
        request.response,
        request.rating,
        request.comment.strip(),
    )
    return {"message": "Feedback submitted successfully"}


@router.get("/stats", dependencies=_PROTECTED)
def feedback_stats():
    return get_stats()
