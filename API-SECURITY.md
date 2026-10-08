# API Security and Rate Limiting

## What was added

- API-key authentication using the `X-API-Key` header.
- API key stored in the `API_SECURITY_KEY` environment variable.
- Public `/health` endpoint.
- Public `/` compatibility endpoint.
- Protected `/generate`, `/feedback`, and `/feedback/stats` endpoints.
- In-memory rate limiting: 10 requests/minute per client IP and endpoint.
- `401 Unauthorized` for missing or invalid API keys.
- `429 Too Many Requests` after the configured rate limit is exceeded.
- Security logs for rejected authentication and rate-limit events.
- API keys and request bodies are not written to logs.
- Automated tests for authentication and rate limiting.

## Setup

From the repository root:

```powershell
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set:

```env
OPENROUTER_API_KEY=your_real_openrouter_key
API_SECURITY_KEY=your_long_random_security_key
API_URL=http://127.0.0.1:8000
```

The real `.env` must remain uncommitted.

## Run the backend

```powershell
uvicorn backend.main:app --reload
```

Open:

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/docs`

## Run the frontend

In another terminal:

```powershell
streamlit run frontend/app.py
```

The frontend reads `API_SECURITY_KEY` from the local environment and sends it as:

```text
X-API-Key: <key>
```

## Test security

Run:

```powershell
python -m pytest tests/test_security.py -v
```

Expected security cases:

| Test | Expected |
|---|---|
| `/health` without key | `200` |
| `/generate` without key | `401` |
| `/generate` with wrong key | `401` |
| `/generate` with correct key | `200` |
| `/feedback` without key | `401` |
| `/feedback/stats` without key | `401` |
| 10 `/generate` calls | `200` |
| 11th `/generate` call within window | `429` |

## Manual curl tests

Health:

```powershell
curl.exe http://127.0.0.1:8000/health
```

Missing key:

```powershell
curl.exe -X POST http://127.0.0.1:8000/generate -H "Content-Type: application/json" -d "{\"prompt\":\"Hello\"}"
```

Valid key:

```powershell
curl.exe -X POST http://127.0.0.1:8000/generate -H "X-API-Key: YOUR_KEY" -H "Content-Type: application/json" -d "{\"prompt\":\"Hello\"}"
```

## Security flow

```text
Client
  |
  v
API Request
  |
  v
X-API-Key validation
  |
  +---- invalid/missing ----> 401
  |
  v
Rate-limit check
  |
  +---- limit exceeded -----> 429
  |
  v
FastAPI endpoint
  |
  v
AI/application logic
  |
  v
Response
```

## Rate-limit implementation

The limiter uses a fixed one-minute window and stores request timestamps in process memory.

The key is:

```text
(client IP, endpoint)
```

Therefore `/generate` and `/feedback` have independent counters for the same client.

This is intentionally a simple development/demo implementation.

## Limitations

This limiter is not production-grade:

- state is lost when the process restarts;
- multiple server workers have separate counters;
- multiple application instances do not share state;
- IP-based identification is not a substitute for user identity;
- no Redis/database coordination is used.

A distributed limiter such as Redis can be considered later if the application is deployed across multiple workers or instances.

## Environment variables

| Variable | Purpose |
|---|---|
| `OPENROUTER_API_KEY` | Existing OpenRouter provider credential |
| `API_SECURITY_KEY` | Client API authentication key |
| `API_URL` | Optional Streamlit-to-FastAPI URL |