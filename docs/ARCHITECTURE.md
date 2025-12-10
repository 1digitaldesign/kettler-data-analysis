# Microservices Architecture Documentation

**Date:** December 8, 2025
**Version:** 1.0.0

---

## Overview

The Kettler Data Analysis system uses a microservices architecture to perform automated license searches, data processing, and vector storage. The system is designed to scale horizontally and handle high-volume license searches across multiple states.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway (3000)                      │
│                  Express.js - Load Balancer                 │
└────────────┬────────────────────────────────────────────────┘
             │
    ┌────────┴────────┬──────────────┬──────────────┐
    │                  │              │              │
┌───▼────┐    ┌───────▼────┐  ┌──────▼────┐  ┌─────▼──────┐
│Scraper │    │  Processor │  │  Vector   │  │ Scheduler  │
│Service │    │  Service   │  │  Service  │  │  Service  │
│ (3001) │    │   (3002)   │  │   (3003)  │  │   (3004)  │
└───┬────┘    └───────┬────┘  └──────┬────┘  └─────┬──────┘
    │                  │              │              │
    │                  │              │              │
┌───▼────┐    ┌───────▼────┐  ┌──────▼────┐  ┌─────▼──────┐
│ Redis  │    │ PostgreSQL │  │  Qdrant   │  │   Redis   │
│ Queue  │    │  Metadata  │  │  Vectors  │  │   Queue   │
└────────┘    └─────────────┘  └───────────┘  └───────────┘
```

---

## Microservices

### 1. Scraper Service (Port 3001)

**Technology:** Node.js + Express + Playwright

**Purpose:** Browser automation and web scraping for license searches

**Key Features:**
- Executes browser automation using universal_devtools_scraper.js
- Handles CAPTCHA (manual or service integration)
- Queues jobs using Redis/Bull
- Supports single and batch searches

**API Endpoints:**
- `POST /api/v1/scrape/employee` - Search single employee
- `POST /api/v1/scrape/batch` - Batch search multiple employees
- `GET /api/v1/scrape/status/:jobId` - Get job status
- `GET /api/v1/scrape/jobs` - List all jobs

**Dependencies:**
- Redis (job queue)
- Playwright (browser automation)

**Scaling:** Stateless, can scale horizontally

---

### 2. Data Processing Service (Port 3002)

**Technology:** Python + FastAPI + R (via rpy2)

**Purpose:** Data consolidation, analysis, and embedding generation

**Key Features:**
- Executes R scripts for data consolidation
- Generates complaint letters
- Creates embeddings using sentence-transformers
- Transforms and processes data

**API Endpoints:**
- `POST /api/v1/process/consolidate` - Run consolidation scripts
- `POST /api/v1/process/generate-letters` - Generate complaint letters
- `POST /api/v1/process/embeddings` - Generate single embedding
- `POST /api/v1/process/embeddings/batch` - Generate batch embeddings
- `POST /api/v1/process/transform` - Transform data

**Dependencies:**
- Redis (optional, for job queuing)
- PostgreSQL (metadata storage)
- R runtime (for R script execution)

**Scaling:** Can scale horizontally, but R execution may be CPU-intensive

---

### 3. Vector Service (Port 3003)

**Technology:** Python + FastAPI + Qdrant Client

**Purpose:** Vector storage and similarity search

**Key Features:**
- Stores document embeddings in Qdrant
- Performs similarity search
- Manages vector collections
- Integrates with embedding generator

**API Endpoints:**
- `POST /api/v1/vectors/store` - Store single vector
- `POST /api/v1/vectors/store/batch` - Store batch vectors
- `POST /api/v1/vectors/search` - Similarity search
- `GET /api/v1/vectors/:collection/:id` - Retrieve vector
- `GET /api/v1/vectors/collections` - List collections
- `DELETE /api/v1/vectors/:collection/:id` - Delete vector

**Collections:**
- `license_findings` - License search results
- `employees` - Employee information
- `violations` - Violation records

**Dependencies:**
- Qdrant (vector database)

**Scaling:** Stateless, can scale horizontally

---

### 4. API Gateway (Port 3000)

**Technology:** Node.js + Express

**Purpose:** Single entry point, request routing, load balancing

**Key Features:**
- Routes requests to appropriate services
- Service discovery
- Request aggregation
- Health check aggregation
- Rate limiting

**Endpoints:**
- `GET /health` - Gateway health
- `GET /health/services` - All services health
- `POST /api/v1/search/complete` - Complete workflow

**Dependencies:**
- All microservices

**Scaling:** Stateless, can scale horizontally

---

### 5. Scheduler Service (Port 3004)

**Technology:** Node.js + Express + node-cron

**Purpose:** Automated scheduling of searches and maintenance tasks

**Key Features:**
- Cron-based scheduling
- Daily license searches
- Weekly data consolidation
- Monthly report generation

**Schedules:**
- Daily: 2 AM - License searches for high-priority employees
- Weekly: Sunday 3 AM - Data consolidation
- Monthly: 1st of month 4 AM - Report generation

**Dependencies:**
- Redis (job queuing)
- Scraper Service
- Processor Service

**Scaling:** Single replica (scheduler should run once)

---

## Data Storage

### PostgreSQL

**Purpose:** Structured metadata storage

**Schema:**
- License findings metadata
- Employee information
- Job status and results
- System configuration

**Access:** Via data-processing-service

---

### Qdrant

**Purpose:** Vector storage for embeddings

**Collections:**
- `license_findings` - License search results with embeddings
- `employees` - Employee profiles with embeddings
- `violations` - Violation records with embeddings

**Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)

**Access:** Via vector-service

---

### Redis

**Purpose:** Job queue and caching

**Queues:**
- `scrape-queue` - Scraping jobs
- `scheduler-queue` - Scheduled tasks

**Access:** All services use Redis for job queuing

---

## Deployment

### Development (Docker Compose)

**File:** `docker-compose.yml`

**Services:**
- All microservices
- PostgreSQL
- Redis
- Qdrant (embedded mode)

**Usage:**
```bash
docker-compose up -d
```

**Access:**
- API Gateway: http://localhost:3000
- Scraper Service: http://localhost:3001
- Processor Service: http://localhost:3002
- Vector Service: http://localhost:3003
- Scheduler Service: http://localhost:3004

---

### Production (Kubernetes)

**Namespace:** `kettler-search`

**Deployments:**
- scraper-service (2 replicas)
- data-processing-service (2 replicas)
- vector-service (2 replicas)
- api-gateway (2 replicas)
- scheduler-service (1 replica)
- redis (1 replica)
- postgres (1 replica)
- qdrant (1 replica, can scale to 3+)

**Services:**
- All services exposed via ClusterIP
- API Gateway exposed via LoadBalancer/Ingress

**Persistent Volumes:**
- qdrant-pvc (50Gi)
- postgres-pvc (20Gi)
- redis-pvc (10Gi)

**Deployment:**
```bash
# Create namespace
kubectl apply -f kubernetes/namespaces/kettler-search.yaml

