# Microservices Architecture

## Overview

The system has been architected as a microservices-based system with proper service discovery, health checks, and inter-service communication.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│              Service Discovery (Port 8080)              │
│  - Service Registry                                     │
│  - Health Monitoring                                    │
│  - Service URL Resolution                               │
└─────────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼───────┐ ┌─────▼──────┐ ┌─────▼──────┐
│  Vector API   │ │  R API     │ │ Python ETL │
│  Port: 8000   │ │  Port: 8001│ │ Port: 8000 │
│               │ │            │ │            │
│  - Search     │ │  - Analysis│ │  - ETL     │
│  - Embed      │ │  - Evidence│ │  - Process │
│  - Stats      │ │  - Connect │ │  - Embed   │
└───────────────┘ └────────────┘ └────────────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
            ┌───────────▼───────────┐
            │   Shared Network      │
            │  kettler-network      │
            └───────────────────────┘
```

## Services

### 1. Service Discovery (`service-discovery`)
- **Port**: 8080
- **Purpose**: Centralized service registry and health monitoring
- **Endpoints**:
  - `GET /health` - Health check
  - `GET /api/v1/services` - List all services
  - `GET /api/v1/services/<name>` - Get service status
  - `GET /api/v1/services/<name>/url` - Get service URL

### 2. Vector API (`vector-api`)
- **Port**: 8000
- **Purpose**: Vector embedding search and management
- **Dependencies**: `python-etl` (for embeddings)
- **Endpoints**: `/health`, `/api/v1/search`, `/api/v1/stats`, `/api/v1/embed`

### 3. Python ETL (`python-etl`)
- **Port**: 8000 (internal)
- **Purpose**: ETL pipeline and data processing
- **Dependencies**: None (base service)
- **Function**: Processes data and creates embeddings

### 4. R API (`r-api`)
- **Port**: 8001
- **Purpose**: R-based analysis API
- **Dependencies**: `r-analysis`
- **Endpoints**: `/health`, `/api/v1/analyze/connections`, `/api/v1/analyze/evidence`

### 5. R Analysis (`r-analysis`)
- **Port**: 8001 (internal)
- **Purpose**: R-based data analysis
- **Dependencies**: None (base service)
- **Function**: Performs R-based analysis tasks

## Microservices Features

### ✅ Service Discovery
- Centralized registry
- Automatic service registration
- Health monitoring
- URL resolution

### ✅ Health Checks
- Docker healthchecks configured
- Service-level health endpoints
- Automatic restart on failure
- Dependency-based startup

### ✅ Inter-Service Communication
- Service client library
- HTTP-based communication
- Service URL discovery
- Error handling

### ✅ Resilience
- Automatic restarts
- Health check monitoring
- Dependency management
- Graceful degradation

### ✅ Scalability
- Horizontal scaling support
- Load balancing ready
- Resource limits configured
- Parallel execution enabled

## Service Communication

### Using Service Client

```python
from scripts.microservices.service_client import get_service_client

client = get_service_client()

# Call Vector API
stats = client.call_service('vector-api', '/api/v1/stats')

# Call R API
results = client.call_service('r-api', '/api/v1/analyze/connections', method='POST')

# Check health
is_healthy = client.is_service_healthy('vector-api')
```

### Direct HTTP Calls

```python
import requests

# Using service discovery
response = requests.get('http://service-discovery:8080/api/v1/services/vector-api/url')
service_url = response.json()['url']

# Call service
response = requests.get(f"{service_url}/api/v1/stats")
```

## Health Monitoring

### Service Discovery Health

```bash
# Check all services
curl http://localhost:8080/api/v1/services

# Check specific service
curl http://localhost:8080/api/v1/services/vector-api
```

### Health Monitor Script

```bash
# One-time check
python scripts/microservices/health_monitor.py

# Watch mode
python scripts/microservices/health_monitor.py --watch

# JSON output
python scripts/microservices/health_monitor.py --json
```

## Deployment

### Start All Services

```bash
docker-compose up -d
```

### Start Specific Services

```bash
docker-compose up -d vector-api python-etl service-discovery
```

### Scale Services

```bash
docker-compose up -d --scale python-etl=3 --scale vector-api=2
```

### Verify Architecture

```bash
./scripts/microservices/verify_architecture.sh
```

## Network Configuration

### Docker Network
- **Name**: `kettler-network`
- **Type**: Bridge
- **Purpose**: Inter-service communication
- **Isolation**: Services can only communicate within network

### Service URLs
- Services use service names as hostnames
- Ports are internal to network
- External ports only for APIs

## Dependencies

### Startup Order
1. Base services (python-etl, r-analysis)
2. Dependent services (vector-api, r-api)
3. Service discovery (monitors all)

### Health Check Dependencies
- `vector-api` waits for `python-etl` to be healthy
- `r-api` waits for `r-analysis` to be healthy
- `service-discovery` waits for APIs to start

## Monitoring

### Service Status
```bash
docker-compose ps
```

### Health Checks
```bash
docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Health}}"
```

### Logs
```bash
docker-compose logs -f service-name
```

### Resource Usage
```bash
docker stats
```

## Best Practices

1. **Service Independence**: Each service is independent and can be scaled separately
2. **Health Checks**: All services have health check endpoints
3. **Service Discovery**: Use service discovery for inter-service communication
4. **Error Handling**: Services handle failures gracefully
5. **Resource Limits**: Each service has defined resource limits
6. **Network Isolation**: Services communicate only through defined network

## Troubleshooting

### Service Not Starting
```bash
# Check logs
docker-compose logs service-name

# Check health
docker-compose ps

# Restart service
docker-compose restart service-name
```

### Service Discovery Not Working
```bash
# Check service discovery
curl http://localhost:8080/health

# Check registered services
curl http://localhost:8080/api/v1/services
```

### Inter-Service Communication Issues
```bash
# Test from within container
docker-compose exec vector-api curl http://python-etl:8000/health

# Check network
docker network inspect kettler-network
```

## Next Steps

1. **Add API Gateway**: For unified API access
2. **Add Load Balancer**: For high availability
3. **Add Message Queue**: For async processing
4. **Add Monitoring**: Prometheus/Grafana integration
5. **Add Logging**: Centralized logging (ELK stack)
