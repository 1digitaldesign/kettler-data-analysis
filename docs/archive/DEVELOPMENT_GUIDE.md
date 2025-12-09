# Development Guide

## Overview

This guide covers development workflows, best practices, and advanced features for the Kettler Data Analysis Docker/Kubernetes setup.

## Quick Start

### 1. Start Services

```bash
# Start all services
make up

# Start specific services
docker-compose up -d python-etl vector-api

# Start with custom configuration
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

### 2. Check Health

```bash
# Using health check script
python3 scripts/monitoring/health_check.py

# Using monitoring script
./scripts/monitoring/service_monitor.sh

# Manual check
curl http://localhost:8000/health
```

### 3. Run ETL Pipeline

```bash
# Using example script
./scripts/examples/run_etl_example.sh

# Direct execution
docker-compose exec python-etl python scripts/etl/etl_pipeline.py

# Run in new container
docker-compose run --rm python-etl python scripts/etl/etl_pipeline.py
```

## Development Workflows

### Local Development

1. **Make Changes**: Edit code in your local directory
2. **Test Locally**: Run scripts directly or in containers
3. **Rebuild Images**: Only when dependencies change
   ```bash
   docker-compose build python-etl
   ```

### Testing

```bash
# Run health checks
python3 scripts/monitoring/health_check.py

# Test Vector API
./scripts/examples/query_vector_example.sh

# Test parallel execution
./scripts/examples/parallel_execution_example.sh
```

### Debugging

```bash
# View logs
docker-compose logs -f python-etl

# Execute commands in container
docker-compose exec python-etl /bin/bash

# Check service status
./scripts/monitoring/service_monitor.sh
```

## Advanced Features

### Parallel Execution

```bash
# Scale services
make scale-etl REPLICAS=5
make scale-analysis REPLICAS=3

# Or directly
docker-compose up -d --scale python-etl=5 --scale r-analysis=3

# Run parallel tasks
./scripts/examples/parallel_execution_example.sh
```

### Custom Configuration

1. Copy override example:
   ```bash
   cp docker-compose.override.yml.example docker-compose.override.yml
   ```

2. Edit `docker-compose.override.yml` with your settings

3. Start services:
   ```bash
   docker-compose up -d
   ```

### Monitoring

```bash
# Health check (JSON output)
python3 scripts/monitoring/health_check.py --json

# Service monitor
./scripts/monitoring/service_monitor.sh

# Resource usage
docker stats
```

## Utility Scripts

### Docker Utils

Source the utility functions:
```bash
source scripts/utils/docker_utils.sh

# Use functions
wait_for_service vector-api http://localhost:8000/health
scale_service python-etl 5
show_status
```

### Example Scripts

- `scripts/examples/run_etl_example.sh` - Run ETL pipeline
- `scripts/examples/query_vector_example.sh` - Query vector API
- `scripts/examples/parallel_execution_example.sh` - Parallel execution demo

## Best Practices

### 1. Resource Management

- Set appropriate resource limits in `docker-compose.yml`
- Monitor resource usage: `docker stats`
- Scale based on load, not preemptively

### 2. Logging

- Use structured logging in applications
- Rotate logs regularly
- Monitor log sizes: `docker-compose logs --tail=100`

### 3. Health Checks

- Implement health check endpoints
- Use health checks in docker-compose
- Monitor health regularly

### 4. Security

- Don't commit secrets to git
- Use environment variables for sensitive data
- Keep images updated
- Use non-root users in containers

### 5. Performance

- Use volume mounts for data persistence
- Optimize Dockerfile layers
- Use multi-stage builds for smaller images
- Cache dependencies appropriately

## Troubleshooting

### Services Not Starting

```bash
# Check logs
docker-compose logs service-name

# Check resource availability
docker stats

# Restart service
docker-compose restart service-name
```

### Port Conflicts

```bash
# Check what's using the port
lsof -i :8000

# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Host:Container
```

### Volume Mount Issues

```bash
# Check volume mounts
docker inspect container-name | grep Mounts

# Verify permissions
docker-compose exec python-etl ls -la /app/data
```

## CI/CD Integration

### GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/docker-build.yml`) that:
- Builds Docker images on push/PR
- Tests image functionality
- Validates dependencies

### Local CI Testing

```bash
# Test build process
docker build -f docker/python-etl/Dockerfile -t test-image .

# Test run
docker run --rm test-image python --version
```

## Production Deployment

### Pre-Deployment Checklist

- [ ] All services health checks passing
- [ ] Resource limits configured
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] Security review completed

### Deployment Steps

1. **Build Images**:
   ```bash
   docker-compose build
   ```

2. **Test Locally**:
   ```bash
   docker-compose up -d
   python3 scripts/monitoring/health_check.py
   ```

3. **Deploy to Production**:
   ```bash
   # Using Kubernetes
   kubectl apply -f kubernetes/

   # Or Docker Compose
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

## Performance Tuning

### Optimize Dockerfile

- Order Dockerfile commands by change frequency
- Use multi-stage builds
- Minimize layers
- Use .dockerignore

### Optimize Compose

- Use named volumes for data
- Set appropriate resource limits
- Use health checks
- Configure restart policies

## Next Steps

1. Set up monitoring (Prometheus, Grafana)
2. Implement auto-scaling
3. Add service mesh (Istio, Linkerd)
4. Set up CI/CD pipeline
5. Configure backup/restore
