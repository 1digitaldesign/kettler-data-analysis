# Microservices Architecture

**Date:** December 9, 2024
**Status:** Implemented

## Overview

Hybrid microservices architecture:
- **Frontend:** Next.js/Vercel (serverless)
- **Backend:** Google Cloud Platform (GCP) microservices

## Architecture Pattern

### Service-Oriented Architecture (SOA)
- Independent, scalable services
- API Gateway pattern for routing
- Service discovery and communication
- Event-driven communication where appropriate

## Microservices

### 1. Analysis Service
**Purpose:** Data analysis operations
**GCP:** Cloud Run
**Port:** 8001
**Endpoints:**
- `POST /analyze/fraud` - Fraud pattern analysis
- `POST /analyze/nexus` - Nexus pattern analysis
- `POST /analyze/connections` - Connection analysis
- `POST /analyze/violations` - Violation detection
- `POST /analyze/all` - Run all analyses

### 2. Scraping Service
**Purpose:** Web scraping operations
**GCP:** Cloud Run
**Port:** 8002
**Endpoints:**
- `POST /scrape/airbnb` - Airbnb scraping
- `POST /scrape/vrbo` - VRBO scraping
- `POST /scrape/front` - Front website scraping
- `POST /scrape/acris` - ACRIS property records

### 3. Validation Service
**Purpose:** Data validation operations
**GCP:** Cloud Run
**Port:** 8003
**Endpoints:**
- `POST /validate/license` - License validation
- `POST /validate/address` - Address validation
- `POST /validate/firm` - Firm validation
- `POST /validate/batch` - Batch validation

### 4. Vector Service
**Purpose:** Vector embeddings and similarity search
**GCP:** Cloud Run
**Port:** 8004
**Endpoints:**
- `POST /vectors/embed` - Create embeddings
- `POST /vectors/search` - Similarity search
- `POST /vectors/index` - Index documents
- `GET /vectors/status` - Service status

### 5. GIS Service
**Purpose:** GIS file conversion
**GCP:** Cloud Run
**Port:** 8005
**Endpoints:**
- `POST /gis/convert` - Convert GIS files
- `GET /gis/info/{file_path}` - Get file info
- `POST /gis/batch` - Batch conversion

### 6. ACRIS Service
**Purpose:** ACRIS property records
**GCP:** Cloud Run
**Port:** 8006
**Endpoints:**
- `POST /acris/search/block-lot` - Search by block/lot
- `POST /acris/search/address` - Search by address
- `POST /acris/search/party` - Search by party name
- `POST /acris/search/document` - Search by document ID

### 7. Data Repository Service
**Purpose:** Data access and storage
**GCP:** Cloud Run
**Port:** 8007
**Endpoints:**
- `GET /data/firms` - Get firms
- `GET /data/firms/{id}` - Get firm by ID
- `POST /data/firms` - Create firm
- `PUT /data/firms/{id}` - Update firm
- `DELETE /data/firms/{id}` - Delete firm

### 8. Google Drive Service
**Purpose:** Google Drive operations
**GCP:** Cloud Run
**Port:** 8008
**Endpoints:**
- `POST /drive/list` - List folder contents
- `POST /drive/download` - Download file
- `POST /drive/export` - Export Google Docs/Sheets
- `GET /drive/info/{file_id}` - Get file information

## API Gateway

**Purpose:** Single entry point for all services
**GCP:** Cloud Run
**Port:** 8000
**Routes:**
- `/api/analysis/*` → Analysis Service
- `/api/scraping/*` → Scraping Service
- `/api/validation/*` → Validation Service
- `/api/vectors/*` → Vector Service
- `/api/gis/*` → GIS Service
- `/api/acris/*` → ACRIS Service
- `/api/data/*` → Data Repository Service
- `/api/drive/*` → Google Drive Service

## Communication Patterns

### Synchronous (REST)
- HTTP/REST for request-response
- JSON payloads
- Standard status codes

### Asynchronous (Events)
- Cloud Pub/Sub for events
- Event-driven processing
- Decoupled services

## Service Discovery

### Environment Variables
Each service registers with:
- `SERVICE_NAME` - Service identifier
- `SERVICE_PORT` - Service port
- `GCP_PROJECT_ID` - GCP project
- `SERVICE_URL` - Service URL (Cloud Run)

### Service Registry
- Cloud Run automatically provides URLs
- Environment variables for service URLs
- Fallback to localhost for development

## Deployment

### GCP Cloud Run
- Containerized services
- Auto-scaling
- Pay-per-use
- HTTPS endpoints

### Vercel (Frontend)
- Next.js serverless functions
- Edge functions for API routes
- Automatic HTTPS

## Configuration

### Environment Variables
```bash
# GCP Configuration
GCP_PROJECT_ID=your-project-id
GCP_REGION=us-central1

# Service URLs (Cloud Run)
ANALYSIS_SERVICE_URL=https://analysis-service-xxx.run.app
SCRAPING_SERVICE_URL=https://scraping-service-xxx.run.app
VALIDATION_SERVICE_URL=https://validation-service-xxx.run.app
VECTOR_SERVICE_URL=https://vector-service-xxx.run.app
GIS_SERVICE_URL=https://gis-service-xxx.run.app
ACRIS_SERVICE_URL=https://acris-service-xxx.run.app
DATA_SERVICE_URL=https://data-service-xxx.run.app

# API Gateway
API_GATEWAY_URL=https://api-gateway-xxx.run.app

# Next.js
NEXT_PUBLIC_API_URL=https://api-gateway-xxx.run.app
```

## Development

### Local Development
```bash
# Start all services locally
make dev-services

# Start individual service
cd microservices/analysis-service
python -m uvicorn main:app --port 8001
```

### Testing
```bash
# Test all services
make test-services

# Test individual service
cd microservices/analysis-service
pytest
```

## Monitoring

### Cloud Monitoring
- Service health checks
- Request metrics
- Error tracking
- Performance monitoring

### Logging
- Cloud Logging integration
- Structured logging
- Request tracing

## Security

### Authentication
- Service-to-service: Service accounts
- Frontend-to-backend: API keys / OAuth

### Network
- HTTPS only
- VPC for internal communication
- Cloud Armor for DDoS protection
