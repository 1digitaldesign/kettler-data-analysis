# Web Application - Modern TypeScript/React Interface

## Overview

A modern, efficient web application built with TypeScript, React, and Vite for the Kettler Data Analysis project.

## Tech Stack

### Frontend
- **React 18** - Modern UI library
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Recharts** - Beautiful charts and visualizations
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Lucide React** - Modern icon library

### Backend API
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

## Features

### 🎯 Interactive Dashboard
- Real-time statistics display
- Quick action buttons
- Overview of findings

### 🔍 Advanced Search Interface
- **Vector Similarity Search** - Semantic search using embeddings
- **DPOR Database Search** - Search state licensing databases
- **Regulatory Agency Search** - Find relevant agencies
- Real-time results with similarity scores

### 📊 Data Visualization
- **Bar Charts** - Connection types distribution
- **Pie Charts** - Violation types breakdown
- Interactive tooltips
- Responsive design

### 🛠️ Analysis Tools
- Run analyses directly from web interface
- Real-time progress indicators
- Results display with status indicators
- Batch analysis support

## Project Structure

```
web/
├── src/
│   ├── components/
│   │   ├── Dashboard.tsx          # Main dashboard
│   │   ├── SearchInterface.tsx    # Search UI
│   │   ├── AnalysisTools.tsx      # Analysis runner
│   │   └── DataVisualization.tsx # Charts and graphs
│   ├── App.tsx                    # Main app component
│   ├── main.tsx                   # Entry point
│   └── index.css                  # Global styles
├── api/
│   └── server.py                  # FastAPI backend
├── package.json                   # Dependencies
├── vite.config.ts                 # Vite configuration
└── tsconfig.json                  # TypeScript config
```

## Installation

### Frontend
```bash
cd web
npm install
```

### Backend API
```bash
pip install fastapi uvicorn pydantic
```

## Development

### Start Frontend Dev Server
```bash
cd web
npm run dev
```
Opens at http://localhost:3000

### Start Backend API Server
```bash
python api/server.py
```
Runs at http://localhost:8000

## API Endpoints

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics

### Search
- `POST /api/search/vector` - Vector similarity search
- `POST /api/search/dpor` - DPOR database search
- `GET /api/search/regulatory` - Get regulatory agencies

### Analysis
- `POST /api/analysis/{type}` - Run specific analysis
  - Types: `fraud`, `nexus`, `timeline`, `anomalies`, `violations`

### Visualization
- `GET /api/visualization/data` - Get chart data

## Benefits Over R Scripts

1. **Interactive UI** - No command-line needed
2. **Real-time Updates** - See results as they're generated
3. **Better Visualization** - Interactive charts vs static outputs
4. **Easier Access** - Web-based, accessible from anywhere
5. **Modern UX** - Clean, intuitive interface
6. **Faster Development** - Hot reload, TypeScript autocomplete

## Browser Testing

The application is designed to work in modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Production Build

```bash
cd web
npm run build
```

Outputs to `web/dist/` directory.

## Integration with Python Backend

The web app seamlessly integrates with the unified Python modules:
- Calls Python API endpoints
- Displays analysis results
- Visualizes data from Python outputs
- Runs analyses on-demand

## Next Steps

1. Add authentication/authorization
2. Add data export functionality
3. Add more visualization types
4. Add real-time updates via WebSockets
5. Add mobile-responsive improvements
