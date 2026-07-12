# GSE Tracker - Backend

This is the backend API service for the Ghana Stock Exchange Tracker.

## Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Development Server
```bash
uvicorn app.main:app --reload --port 8000
```

### Run Tests
```bash
pytest tests/ -v
```

### Lint & Format
```bash
ruff check . && ruff format .
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/v1/gse/live` - Live market data
- `GET /api/v1/gse/live/{symbol}` - Live price for stock
- `GET /api/v1/gse/equities` - All equities
- `GET /api/v1/gse/equities/{symbol}` - Stock details

## Configuration

Copy `.env.example` to `.env` and configure:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi-3-mini
GSE_API_URL=https://dev.kwayisi.org/apis/gse
DEBUG=true
PORT=8000
```

The `OLLAMA_*` settings are reserved for a planned AI-insights feature and are not currently used by any endpoint.

## Project Structure

```
backend/
├── app/
│   ├── api/       # API routes
│   ├── core/      # Configuration
│   ├── models/    # Pydantic models
│   └── services/  # Business logic (GSE API client + caching)
├── tests/         # Test suite
└── main.py        # FastAPI app
```
