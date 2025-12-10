# Docker and Kubernetes Deployment Guide

Complete guide for deploying Kettler Data Analysis services using Docker and Kubernetes for parallel execution.

## Overview

The project has been containerized to enable:
- **Parallel execution** of ETL and analysis tasks
- **Scalable services** using Docker Compose or Kubernetes
- **Docker MCP integration** for programmatic container management
- **Team collaboration** with Docker TEAM mode support

## Quick Start

### Docker Compose (Local Development)

```bash
# Build and start all services
docker-compose up -d

# Scale services for parallel execution
docker-compose up -d --scale python-etl=3 --scale r-analysis=2

# View logs
docker-compose logs -f python-etl

# Stop services
docker-compose down
```

### Kubernetes (Production)

```bash
# Create persistent volumes
kubectl apply -f kubernetes/persistent-volumes.yaml

# Deploy services
kubectl apply -f kubernetes/python-etl-deployment.yaml
kubectl apply -f kubernetes/r-analysis-deployment.yaml
kubectl apply -f kubernetes/vector-api-deployment.yaml

# Scale services
kubectl scale deployment python-etl --replicas=5
```

## Architecture

### Services

1. **Python ETL Service** (`python-etl`)
   - Vector embeddings
   - Data processing
   - ETL pipeline execution
   - Default: 2 replicas (parallel)

2. **R Analysis Service** (`r-analysis`)
   - Data analysis
   - Connection analysis
   - Evidence processing
   - Default: 3 replicas (parallel)

3. **Vector API Service** (`vector-api`)
   - Vector similarity search
   - Embedding queries
   - REST API endpoint
   - Default: 2 replicas (load balanced)

4. **R API Service** (`r-api`)
   - R analysis API
   - REST endpoints for R functions
   - Default: 1 replica (scalable)

## Docker MCP Integration

The Docker MCP server provides programmatic control:

```python
from docker.mcp.docker_mcp_server import DockerMCPServer

server = DockerMCPServer()

# List containers
containers = server.list_containers()

# Start service
server.start_service('python-etl')

# Scale service
server.scale_service('python-etl', replicas=5)

# Run parallel tasks
tasks = [
    {'service': 'python-etl', 'command': ['python', 'scripts/etl/etl_pipeline.py']},
    {'service': 'r-analysis', 'command': ['Rscript', 'scripts/analysis/analyze_all_evidence.R']}
]
results = server.run_parallel_tasks(tasks)
```

## Parallel Execution

### Using Docker Compose

```bash
# Scale ETL to 3 parallel instances
docker-compose up -d --scale python-etl=3

# Scale analysis to 2 parallel instances
docker-compose up -d --scale r-analysis=2
```

### Using Kubernetes

```bash
# Scale deployments
kubectl scale deployment python-etl --replicas=5
kubectl scale deployment r-analysis --replicas=4
```

### Using Orchestrator Script

```bash
# Run ETL pipeline in parallel (Docker)
python scripts/orchestration/parallel_executor.py --etl --parallel --backend docker

# Run ETL pipeline in parallel (Kubernetes)
python scripts/orchestration/parallel_executor.py --etl --parallel --backend kubernetes

# Scale services
python scripts/orchestration/parallel_executor.py --scale 5 --backend docker
```

## API Endpoints

### Vector API (Port 8000)

```bash
# Health check
curl http://localhost:8000/health

# Search similar content
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Caitlin Skidmore", "top_k": 10}'

# Get statistics
curl http://localhost:8000/api/v1/stats

# Create embedding
curl -X POST http://localhost:8000/api/v1/embed \
  -H "Content-Type: application/json" \
  -d '{"text": "Sample text", "source": "api"}'
```

### R API (Port 8001)

```bash
# Health check
curl http://localhost:8001/health

# Analyze connections
curl -X POST http://localhost:8001/api/v1/analyze/connections

# Analyze evidence
curl -X POST http://localhost:8001/api/v1/analyze/evidence
```

## Volume Management

### Docker Compose

Volumes are mounted from host:
- `./data` → `/app/data`
- `./research` → `/app/research`
- `./evidence` → `/app/evidence`
- `./scripts` → `/app/scripts`

### Kubernetes

Uses PersistentVolumeClaims:
- `kettler-data-pvc`: 50GB
- `kettler-research-pvc`: 20GB
- `kettler-evidence-pvc`: 30GB
- `kettler-outputs-pvc`: 10GB

## Resource Limits

### Docker Compose

Configured in `docker-compose.yml`:
- **CPU**: 1-2 cores per service
- **Memory**: 2-4GB per service

### Kubernetes

Configured in deployment YAMLs:
- **CPU**: 0.5-2 cores per pod
- **Memory**: 1-4GB per pod

## Monitoring

### Docker Compose

```bash
# Service status
docker-compose ps

# Resource usage
docker stats

# Logs
docker-compose logs -f python-etl
```

### Kubernetes

```bash
# Pod status
kubectl get pods -l app=python-etl

# Resource usage
kubectl top pods -l app=python-etl

# Logs
kubectl logs -l app=python-etl --tail=100 -f
```

## Docker TEAM Mode

With Docker TEAM mode subscription:

1. **Shared Images**: Push images to Docker Hub or registry
2. **Team Access**: Team members can pull and run containers
3. **Parallel Execution**: Multiple team members can run services simultaneously
4. **Resource Management**: Docker Desktop manages resources across team

### Sharing Images

```bash
# Tag image
docker tag kettler-python-etl:latest your-registry/kettler-python-etl:latest

# Push to registry
docker push your-registry/kettler-python-etl:latest

# Team members pull
docker pull your-registry/kettler-python-etl:latest
```

## Troubleshooting

### Services Not Starting

```bash
# Check logs
docker-compose logs python-etl

# Check resource limits
docker stats

# Restart service
docker-compose restart python-etl
```

### Kubernetes Pods Not Running

```bash
# Check pod status
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Check resource quotas
kubectl describe quota
```

### Volume Mount Issues

```bash
# Check volume mounts (Docker)
docker inspect <container-id> | grep Mounts

# Check PVC status (Kubernetes)
kubectl get pvc
kubectl describe pvc kettler-data-pvc
```

## Best Practices

1. **Resource Planning**: Monitor resource usage and adjust limits
2. **Scaling**: Start with 2-3 replicas, scale based on load
3. **Monitoring**: Set up logging and monitoring for production
4. **Backup**: Regularly backup persistent volumes
5. **Security**: Use secrets for sensitive data in Kubernetes

## Next Steps

1. Set up monitoring (Prometheus, Grafana)
2. Configure CI/CD pipelines
3. Set up auto-scaling based on metrics
4. Implement service mesh (Istio, Linkerd) for advanced routing
