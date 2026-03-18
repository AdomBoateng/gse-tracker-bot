# GSE Tracker Bot - Architecture

## Overview

GSE Tracker Bot is a full-stack web application for tracking Ghana Stock Exchange investments. It features a FastAPI backend with SQLite database, Vue 3 frontend, and integrated AI insights via Ollama.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                              Frontend                               │
│                    (Vue 3 + TypeScript + Pinia)                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │ Dashboard   │  │   Chat UI   │  │ Portfolio   │  │  Market     │ │
│  │   View      │  │  (AI Chat)  │  │   Views     │  │  Data       │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │
└────────────────────┬────────────────────────────────────────────────┘
                     │ HTTP/REST API (port 8000)
                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                              Backend                                │
│                     (FastAPI + Python 3.10+)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  Routers    │  │  Services   │  │   Models    │  │   Database  │ │
│  │ (API Endpts)│  │ (Business  │  │ (Pydantic/ │  │ (SQLite/    │ │
│  │             │  │  Logic)    │  │ SQLAlchemy)│  │  Alembic)   │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │
│  │   GSE API   │  │   AI        │  │   Cache     │                  │
│  │   Client    │  │  Service    │  │  (TTL)      │                  │
│  └─────────────┘  └─────────────┘  └─────────────┘                  │
└────────────────────┬────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                              AI Layer                               │
│                      (Ollama Local LLM)                             │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  18 Specialized AI Agents via Qwen3-Coder-Next               │ │
│  │  - Orchestrator, Task Planner, AI Architect                  │ │
│  │  - Backend Dev, Frontend Dev, RAG Engineer                   │ │
│  │  - Prompt Engineer, ML Engineer, Data Engineer               │ │
│  │  - DevOps, Tester, Reviewer, Debugger                        │ │
│  │  - Docs Writer, PR Generator, Evaluator                      │ │
│  │  - Hallucination Detector, Cost Optimizer                    │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Details

### Backend Components

#### API Layer
- **Routers** (`app/api/v1/`): REST endpoints for stocks, portfolio, and chat
- **FastAPI**: Async web framework with automatic OpenAPI docs

#### Service Layer
- **GSE Service** (`gse_service.py`): Fetches live stock data from GSE API
- **Portfolio Service** (`portfolio_service.py`): Manages holdings, calculations, and analytics
- **AI Service** (`ai_service.py`): Integrates with Ollama for conversational AI

#### Data Layer
- **SQLAlchemy ORM**: Database abstraction with session management
- **Pydantic Models**: Data validation and serialization
- **SQLite Database**: Light-weight persistence with Alembic migrations

#### Core Components
- **Config** (`core/config.py`): Environment-based configuration
- **Cached Functions**: TTLCache with 300s expiry for API responses

### Frontend Components

#### UI Layer
- **Views** (`src/views/`): Dashboard and Chat pages
- **Components**: Reusable Vue 3 components
- **Pinia Stores**: State management for portfolio and market data

#### Service Layer
- **API Service**: HTTP client for backend communication
- **Auth**: Token-based authentication (not implemented in v0.1.0)

#### Tooling
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first styling
- **Vitest**: Unit testing framework

### Data Flow

```
User Request
    │
    ▼
Frontend (Vue)
    │ HTTP Request
    ▼
Backend (FastAPI)
    ├─→ GSEService → GSE API → Live Prices
    ├─→ PortfolioService → DB → Holdings Data
    └─→ AIService → Ollama → AI Responses
    │
    ▼
Response with JSON
    ▼
Frontend updates reactive state
    ▼
UI renders new data
```

## AI Agent System

The project includes 18 specialized agents coordinated by the Orchestrator:

| Agent | Purpose | Model |
|-------|---------|-------|
| Orchestrator | Coordinates workflows | deepseek-r1:1.5b |
| Task Planner | Breaks tasks into steps | deepseek-r1:1.5b |
| AI Architect | Designs system architecture | qwen3-coder-next |
| Backend Dev | Backend implementation | qwen3-coder-next |
| Frontend Dev | Frontend implementation | qwen3-coder-next |
| RAG Engineer | Knowledge retrieval pipelines | qwen3-coder-next |
| Prompt Engineer | Prompt optimization | qwen3-coder-next |
| ML Engineer | Machine learning models | qwen3-coder-next |
| Data Engineer | Data pipelines | qwen3-coder-next |
| DevOps | Deployment & infra | deepseek-r1:1.5b |
| Tester | Test execution | deepseek-r1:1.5b |
| Reviewer | Code quality review | qwen3-coder-next |
| Debugger | Issue resolution | deepseek-r1:1.5b |
| Docs Writer | Documentation | qwen3:latest |
| PR Generator | PR creation | deepseek-r1:1.5b |
| Evaluator | Output evaluation | deepseek-r1:1.5b |
| Hallucination Detector | Fact verification | deepseek-r1:1.5b |
| Cost Optimizer | Token optimization | deepseek-r1:1.5b |

## Technology Stack

### Backend
- **FastAPI**: Modern async web framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation
- **cachetools**: Caching with TTL
- **httpx**: Async HTTP client
- **pytest**: Testing framework
- **ruff**: Linting and formatting

### Frontend
- **Vue 3**: UI framework
- **TypeScript**: Type-safe JavaScript
- **Pinia**: State management
- **Tailwind CSS**: Utility-first styling
- **Vite**: Build tool
- **Vitest**: Testing framework

### AI/ML
- **Ollama**: Local LLM runtime
- **Qwen3-Coder-Next**: Primary model for AI agents
- **deepseek-r1:1.5b**: Secondary model for orchestration

### Database
- **SQLite**: Development database
- **Alembic**: Schema migrations

## Deployment Architecture

```
Development Environment
    │
    ├─→ Frontend: npm run dev (localhost:5173)
    ├─→ Backend: uvicorn app.main:app (localhost:8000)
    └─→ AI: ollama serve (localhost:11434)

Production (Planned)
    │
    ├─→ Frontend: Static files via Nginx
    ├─→ Backend: Docker container via PM2
    └─→ AI: Dedicated Ollama instance
```

## Security Considerations

- Environment variables for sensitive config (`.env` not tracked)
- No authentication in v0.1.0 ( planned for future)
- Local Ollama for data privacy (no external LLM API calls)
- SQLite for simplicity (no SQL injection via ORM)

## Performance Considerations

- Caching with 300s TTL for GSE API responses
- Async/await for non-blocking HTTP calls
- SQLite connection pooling
- Vue 3 reactivity for efficient UI updates

## Future Enhancements

- PostgreSQL database for production
- OAuth2 authentication
- WebSocket for real-time updates
- Chart.js for data visualization
- Docker containerization
- CI/CD pipeline with GitHub Actions
