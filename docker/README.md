# Docker Configuration

This directory contains Docker configurations for containerizing the Kettler Data Analysis services.

## Structure

```
docker/
├── python-etl/
│   └── Dockerfile          # Python ETL service
├── r-analysis/
│   └── Dockerfile          # R analysis service
└── mcp/
    └── docker-mcp-server.py # Docker MCP server
```

## Building Images

### Python ETL Service

```bash
docker build -f docker/python-etl/Dockerfile -t kettler-python-etl:latest .
```

### R Analysis Service

```bash
docker build -f docker/r-analysis/Dockerfile -t kettler-r-analysis:latest .
```

## Running with Docker Compose

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d python-etl

# Scale services for parallel execution
docker-compose up -d --scale python-etl=3 --scale r-analysis=2

# View logs
docker-compose logs -f python-etl

# Stop services
docker-compose down
```

## Docker MCP Integration

The Docker MCP server provides programmatic control over containers:

```bash
# List containers
python docker/mcp/docker-mcp-server.py list

# Start service
python docker/mcp/docker-mcp-server.py start --service python-etl

# Scale service
python docker/mcp/docker-mcp-server.py scale --service python-etl --replicas 3

# Get status
python docker/mcp/docker-mcp-server.py status

# View logs
python docker/mcp/docker-mcp-server.py logs --service python-etl
```

## Parallel Execution

Services are configured to run in parallel:

- **Python ETL**: 2-3 replicas for parallel data processing
- **R Analysis**: 3 replicas for parallel analysis tasks
- **Vector API**: 2 replicas for load balancing
- **R API**: Single instance (can be scaled)

## Volume Mounts

All services share the following volumes:
- `./data` → `/app/data` - Data files
- `./research` → `/app/research` - Research outputs
- `./evidence` → `/app/evidence` - Evidence files
- `./scripts` → `/app/scripts` - Scripts directory

## Networking

All services run on the `kettler-network` bridge network for inter-service communication.

## Resource Limits

Default resource limits:
- **CPU**: 1-2 cores per service
- **Memory**: 2-4GB per service

Adjust in `docker-compose.yml` as needed.
