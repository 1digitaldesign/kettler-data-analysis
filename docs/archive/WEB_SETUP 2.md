# Web Application Setup Guide

## Quick Start

### 1. Install Dependencies

**Python (API Server):**
```bash
pip install -r requirements.txt
```

**Node.js (Web Frontend):**
```bash
cd web
npm install
```

### 2. Start Application

**Option A: Use startup script**
```bash
./start_web.sh
```

**Option B: Manual start**

Terminal 1 - API Server:
```bash
python3 scripts/api/web_api_server.py
```

Terminal 2 - Web Frontend:
```bash
cd web
npm run dev
```

### 3. Access Application

- **Web UI:** http://localhost:3000
- **API:** http://localhost:8000/api
- **Health Check:** http://localhost:8000/api/health

## Features

✅ **Interactive Dashboard** - Real-time stats and charts
✅ **Analysis Tools** - Run Python modules from web
✅ **Search Interface** - Search regulatory databases
✅ **Report Generation** - Generate and download reports
✅ **Vector Search** - Semantic search with embeddings
✅ **Modern UI** - React + TypeScript + Tailwind CSS

## Architecture

```
React Frontend (Port 3000)
    ↓ HTTP/REST API
Flask API Server (Port 8000)
    ↓ Python Modules
Unified Analysis Modules
```

## API Endpoints

- `GET /api/dashboard/stats` - Dashboard statistics
- `POST /api/analysis/run` - Run analysis
- `GET /api/search/regulatory-agencies` - Search agencies
- `POST /api/search/dpor` - Search DPOR
- `POST /api/vector/search` - Vector semantic search
- `GET /api/reports` - List reports
- `POST /api/reports/generate` - Generate report

## Development

The web application uses:
- **Vite** for fast development
- **Hot Module Replacement** for instant updates
- **TypeScript** for type safety
- **Tailwind CSS** for styling

See `WEB_APPLICATION.md` for full documentation.
