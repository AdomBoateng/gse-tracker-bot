# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-13

### Added
- **Core Functionality**
  - Real-time Ghana Stock Exchange (GSE) market data integration
  - Portfolio management with holdings tracking
  - AI-powered portfolio assistant via Ollama
  - Portfolio statistics and performance metrics

- **Backend (FastAPI)**
  - REST API endpoints for stocks and portfolio
  - GSE API client with caching
  - Portfolio service with calculations
  - SQLite database with SQLAlchemy ORM
  - Pydantic models for data validation
  - TTL caching for API responses

- **Frontend (Vue 3)**
  - Dashboard view with portfolio overview
  - Chat interface for AI assistant
  - Real-time data updates
  - Responsive design with Tailwind CSS
  - State management with Pinia

- **AI Integration**
  - 18 specialized AI agents via Qwen3-Coder-Next
  - Orchestrator agent for workflow coordination
  - Local Ollama integration
  - AI chat service with conversation history

- **Testing**
  - Backend test suite with pytest
  - Frontend unit tests with Vitest
  - API endpoint tests
  - Service layer tests

- **Documentation**
  - Professional README with setup instructions
  - Project architecture documentation
  - Contributing guidelines
  - API endpoint documentation

- **Development Tools**
  - Environment configuration (.env.example)
  - Ruff linting and formatting
  - ESLint and Prettier for frontend
  - TypeScript configuration

### Technical Details
- Backend: Python 3.10+, FastAPI, SQLAlchemy, Pydantic, httpx, cachetools
- Frontend: Vue 3, TypeScript, Pinia, Tailwind CSS, Vite
- Database: SQLite with Alembic migration support
- AI: Ollama with multiple model support
- Testing: pytest, Vitest

### Known Limitations
- No user authentication (planned for v0.2.0)
- SQLite database only ( PostgreSQL for production)
- No WebSocket for real-time updates (planned for v0.3.0)

### Breaking Changes
None

### Deprecations
None

---

## [Unreleased] - Planned Features

### Planned for v0.2.0
- User authentication and authorization
- PostgreSQL database support
- Docker containerization
- Enhanced AI agent system

### Planned for v0.3.0
- Real-time updates via WebSocket
- Chart.js integration for data visualization
- Portfolio optimization suggestions
- Export functionality (CSV, PDF)

### Planned for v1.0.0
- Production-ready infrastructure
- CI/CD pipeline
- Comprehensive documentation
- Performance optimization
