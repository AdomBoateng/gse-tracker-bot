# GSE Tracker Bot

An informative web application providing real-time Ghana Stock Exchange (GSE) market data, top gainers and losers, comprehensive stock listings, and market status information.

## 📊 Features

### Market Status
- Real-time market open/closed status with countdown timer
- Market hours: 10:00 AM - 3:00 PM GMT
- Time remaining until market closes or opens
- Live GSE Stock Index with performance metrics

### Top Performers
- Top gainers with company logos, price changes, and volumes
- Top losers with company logos, price changes, and volumes
- Interactive displays with hover effects and animations

### Comprehensive Stock Information
- Ultra-modern stock listing with full company details
- Live price, percentage change, and volume for all companies
- Search functionality to filter stocks
- Sortable columns for name, price, change, and volume
- Company images and logos

### Market Summary
- End-of-day market summary
- Top gainers and losers summary with volumes and prices
- Quick insights into market performance

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **API Client**: httpx
- **Caching**: cachetools
- **Testing**: PyTest

### Frontend
- **Framework**: Vue 3 + TypeScript
- **Routing**: Vue Router
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios

## 📁 Project Structure

```
gse-tracker/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   │   ├── v1/
│   │   │   │   └── stocks.py
│   │   ├── core/         # Configuration
│   │   ├── models/       # Pydantic models
│   │   └── services/     # Business logic
│   │       └── gse_service.py
│   ├── tests/            # Test suite
│   ├── requirements.txt
│   └── main.py
├── frontend/             # Vue 3 frontend
│   ├── src/
│   │   ├── views/        # Page components
│   │   │   └── Dashboard.vue
│   │   ├── App.vue
│   │   └── main.ts
│   ├── tests/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── .env.example
├── .gitignore
├── AGENTS.md
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ with pip
- Node.js 18+ with npm
- Access to GSE API (free, no API key required)

### Setup

1. **Clone and install dependencies**

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

2. **Configure environment**

```bash
# Backend
cp .env.example .env
# Edit .env with your preferences
```

3. **Run the application**

```bash
# Terminal 1: Start backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Start frontend
cd frontend
npm run dev
```

4. **Access the application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm run test:unit

# Linting
cd backend
ruff check .

cd frontend
npm run lint
```

## 🔧 API Endpoints

### GSE Market Data
- `GET /api/v1/gse/live` - Get all live prices
- `GET /api/v1/gse/live/{symbol}` - Get live price for specific stock
- `GET /api/v1/gse/equities` - Get all equities summary
- `GET /api/v1/gse/equities/{symbol}` - Get equity details

## 📝 Development

### Backend Development
```bash
# Run with auto-reload
uvicorn app.main:app --reload --port 8000

# Type checking
mypy --ignore-missing-imports app/

# Run tests
pytest tests/ -v --cov=app --cov-report=html
```

### Frontend Development
```bash
# Start dev server
npm run dev

# Build production
npm run build

# Preview production build
npm run preview
```

## 🚀 Deployment (Render, free tier)

A `render.yaml` blueprint at the repo root deploys two free services:

- **`gse-tracker-api`** — FastAPI backend (Python web service, root `backend/`), started with
  `gunicorn -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:$PORT`.
- **`gse-tracker-web`** — Vue frontend (static site, root `frontend/`) that **rewrites `/api/*`
  to the backend**, so the browser calls the API same-origin (no CORS needed).

### Deploy steps

1. Push this repo to GitHub.
2. In Render: **New → Blueprint**, point it at the repo. Render reads `render.yaml` and creates both services.
3. Service names become subdomains (`https://<name>.onrender.com`) and must be globally unique.
   If you rename either service, update the rewrite `destination` and `CORS_ORIGINS` in `render.yaml` to match.
4. First deploy builds both; the static site's `/api/*` rewrite targets the API service.

### Free-tier caveats

- Services **sleep after ~15 min idle** → 30–60s cold starts.
- **No persistent disk**: the SQLite DB (`gse_tracker.db`) holding composite history and cached
  news **resets on each deploy/restart**. Tables auto-create on startup, so the app still runs;
  for durable history, attach a paid disk or use an external Postgres.
- The news service scrapes public feeds on a schedule; the **first `/api/v1/news`** call after a
  cold start can be slow while it warms the cache.

### Local production run (without Render)

```bash
cd backend
pip install -r requirements.txt   # includes gunicorn
DEBUG=false CORS_ORIGINS="https://your-frontend.example" \
  gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 app.main:app
```

`CORS_ORIGINS` accepts either a comma-separated list or a JSON array.

## 📚 Configuration

### Backend (.env)
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi-3-mini
OLLAMA_TEMPERATURE=0.3

GSE_API_URL=https://dev.kwayisi.org/apis/gse

DEBUG=true
PORT=8000

# Production settings
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
GUNICORN_WORKERS=4
GUNICORN_TIMEOUT=120
```

`OLLAMA_*` settings are reserved for a planned AI-insights feature and are not used by any endpoint yet.

### Frontend
Edit `frontend/vite.config.ts` to configure proxy and other settings.

## ⚡ Performance

- **Async/Await**: All API endpoints use async/await with httpx.AsyncClient
- **Caching**: 5-minute in-memory cache for live market data, shared across requests
- **Worker System**: Gunicorn with multiple Uvicorn workers

No load testing has been performed against this app yet — treat any concurrency numbers you see elsewhere in this repo's history as aspirational, not measured.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- GSE API by [kwayisi.org](https://dev.kwayisi.org/apis/gse/)
- Powered by FastAPI and Vue.js
- Built for Ghana Stock Exchange investors
