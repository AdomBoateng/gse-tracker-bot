# GSE Tracker - Frontend

This is the Vue 3 frontend application for the Ghana Stock Exchange Tracker.

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
│   ├── views/     # Page components (Dashboard)
│   ├── App.vue    # Root component
│   └── main.ts    # App entry point
├── tests/         # Test files
└── index.html     # HTML entry point
```

## API Configuration

The frontend proxy is configured in `vite.config.ts` to forward `/api` requests to `http://localhost:8000`.

## Features

- Live GSE market dashboard with top gainers/losers and a searchable, sortable company table
- Market open/closed status with countdown
- Responsive design with Tailwind CSS
- Vue 3 Composition API with TypeScript
