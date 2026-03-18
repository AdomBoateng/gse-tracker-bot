# Project Agents Reference

This file provides AI agents and developers with project-specific commands, style guidelines, and best practices.

---

## AI Agents

| # | Agent | Model | Temperature | Skills |
|---|---|---|-|
| 1 | Orchestrator | deepseek-r1:1.5b | 0.2 | orchestrator, task-planner |
| 2 | Task Planner | deepseek-r1:1.5b | 0.1 | task-planner |
| 3 | AI Architect | qwen3-coder-next | 0.2 | ai-architect, self-hosted-ai-stack |
| 4 | Backend Dev | qwen3-coder-next | 0.3 | backend-development, database-architect, backend-optimization |
| 5 | Frontend Dev | qwen3-coder-next | 0.3 | frontend-development |
| 6 | RAG Engineer | qwen3-coder-next | 0.2 | rag-engineering, rag-optimization, vector-database-tuning |
| 7 | Prompt Engineer | qwen3-coder-next | 0.2 | prompt-engineering, prompt-optimization, llm-guardrails |
| 8 | ML Engineer | qwen3-coder-next | 0.2 | ml-engineering, ml-evaluation |
| 9 | Data Engineer | qwen3-coder-next | 0.2 | data-engineering, data-cleaning, data-validation |
| 10 | DevOps | deepseek-r1:1.5b | 0.2 | devops, containerization, cicd-pipelines, infrastructure-monitoring |
| 11 | Tester | deepseek-r1:1.5b | 0.2 | testing, automated-testing |
| 12 | Reviewer | qwen3-coder-next | 0.1 | code-review, security-auditing |
| 13 | Debugger | deepseek-r1:1.5b | 0.2 | debugging |
| 14 | Docs Writer | qwen3:latest | 0.1 | documentation |
| 15 | PR Generator | deepseek-r1:1.5b | 0.1 | pr-generation, github-publisher |
| 16 | Evaluator | deepseek-r1:1.5b | 0.1 | evaluator |
| 17 | Hallucination Detector | deepseek-r1:1.5b | 0 | hallucination-detection |
| 18 | Cost Optimizer | deepseek-r1:1.5b | 0.1 | cost-optimization |

---

## Backend Commands

### Install
```bash
cd backend && pip install -r requirements.txt
```

### Run
```bash
cd backend && uvicorn app.main:app --reload --port 8000
```

### Test (Single)
```bash
pytest tests/test_api.py::test_root -v
pytest tests/test_api.py::test_health -v
pytest tests/test_gse_service.py -v
pytest tests/ -k "test_example" -v
```

### All Tests
```bash
pytest tests/ -v --tb=short
```

### Lint
```bash
cd backend && ruff check . && ruff check . --fix
```

### Format
```bash
cd backend && ruff format .
```

---

## Frontend Commands

### Install
```bash
cd frontend && npm install
```

### Run
```bash
cd frontend && npm run dev
```

### Build
```bash
cd frontend && npm run build
```

### Preview Build
```bash
cd frontend && npm run preview
```

### Test
```bash
cd frontend && npm run test:unit
```

### Lint & Fix
```bash
cd frontend && npm run lint -- --fix
```

### Format
```bash
cd frontend && npx prettier --write src/
```

---

## Python Style Guide

### Imports
- Use absolute imports: `from app.db.session import SessionLocal`
- Group: stdlib → third-party → local; sort alphabetically within groups
- Example: `from app.services.gse_service import gse_service`

### Types
- Python 3.10+ syntax: `list[T]`, `dict[K, V]`, `Optional[T]`
- Annotate ALL function parameters and return types
- Use Pydantic models for data validation
- Use `@cached` decorator for cached functions with TTLCache

### Naming
- Classes: `PascalCase` (e.g., `GSEService`, `AIService`)
- Functions: `snake_case` (e.g., `get_live_data`)
- Variables: `snake_case` (e.g., `api_client`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `BACKEND_DIR`)

### Error Handling
- Catch specific exceptions (e.g., `httpx.HTTPError`, `json.JSONDecodeError`)
- Use `HTTPException` for API errors with status codes and descriptive messages
- Log errors with context using `print()` for service layers
- In API endpoints, use FastAPI's `HTTPException`

### Formatting
- PEP 8 compliant with ruff (max 88 chars)
- Use f-strings: `f"Error: {error_msg}"`
- Import types from `typing`: `Optional`, `Dict`, `List`, `Any`
- Use async/await for all HTTP calls with httpx

