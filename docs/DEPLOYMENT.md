# Deployment

## Local

```bash
# API
cd api && python server.py

# Web
cd web && npm run dev

# Pipeline
python bin/run_pipeline.py
```

## Docker

```bash
make build
make up
make logs
```

## Kubernetes

```bash
kubectl apply -f kubernetes/
```

## Environment

- `.env` - Environment variables
- `config/` - Configuration files
- `docker-compose.yml` - Docker setup
