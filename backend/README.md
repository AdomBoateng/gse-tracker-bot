# GSE Portfolio Tracker - Backend

This is the backend API service for the Ghana Stock Exchange Portfolio Tracker.

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
- `GET /api/v1/portfolio/holdings` - Get all holdings
- `POST /api/v1/portfolio/holdings` - Add holding
- `PUT /api/v1/portfolio/holdings/{id}` - Update holding
- `DELETE /api/v1/portfolio/holdings/{id}` - Delete holding
- `GET /api/v1/portfolio/stats` - Portfolio statistics
- `POST /api/v1/ai/chat` - AI chat with portfolio insights

## Configuration

Copy `.env.example` to `.env` and configure:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi-3-mini
GSE_API_URL=https://dev.kwayisi.org/apis/gse
DATABASE_URL=sqlite:///./gse_tracker.db
DEBUG=true
PORT=8000
```

Relative SQLite paths are resolved from the `backend` directory.

## Project Structure

```
backend/
├── app/
│   ├── api/       # API routes
│   ├── core/      # Configuration
│   ├── models/    # Pydantic & SQLAlchemy models
│   ├── services/  # Business logic
│   └── db/        # Database layer
├── tests/         # Test suite
└── main.py        # FastAPI app
```
