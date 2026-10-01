from pydantic import BaseModel, Field

class FeedbackRequest(BaseModel):
    prompt: str = Field(min_length=1)
    response: str = Field(min_length=1)
    rating: str
    comment: str = ""

class FeedbackResponse(BaseModel):
    message: str
