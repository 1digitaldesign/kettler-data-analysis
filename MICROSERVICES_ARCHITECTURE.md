# Microservices Architecture - Hybrid Next.js/Vercel + GCP

**Date:** December 9, 2024
**Status:** Implemented

## Overview

Hybrid microservices architecture:
- **Frontend:** Next.js deployed on Vercel (serverless)
- **Backend:** Microservices deployed on Google Cloud Platform (GCP) Cloud Run
- **API Gateway:** Routes requests from Next.js to appropriate microservices

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Next.js/Vercel Frontend                  │
│  (Serverless Functions, Edge Functions, Static Assets)       │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTPS
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    API Gateway (Cloud Run)                   │
│              Routes requests to microservices                │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
│  Analysis    │ │  Scraping   │ │ Validation │
│  Service     │ │  Service    │ │  Service   │
│  (Cloud Run) │ │ (Cloud Run) │ │(Cloud Run) │
└──────────────┘ └─────────────┘ └────────────┘
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
│   Vector     │ │     GIS     │ │   ACRIS   │
│   Service   │ │   Service   │ │  Service  │
│  (Cloud Run) │ │ (Cloud Run) │ │(Cloud Run)│
└──────────────┘ └─────────────┘ └───────────┘
        │
┌───────▼──────┐
│    Data      │
│  Repository  │
│   Service    │
│  (Cloud Run) │
└──────────────┘
```

## Microservices

### 1. API Gateway (`api-gateway`)
**Port:** 8000
**Purpose:** Single entry point, routes requests to appropriate services
**GCP:** Cloud Run
**Endpoints:**
- `/api/analysis/*` → Analysis Service
- `/api/scraping/*` → Scraping Service
- `/api/validation/*` → Validation Service
- `/api/vectors/*` → Vector Service
- `/api/gis/*` → GIS Service
- `/api/acris/*` → ACRIS Service
- `/api/data/*` → Data Repository Service

### 2. Analysis Service (`analysis-service`)
**Port:** 8001
**Purpose:** Data analysis operations
**Endpoints:**
- `POST /analyze/fraud` - Fraud pattern analysis
- `POST /analyze/nexus` - Nexus pattern analysis
- `POST /analyze/connections` - Connection analysis
- `POST /analyze/violations` - Violation detection
- `POST /analyze/all` - Run all analyses

### 3. Scraping Service (`scraping-service`)
**Port:** 8002
**Purpose:** Web scraping operations
**Endpoints:**
- `POST /scrape/airbnb` - Airbnb scraping
- `POST /scrape/vrbo` - VRBO scraping
- `POST /scrape/front` - Front website scraping
- `POST /scrape/acris` - ACRIS property records

### 4. Validation Service (`validation-service`)
**Port:** 8003
**Purpose:** Data validation operations
**Endpoints:**
- `POST /validate/license` - License validation
- `POST /validate/address` - Address validation
- `POST /validate/firm` - Firm validation
- `POST /validate/batch` - Batch validation

### 5. Vector Service (`vector-service`)
**Port:** 8004
**Purpose:** Vector embeddings and similarity search
**Endpoints:**
- `POST /vectors/embed` - Create embeddings
- `POST /vectors/search` - Similarity search
- `POST /vectors/index` - Index documents
- `GET /vectors/status` - Service status

### 6. GIS Service (`gis-service`)
**Port:** 8005
**Purpose:** GIS file conversion
**Endpoints:**
- `POST /gis/convert` - Convert GIS files
- `GET /gis/info/{file_path}` - Get file info
- `POST /gis/batch` - Batch conversion

### 7. ACRIS Service (`acris-service`)
**Port:** 8006
**Purpose:** ACRIS property records
**Endpoints:**
- `POST /acris/search/block-lot` - Search by block/lot
- `POST /acris/search/address` - Search by address
- `POST /acris/search/party` - Search by party name
- `POST /acris/search/document` - Search by document ID

### 8. Data Repository Service (`data-service`)
**Port:** 8007
**Purpose:** Data access and storage
**Endpoints:**
- `GET /data/firms` - Get firms
- `GET /data/firms/{id}` - Get firm by ID
- `POST /data/firms` - Create firm
- `PUT /data/firms/{id}` - Update firm
- `DELETE /data/firms/{id}` - Delete firm

## Next.js Integration

### API Routes
Next.js API routes proxy requests to GCP API Gateway:

```typescript
// pages/api/analysis/fraud.ts
import axios from 'axios';

export default async function handler(req, res) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  try {
    const response = await axios.post(`${apiUrl}/api/analysis/fraud`, req.body);
    res.status(200).json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
```

### Environment Variables (Vercel)
```bash
NEXT_PUBLIC_API_URL=https://api-gateway-xxx.run.app
```

## GCP Configuration

### Cloud Run Settings
- **Memory:** 2Gi per service
- **CPU:** 2 vCPU per service
- **Timeout:** 300 seconds
- **Max Instances:** 10
- **Min Instances:** 0 (scale to zero)
- **Concurrency:** 80 requests per instance

### Service URLs
Each service gets a Cloud Run URL:
- `https://analysis-service-xxx.run.app`
- `https://scraping-service-xxx.run.app`
- etc.

### Environment Variables
Set in Cloud Run:
```bash
ANALYSIS_SERVICE_URL=https://analysis-service-xxx.run.app
SCRAPING_SERVICE_URL=https://scraping-service-xxx.run.app
VALIDATION_SERVICE_URL=https://validation-service-xxx.run.app
VECTOR_SERVICE_URL=https://vector-service-xxx.run.app
GIS_SERVICE_URL=https://gis-service-xxx.run.app
ACRIS_SERVICE_URL=https://acris-service-xxx.run.app
DATA_SERVICE_URL=https://data-service-xxx.run.app
```

## Deployment

### Local Development
```bash
# Start all services locally
cd microservices
docker-compose up

# Or start individually
cd microservices/analysis-service
python -m uvicorn main:app --port 8001
```

### GCP Deployment
```bash
# Set project
export GCP_PROJECT_ID=your-project-id
export GCP_REGION=us-central1

# Deploy all services
cd microservices
./deploy.sh

# Or use Cloud Build
gcloud builds submit --config cloudbuild.yaml
```

### Vercel Deployment
```bash
# Deploy Next.js frontend
cd web
vercel deploy

# Set environment variables in Vercel dashboard
NEXT_PUBLIC_API_URL=https://api-gateway-xxx.run.app
```

## Communication Patterns

### Synchronous (REST)
- HTTP/REST for request-response
- JSON payloads
- Standard status codes
- Timeout: 30 seconds

### Asynchronous (Future)
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

## Monitoring

### Cloud Monitoring
- Service health checks (`/health` endpoint)
- Request metrics
- Error tracking
- Performance monitoring

### Logging
- Cloud Logging integration
- Structured logging
- Request tracing

## Security

### Authentication
- **Service-to-service:** Service accounts
- **Frontend-to-backend:** API keys / OAuth
- **Cloud Run:** IAM roles

### Network
- HTTPS only
- VPC for internal communication (optional)
- Cloud Armor for DDoS protection

## Cost Optimization

### Cloud Run
- Pay-per-use (scale to zero)
- Only pay for actual usage
- Auto-scaling based on traffic

### Vercel
- Free tier for Next.js
- Pay for bandwidth and serverless functions

## Benefits

1. **Scalability:** Each service scales independently
2. **Maintainability:** Clear separation of concerns
3. **Deployment:** Independent deployments
4. **Technology:** Can use different tech stacks per service
5. **Cost:** Pay only for what you use
6. **Performance:** Optimized for each service's needs

## Migration Path

1. ✅ Microservices created
2. ✅ API Gateway implemented
3. ⏭️ Deploy to GCP Cloud Run
4. ⏭️ Update Next.js to use API Gateway
5. ⏭️ Migrate from monolithic API
6. ⏭️ Add monitoring and logging
7. ⏭️ Implement service-to-service auth

## File Structure

```
microservices/
├── api-gateway/
│   └── main.py
├── analysis-service/
│   └── main.py
├── scraping-service/
│   └── main.py
├── validation-service/
│   └── main.py
├── vector-service/
│   └── main.py
├── gis-service/
│   └── main.py
├── acris-service/
│   └── main.py
├── data-service/
│   └── main.py
├── Dockerfile
├── docker-compose.yml
├── cloudbuild.yaml
├── deploy.sh
└── README.md
```
