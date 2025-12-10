# Deployment Guide

**Date:** December 8, 2025

---

## Quick Start

### Development (Docker Compose)

1. **Prerequisites:**
   - Docker and Docker Compose installed
   - At least 8GB RAM available
   - Ports 3000-3004, 5432, 6333, 6379 available

2. **Setup:**
   ```bash
   # Copy environment file
   cp .env.example .env

   # Edit .env with your configuration (optional)
   # Start all services
   docker-compose up -d

   # View logs
   docker-compose logs -f
   ```

3. **Verify:**
   ```bash
   # Check all services are running
   docker-compose ps

   # Test API Gateway
   curl http://localhost:3000/health

   # Test individual services
   curl http://localhost:3001/health  # Scraper
   curl http://localhost:3002/health  # Processor
   curl http://localhost:3003/health  # Vector
   curl http://localhost:3004/health  # Scheduler
   ```

4. **Stop Services:**
   ```bash
   docker-compose down
   ```

---

## Production (Kubernetes)

### Prerequisites

- Kubernetes cluster (v1.24+)
- kubectl configured
- Storage class configured
- Ingress controller (optional, for external access)

### Step 1: Create Namespace

```bash
kubectl apply -f kubernetes/namespaces/kettler-search.yaml
```

### Step 2: Create Secrets

```bash
# Copy example secrets
cp kubernetes/secrets/secrets.example.yaml kubernetes/secrets/secrets.yaml

# Edit secrets.yaml with actual values
# IMPORTANT: Never commit secrets.yaml

# Apply secrets
kubectl apply -f kubernetes/secrets/secrets.yaml
```

### Step 3: Create ConfigMaps

```bash
kubectl apply -f kubernetes/configmaps/app-config.yaml
```

### Step 4: Create Persistent Volumes

```bash
kubectl apply -f kubernetes/persistent-volumes/qdrant-pv.yaml
kubectl apply -f kubernetes/persistent-volumes/postgres-pv.yaml
kubectl apply -f kubernetes/persistent-volumes/redis-pv.yaml
```

### Step 5: Deploy Infrastructure Services

```bash
# Deploy Redis
kubectl apply -f kubernetes/deployments/redis-deployment.yaml
kubectl apply -f kubernetes/services/redis-service.yaml

# Deploy PostgreSQL
kubectl apply -f kubernetes/deployments/postgres-deployment.yaml
kubectl apply -f kubernetes/services/postgres-service.yaml

# Deploy Qdrant
kubectl apply -f kubernetes/deployments/qdrant-deployment.yaml
kubectl apply -f kubernetes/services/qdrant-service.yaml
```

### Step 6: Deploy Application Services

```bash
# Deploy Scraper Service
kubectl apply -f services/scraper-service/kubernetes/

# Deploy Processor Service
kubectl apply -f services/data-processing-service/kubernetes/

# Deploy Vector Service
kubectl apply -f services/vector-service/kubernetes/

# Deploy Scheduler Service
kubectl apply -f services/scheduler-service/kubernetes/

# Deploy API Gateway
kubectl apply -f services/api-gateway/kubernetes/
```

### Step 7: Deploy Ingress (Optional)

```bash
kubectl apply -f kubernetes/ingress/ingress.yaml
```

### Step 8: Verify Deployment

```bash
# Check all pods are running
kubectl get pods -n kettler-search

# Check services
kubectl get services -n kettler-search

# Check logs
kubectl logs -n kettler-search -l app=api-gateway
```

---

## Building Docker Images

### Build Individual Services

```bash
# Scraper Service
docker build -t kettler-search/scraper-service:latest ./services/scraper-service

# Processor Service
docker build -t kettler-search/data-processing-service:latest ./services/data-processing-service

# Vector Service
docker build -t kettler-search/vector-service:latest ./services/vector-service

# API Gateway
docker build -t kettler-search/api-gateway:latest ./services/api-gateway

# Scheduler Service
docker build -t kettler-search/scheduler-service:latest ./services/scheduler-service
```

### Build All Services

```bash
# Using docker-compose
docker-compose build

# Or build script
./scripts/build-all.sh
```

---

## Environment Configuration

### Development (.env)

```bash
POSTGRES_PASSWORD=your_password
LOG_LEVEL=debug
TZ=America/New_York
```

### Production (Kubernetes ConfigMap)

Edit `kubernetes/configmaps/app-config.yaml`:
- Service URLs
- Database hosts
- Log levels
- Feature flags

---

## Monitoring

### Health Checks

All services provide `/health` endpoints:
- Check individual services: `curl http://<service>:<port>/health`
- Check all via gateway: `curl http://api-gateway/health/services`

### Logs

**Docker Compose:**
```bash
docker-compose logs -f <service-name>
```

**Kubernetes:**
```bash
kubectl logs -n kettler-search -l app=<service-name> -f
```

### Metrics

Services expose metrics on `/metrics` endpoint (if implemented).

---

## Troubleshooting

### Service Won't Start

1. Check logs: `docker-compose logs <service>` or `kubectl logs <pod>`
2. Check health endpoint
3. Verify dependencies are running
4. Check resource limits

### Database Connection Issues

1. Verify PostgreSQL is running
2. Check connection string in environment variables
3. Verify network connectivity

### Qdrant Connection Issues

1. Verify Qdrant is running
2. Check QDRANT_HOST and QDRANT_PORT
3. Verify network connectivity

### Browser Automation Issues

1. Check Playwright browsers installed
2. Verify sufficient resources (memory/CPU)
3. Check for CAPTCHA requirements

---

## Scaling

### Horizontal Scaling (Kubernetes)

```bash
# Scale scraper service
kubectl scale deployment scraper-service -n kettler-search --replicas=5

# Scale processor service
kubectl scale deployment data-processing-service -n kettler-search --replicas=3
```

### Vertical Scaling

Edit deployment YAML files to adjust resource limits:
- `resources.requests.memory`
- `resources.requests.cpu`
- `resources.limits.memory`
- `resources.limits.cpu`

---

## Backup and Recovery

### PostgreSQL Backup

```bash
# Backup
kubectl exec -n kettler-search postgres-<pod-id> -- \
  pg_dump -U kettler kettler_search > backup.sql

# Restore
kubectl exec -i -n kettler-search postgres-<pod-id> -- \
  psql -U kettler kettler_search < backup.sql
```

### Qdrant Backup

```bash
# Qdrant stores data in persistent volume
# Backup the PVC or use Qdrant snapshot API
```

### Redis Backup

```bash
# Redis persists to disk (AOF)
# Backup the persistent volume
```

---

## Maintenance

### Updating Services

1. Build new Docker images
2. Update image tags in Kubernetes deployments
3. Apply updated deployments: `kubectl apply -f kubernetes/deployments/`
4. Rolling update will occur automatically

### Database Migrations

Run migrations via processor service API or directly:
```bash
kubectl exec -n kettler-search data-processing-service-<pod-id> -- \
  python -m alembic upgrade head
```

---

**Last Updated:** December 8, 2025
