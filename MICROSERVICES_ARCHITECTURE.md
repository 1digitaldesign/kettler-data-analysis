# Microservices Architecture

## Services

- **API Gateway** - Centralized routing, authentication
- **Analysis Service** - Distributed analysis processing
- **Google Drive Service** - File access and processing

## Deployment

```bash
make build    # Build images
make up       # Start services
make logs     # View logs
```

## Configuration

- Docker Compose for local development
- Kubernetes for production
- Environment variables via `.env`

## API

- REST endpoints via FastAPI
- API Gateway routes requests
- Circuit breakers for resilience
