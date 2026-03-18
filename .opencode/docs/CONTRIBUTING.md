# Contributing to GSE Tracker Bot

Thank you for your interest in contributing! This document outlines the process for contributing to GSE Tracker Bot.

## 📋 Table of Contents

- [Development Workflow](#development-workflow)
- [Branch Naming](#branch-naming)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Testing](#testing)
- [Questions](#questions)

## 🔄 Development Workflow

1. **Fork** the repo and clone your fork
2. **Create a branch** from `dev` (see Branch Naming below)
3. **Make your changes** following the Code Style guidelines
4. **Test your changes** (see Testing guidelines)
5. **Update documentation** if needed
6. **Open a Pull Request** to the `dev` branch

## 🌿 Branch Naming

Use descriptive branch names with prefixes:

- `feature/` - New features
  - `feature/add-chat-history`
  - `feature/user-authentication`

- `fix/` - Bug fixes
  - `fix/portfolio-calculation`
  - `fix/api-timeout`

- `docs/` - Documentation changes
  - `docs/update-readme`
  - `docs/add-api-reference`

- `refactor/` - Code refactoring
  - `refactor/database-session`
  - `refactor/frontend-components`

- `test/` - Test additions or modifications
  - `test/add-gse-service-tests`

- `chore/` - Maintenance tasks
  - `chore/update-dependencies`
  - `chore/clean-up-cache`

## 📝 Commit Messages

Use **Conventional Commits** format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, semicolons, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

### Examples

```
feat(portfolio): add profit/loss calculation
fix(stocks): handle missing market data gracefully
docs(README): update installation instructions
refactor(db): improve session management
test(gse): add live price tests
```

### Multi-line Commits

For complex changes:

```
feat(chat): integrate AI-powered insights

- Add conversation history storage
- Implement streaming responses
- Support multiple AI models via Ollama

Closes #23
```

## 🔄 Pull Request Process

1. **Update the README.md** if you added/changed features
2. **Update the CHANGELOG.md** with your changes
3. **All tests must pass** (see Testing guidelines)
4. **Code review** by at least one maintainer
5. **Squash commits** if requested
6. **Merge** to `dev` branch by maintainer

### PR Template

```markdown
## Summary

Brief summary of changes

## Related Issue

Fixes #<issue-number>

## Changes

- Change 1
- Change 2

## Testing

How you tested the changes

## Screenshots

If applicable
```

## 💻 Code Style

### Python (Backend)

Follow PEP 8 with **ruff**:

```bash
cd backend
ruff check .           # Lint
ruff check . --fix     # Auto-fix
ruff format .          # Format
```

**Key rules:**
- Max line length: 88 chars
- Use absolute imports: `from app.db.session import SessionLocal`
- Type hints for all functions: `def get_stock(symbol: str) -> StockModel:`
- Use f-strings: `f"Error: {error}"`
- Use `async`/`await` for all HTTP calls

### TypeScript/Vue (Frontend)

```bash
cd frontend
npm run lint      # ESLint
npm run format    # Prettier
```

**Key rules:**
- Use Vue 3 Composition API with `<script setup lang="ts">`
- Use `ref()` for primitives, `reactive()` for objects
- Use kebab-case for CSS classes: `.portfolio-container`
- Max line length: 100 chars
- Use absolute imports: `import { ref } from 'vue'`

## ✅ Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v                  # Run all tests
pytest tests/test_api.py -v       # Run API tests
pytest tests/ -k "test_example"   # Run specific test
pytest tests/ --cov=app           # With coverage
```

### Frontend Tests

```bash
cd frontend
npm run test:unit                 # Run unit tests
npm run test:unit -- --coverage   # With coverage
```

### Run Both

```bash
# Backend
cd backend && pytest tests/ -v

# Frontend
cd frontend && npm run test:unit
```

## ❓ Questions?

- Open an issue for bugs or feature requests
- Check existing issues before starting new work
- Ask in PR comments for clarity

---

**Thank you for contributing! 🎉**
