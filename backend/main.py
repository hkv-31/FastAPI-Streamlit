from fastapi import FastAPI
from pydantic import BaseModel
from feedback_routes import router as feedback_router
from openai import OpenAI
from dotenv import load_dotenv
import os

app = FastAPI(title="AI Text Assistant API")
app.include_router(feedback_router)

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    response: str

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set in the .env file")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

MODEL = "dots-studio/dots-3-note-preview:free"


class GenerateRequest(BaseModel):
    prompt: str


class GenerateResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {"message": "FastAPI backend is running"}


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. Give clear and concise answers."
                },
                {
                    "role": "user",
                    "content": request.prompt
                }
            ],
            temperature=0.3
        )
        answer = response.choices[0].message.content
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/")
def root():
    return {"message": "FastAPI backend is running"}

@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    return {"response": f"You asked: {request.prompt}"}