### Database
- SQLAlchemy ORM for all DB operations
- Use dependency injection for sessions
- Close sessions in `finally` blocks or use context managers
- Auto-generated migrations via Alembic (when needed)

### Caching
- Use `cachetools.TTLCache` for data caching
- Cache TTL: 300 seconds (5 minutes) for GSE data
- Use `@cached` decorator with cache object

---

## TypeScript/Vue Style Guide

### Imports
- Absolute imports: `import { ref } from 'vue'`
- Group: vue, vue-router, pinia, other libraries; sort alphabetically within groups
- Example: `import { ref, computed, onMounted } from 'vue'`

### Types
- Use `interface` for object shapes, `type` for union types
- Enable strict TypeScript mode in `tsconfig.json`
- Annotate ALL function parameters and return types
- Use `MaybeRef<T>` for reactive values where applicable

### Naming
- Components: `PascalCase` (e.g., `Dashboard.vue`)
- Composables: `useXxx` (e.g., `usePortfolioStore`)
- Methods: `camelCase` (e.g., `fetchHoldings`)
- Data properties: `camelCase` (e.g., `portfolioStats`)
- CSS classes: `kebab-case` (e.g., `.portfolio-container`)

### Vue 3
- Use Composition API with `<script setup lang="ts">`
- Prefer `ref()` over `reactive()` for primitives
- Use `defineProps()` and `defineEmits()` for component interfaces
- Use `computed()` for derived state
- Import lifecycle hooks: `onMounted`, `onUnmounted`

### Styling
- Use Tailwind CSS utility classes
- Prefer utility classes over custom CSS
- Group utility classes logically
- Use gradient classes from `from-` to `-to-` format

### Error Handling
- Catch HTTP errors with try/catch blocks
- Display user-friendly messages (e.g., `alert()` or toast notifications)
- Handle network errors gracefully
- Log errors with `console.error()`

### Testing
- Use Vitest for unit testing
- Use Vue Test Utils for component testing
- Mock API calls with `vi.mock()`
- Test edge cases: empty lists, null values, error states

---

## AI-Specific Guidelines

### Ollama/LM Integration
- Local Ollama server configured via `backend/.env`
- Default model: `phi4-mini:latest`
- API endpoint: `http://localhost:11434/api/chat`
- Response format: `result["message"]["content"]` (dict with "message" key)
- Use `httpx.AsyncClient()` for non-blocking AI calls
- Set appropriate timeout for AI responses (default: 180.0s)

### Prompt Engineering
- Always include clear, specific instructions
- Provide sufficient context in the prompt
- Validate AI output before returning to user
- Include fallback responses for errors
- Cache repeated queries where appropriate

### Hallucination Prevention
- Use factual context from real APIs (GSE, not hypothetical data)
- Flag uncertain predictions with disclaimers
- Include disclaimers for financial advice: "Not financial advice"
- Verify critical information against live data
- Log AI responses for review

### System Prompt Structure
- Define role and purpose clearly
- List capabilities and limitations
- Include real-time data integration instructions
- Add guidelines for response formatting
- Include disclaimers and safety notes

---

## File Organization

### Backend Structure
```
backend/
├── app/
│   ├── api/v1/          # FastAPI routers (stocks.py)
│   ├── core/            # Core configuration (config.py)
│   ├── models/          # Pydantic models
│   ├── services/        # Business logic (gse_service.py)
│   ├── db/              # Database session & CRUD operations
│   └── main.py          # FastAPI app entry point
├── tests/               # Test suite
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables
```

### Frontend Structure
```
frontend/
├── src/
│   ├── views/           # Page components (Dashboard.vue)
│   ├── components/      # Reusable components
│   ├── stores/          # Pinia state management
│   ├── services/        # API service layer
│   ├── assets/          # Static assets
│   └── main.ts          # Vue app entry point
├── tests/               # Vitest test files
├── vite.config.ts       # Vite configuration
├── package.json         # NPM dependencies
└── tsconfig.json        # TypeScript configuration
```

---

## Development Workflow

1. Ensure Ollama is running: `ollama list`
2. Pull required models: `ollama pull phi4-mini:latest`
3. Start backend: `cd backend && uvicorn app.main:app --reload --port 8000`
4. Start frontend: `cd frontend && npm run dev`
5. Access UI: http://localhost:5173
6. API docs: http://localhost:8000/docs
7. Test backend: `cd backend && pytest tests/ -v`
8. Lint backend: `cd backend && ruff check .`
9. Lint frontend: `cd frontend && npm run lint`