# Apply ConfigMaps
kubectl apply -f kubernetes/configmaps/app-config.yaml

# Apply Secrets (create from example first)
kubectl apply -f kubernetes/secrets/secrets.yaml

# Apply Persistent Volumes
kubectl apply -f kubernetes/persistent-volumes/

# Apply Services
kubectl apply -f kubernetes/services/

# Apply Deployments
kubectl apply -f kubernetes/deployments/
```

---

## API Documentation

### Scraper Service

#### Search Single Employee
```http
POST /api/v1/scrape/employee
Content-Type: application/json

{
  "employee": {
    "name": "Caitlin Skidmore",
    "lastName": "Skidmore",
    "firstName": "Caitlin"
  },
  "state": "Connecticut",
  "options": {}
}
```

#### Batch Search
```http
POST /api/v1/scrape/batch
Content-Type: application/json

{
  "employees": [...],
  "state": "Connecticut",
  "options": {}
}
```

#### Get Job Status
```http
GET /api/v1/scrape/status/:jobId
```

---

### Processor Service

#### Consolidate Findings
```http
POST /api/v1/process/consolidate
Content-Type: application/json

{
  "state": "Connecticut",
  "output_format": "csv"
}
```

#### Generate Complaint Letters
```http
POST /api/v1/process/generate-letters
Content-Type: application/json

