import logging
import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel

from backend.feedback_routes import router as feedback_router
from rate_limiter import check_rate_limit
from security import require_api_key

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_api")

app = FastAPI(title="AI Text Assistant API")
app.include_router(feedback_router)


class GenerateRequest(BaseModel):
    prompt: str


class GenerateResponse(BaseModel):
    response: str


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set in the .env file")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

MODEL = "dots-studio/dots-3-note-preview:free"


@app.get("/")
def root():
    """Public compatibility endpoint."""
    return {"message": "FastAPI backend is running"}


@app.get("/health")
def health():
    """Public health endpoint for monitoring."""
    return {"status": "healthy"}


@app.post(
    "/generate",
    response_model=GenerateResponse,
    dependencies=[Depends(require_api_key), Depends(check_rate_limit)],
)
def generate(request: GenerateRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. Give clear and concise answers.",
                },
                {"role": "user", "content": request.prompt},
            ],
            temperature=0.3,
        )
        answer = response.choices[0].message.content
        return {"response": answer}
    except Exception:
        logger.exception("LLM request failed")
        raise HTTPException(status_code=500, detail="AI service request failed")
