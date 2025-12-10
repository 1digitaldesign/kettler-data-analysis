# Microservices Architecture

This directory contains microservices infrastructure for the Kettler Data Analysis system.

## Components

### Service Discovery (`service_discovery.py`)
- Centralized service registry
- Health monitoring
- Service URL resolution
- REST API for service discovery

### Service Client (`service_client.py`)
- Inter-service communication helper
- Service URL resolution
- HTTP client wrapper
- Health checking

### Health Monitor (`health_monitor.py`)
- Monitors all services
- Reports health status
- Watch mode for continuous monitoring
- JSON output support

### Startup Check (`startup_check.sh`)
- Ensures dependencies are available
- Waits for required services
- Validates configuration

## Usage

### Service Discovery

```bash
# Start service discovery
docker-compose up -d service-discovery

# List all services
curl http://localhost:8080/api/v1/services

# Get specific service
curl http://localhost:8080/api/v1/services/vector-api

# Get service URL
curl http://localhost:8080/api/v1/services/vector-api/url
```

### Health Monitoring

```bash
# One-time check
python scripts/microservices/health_monitor.py

# Watch mode
python scripts/microservices/health_monitor.py --watch

# JSON output
python scripts/microservices/health_monitor.py --json
```

### Inter-Service Communication

```python
from scripts.microservices.service_client import get_service_client

client = get_service_client()

# Call a service
result = client.call_service('vector-api', '/api/v1/stats')

# Check service health
is_healthy = client.is_service_healthy('vector-api')
```

## Service Architecture

```
┌─────────────────────┐
│  Service Discovery  │ (Port 8080)
│  - Registry         │
│  - Health Monitor   │
└─────────────────────┘
         │
         ├─────────────────┬─────────────────┬─────────────────┐
         │                 │                 │                 │
┌────────▼────────┐  ┌─────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
│  Vector API     │  │  R API     │  │ Python ETL  │  │ R Analysis  │
│  Port: 8000     │  │  Port: 8001│  │ Port: 8000  │  │ Port: 8001  │
└─────────────────┘  └────────────┘  └─────────────┘  └─────────────┘
```

## Features

- ✅ Service discovery
- ✅ Health monitoring
- ✅ Inter-service communication
- ✅ Automatic failover
- ✅ Service registration
- ✅ Health checks
- ✅ Dependency management