{
  "states": ["Connecticut", "Maryland"],
  "output_dir": "/app/output"
}
```

#### Generate Embeddings
```http
POST /api/v1/process/embeddings
Content-Type: application/json

{
  "text": "License search result text...",
  "metadata": {
    "employee": "Caitlin Skidmore",
    "state": "Connecticut"
  }
}
```

---

### Vector Service

#### Store Vector
```http
POST /api/v1/vectors/store
Content-Type: application/json

{
  "collection": "license_findings",
  "text": "License search result text...",
  "metadata": {
    "employee": "Caitlin Skidmore",
    "state": "Connecticut",
    "licensed": false
  },
  "id": "optional-id"
}
```

#### Search Vectors
```http
POST /api/v1/vectors/search
Content-Type: application/json

{
  "collection": "license_findings",
  "query_text": "unlicensed operations",
  "limit": 10,
  "score_threshold": 0.7,
  "filter": {
    "state": "Connecticut"
  }
}
```

---

## Workflow Examples

### Complete Search Workflow

1. **Scrape** - API Gateway → Scraper Service
2. **Process** - Scraper Service → Processor Service (generate embeddings)
3. **Store** - Processor Service → Vector Service (store embeddings)
4. **Query** - Vector Service (similarity search)

### Scheduled Daily Search

1. **Scheduler Service** triggers at 2 AM
2. Queues jobs in Redis for high-priority employees
3. **Scraper Service** processes jobs
4. Results stored in PostgreSQL and Qdrant

---

## Monitoring

### Health Checks

All services provide `/health` endpoints:
- `GET /health` - Service health status

### Service Health Aggregation

API Gateway provides aggregated health:
- `GET /health/services` - All services health status

---

## Configuration

### Environment Variables

See `.env.example` for development configuration.

### Kubernetes ConfigMaps

See `kubernetes/configmaps/app-config.yaml` for production configuration.

### Secrets

See `kubernetes/secrets/secrets.example.yaml` for secret structure.

**IMPORTANT:** Never commit actual secrets. Use Kubernetes Secrets.

---

## Scaling

### Horizontal Scaling

All services except scheduler can scale horizontally:
- Scraper Service: 2+ replicas
- Processor Service: 2+ replicas
- Vector Service: 2+ replicas
- API Gateway: 2+ replicas

### Vertical Scaling

Adjust resource limits in Kubernetes deployments:
- Scraper Service: 2Gi memory, 1000m CPU
- Processor Service: 4Gi memory, 2000m CPU
- Vector Service: 4Gi memory, 2000m CPU

---

## Security

### Best Practices

1. **Secrets Management**: Use Kubernetes Secrets, never commit
2. **Network Security**: Use ClusterIP for internal services
3. **Rate Limiting**: Implemented in API Gateway
4. **Input Validation**: Validate all API inputs
5. **Error Handling**: Don't expose internal errors

---

## Troubleshooting

### Common Issues

1. **Browser Locked**: Close browser sessions properly
2. **Qdrant Connection**: Check QDRANT_HOST and QDRANT_PORT
3. **Redis Connection**: Check REDIS_HOST and REDIS_PORT
4. **R Script Errors**: Check R packages installed in container

### Debugging

1. Check service logs: `kubectl logs -n kettler-search <service-name>`
2. Check health endpoints: `curl http://localhost:<port>/health`
3. Check Redis queue: `redis-cli KEYS *`
4. Check Qdrant collections: `curl http://localhost:6333/collections`

---

## Future Enhancements

1. **Authentication**: Add API key authentication
2. **Monitoring**: Integrate Prometheus and Grafana
3. **Logging**: Centralized logging with ELK stack
4. **Caching**: Add Redis caching layer
5. **Load Testing**: Implement load testing suite

---

**Last Updated:** December 8, 2025
**Status:** Production Ready
