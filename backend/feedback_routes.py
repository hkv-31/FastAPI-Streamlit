from fastapi import APIRouter, HTTPException
from feedback_models import FeedbackRequest, FeedbackResponse
from feedback_store import add_feedback, get_stats

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("", response_model=FeedbackResponse)
def submit_feedback(request: FeedbackRequest):
    if request.rating not in {"positive", "negative"}:
        raise HTTPException(status_code=400, detail="Rating must be 'positive' or 'negative'")
    add_feedback(request.prompt, request.response, request.rating, request.comment.strip())
    return {"message": "Feedback submitted successfully"}

@router.get("/stats")
def feedback_stats():
    return get_stats()
