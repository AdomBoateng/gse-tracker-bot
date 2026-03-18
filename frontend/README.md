# GSE Portfolio Tracker - Frontend

This is the Vue 3 frontend application for the Ghana Stock Exchange Portfolio Tracker.

## Quick Start

### Install Dependencies
```bash
npm install
```

### Run Development Server
```bash
npm run dev
```

### Build for Production
```bash
npm run build
```

### Run Tests
```bash
npm run test:unit
```

### Lint & Format
```bash
npm run lint
npm run format
```

## Project Structure

```
frontend/
├── src/
│   ├── views/     # Page components (Dashboard, Chat)
│   ├── components/# Reusable UI components
│   ├── stores/    # Pinia state management
│   ├── services/  # API clients
│   ├── assets/    # Static assets
│   └── main.ts    # App entry point
├── tests/         # Test files
└── index.html     # HTML entry point
```

## API Configuration

The frontend proxy is configured in `vite.config.ts` to forward `/api` requests to `http://localhost:8000`.

## Features

- Portfolio dashboard with statistics
- AI chat assistant for portfolio queries
- Responsive design with Tailwind CSS
- Vue 3 Composition API with TypeScript
