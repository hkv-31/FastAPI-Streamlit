# FastAPI + Streamlit Demo: AI Text Assistant

A small end-to-end Generative AI application that combines a **FastAPI backend** with a **Streamlit frontend**. The application accepts a user's text prompt in the Streamlit UI, sends it to the FastAPI API through an HTTP POST request, forwards the prompt to an LLM through OpenRouter, and displays the generated response back in the Streamlit interface.

## Project Overview

This project demonstrates how an AI application can be separated into two layers:

- **FastAPI backend**- exposes the `/generate` API endpoint, validates requests with Pydantic, calls the LLM through OpenRouter, and returns a JSON response.
- **Streamlit frontend**- provides a simple interactive UI where users enter a prompt and view the AI-generated response.

### Architecture

```text
User
  ↓
Streamlit UI
  ↓
HTTP POST /generate
  ↓
FastAPI Backend
  ↓
OpenRouter API
  ↓
Free LLM
  ↓
JSON Response
  ↓
Streamlit UI
```

## Features

- FastAPI REST API
- Pydantic request and response models
- `POST /generate` endpoint
- Automatic interactive API documentation through `/docs`
- OpenRouter LLM integration
- Streamlit text input interface
- HTTP communication between Streamlit and FastAPI
- Empty-input validation
- Backend connection/error handling
- JSON-based API response

## Project Structure

```text
fastapi-streamlit-demo/
├── backend/
│   └── main.py
├── frontend/
│   └── app.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Pydantic
- Streamlit
- Requests
- OpenAI Python SDK
- OpenRouter API
- Free LLM model from OpenRouter

## Setup

### 1. Create and activate a virtual environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the OpenRouter API key

Create a `.env` file in the project root:

```text
OPENROUTER_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your own OpenRouter API key.

**Do not commit `.env` or your API key to GitHub.**

## Running the Backend

Open a terminal in the project root and run:

```bash
uvicorn backend.main:app --reload
```

The FastAPI server will run at:

```text
http://127.0.0.1:8000
```

### FastAPI API Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

The Swagger UI allows you to test the API directly.

## API Endpoint

### `POST /generate`

Request:

```json
{
  "prompt": "What is RAG in AI?"
}
```

Response:

```json
{
  "response": "RAG stands for Retrieval-Augmented Generation..."
}
```

The exact response depends on the selected LLM.

## Running the Streamlit UI

Keep the FastAPI terminal running.

Open a second terminal and run:

```bash
streamlit run frontend/app.py
```

The Streamlit application will normally be available at:

```text
http://localhost:8501
```

Enter a question in the text area and click **Generate**.

## Testing

The application was tested at three levels:

### 1. FastAPI health check

```text
GET /
```

Expected response:

```json
{
  "message": "FastAPI backend is running"
}
```

### 2. FastAPI + OpenRouter

The `/generate` endpoint was tested using Swagger UI with a text prompt. The backend successfully sent the request to OpenRouter and returned the model response.

### 3. Streamlit + FastAPI + OpenRouter

The Streamlit interface was tested by entering a question and clicking **Generate**. The UI successfully communicated with the FastAPI backend and displayed the generated AI response.

The project testing screenshots document the FastAPI server, running Streamlit UI, AI testing through OpenRouter, and AI testing from the Streamlit interface.

## Error Handling

The backend checks for empty prompts and returns an appropriate HTTP error.

The Streamlit frontend also handles:

- Empty user input
- Failed HTTP requests
- FastAPI backend being unavailable
- Server-side errors returned by the API

## Security

The OpenRouter API key is stored in `.env` instead of being hard-coded into the application.

Recommended `.gitignore` entries:

```text
.env
.venv/
__pycache__/
```

Never push your API key to a public repository.

## Feedback Loop

The application includes a feedback module that allows users to provide feedback on AI-generated responses.

### Feedback Features

- Users can rate an AI response as **positive** or **negative**.
- Users can optionally provide additional comments.
- Feedback is stored in `feedback.json` along with the prompt, response, rating, comment, and timestamp.
- The `/feedback/stats` endpoint provides basic feedback statistics such as total, positive, and negative feedback.
- The Streamlit frontend sends submitted feedback to the FastAPI backend through the `/feedback` API endpoint.

This feedback can be used to understand user satisfaction and identify areas for improving the AI application.