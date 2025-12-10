# Deployment Guide

## Deployment Architecture

```mermaid
graph TB
    subgraph "Local Development"
        L1[Python venv]
        L2[Local API]
        L3[Local Web]
    end

    subgraph "Docker Deployment"
        D1[Docker Compose]
        D2[API Container]
        D3[Web Container]
        D4[Database Container]
    end

    subgraph "Kubernetes Deployment"
        K1[K8s Cluster]
        K2[API Pods]
        K3[Web Pods]
        K4[Service Mesh]
    end

    L1 --> L2
    L1 --> L3
    D1 --> D2
    D1 --> D3
    D1 --> D4
    K1 --> K2
    K1 --> K3
    K1 --> K4

    style L1 fill:#C8E6C9
    style D1 fill:#B3E5FC
    style K1 fill:#E1BEE7
```

## Deployment Flow

```mermaid
flowchart TD
    START([Start Deployment]) --> CHOOSE{Deployment Type}

    CHOOSE -->|Local| LOCAL[Local Setup]
    CHOOSE -->|Docker| DOCKER[Docker Setup]
    CHOOSE -->|Kubernetes| K8S[Kubernetes Setup]

    LOCAL --> L1[Install Dependencies]
    L1 --> L2[Configure .env]
    L2 --> L3[Run Services]

    DOCKER --> D1[Build Images]
    D1 --> D2[Configure docker-compose.yml]
    D2 --> D3[Start Containers]

    K8S --> K1[Apply Configs]
    K1 --> K2[Deploy Services]
    K2 --> K3[Configure Ingress]

    L3 --> VERIFY[Verify Deployment]
    D3 --> VERIFY
    K3 --> VERIFY

    VERIFY --> END([Deployment Complete])

    style START fill:#C8E6C9
    style LOCAL fill:#FFF9C4
    style DOCKER fill:#B3E5FC
    style K8S fill:#E1BEE7
    style END fill:#C8E6C9
```

## Local Deployment

```bash

# API
cd api && python server.py

# Web
cd web && npm run dev

# Pipeline
python bin/run_pipeline.py
```

## Docker Deployment

```mermaid
graph LR
    A[docker-compose.yml] --> B[Build Images]
    B --> C[Start Containers]
    C --> D[API:8000]
    C --> E[Web:3000]
    C --> F[Database]

    style A fill:#B3E5FC
    style D fill:#FFF9C4
    style E fill:#F8BBD0
    style F fill:#C8E6C9
```

```bash
make build
make up
make logs
```

## Kubernetes Deployment

```mermaid
graph TB
    subgraph "Kubernetes Cluster"
        K1[ConfigMaps] --> K2[Deployments]
        K2 --> K3[Services]
        K3 --> K4[Ingress]
        K2 --> K5[Persistent Volumes]
    end

    K4 --> EXT[External Access]

    style K1 fill:#E1BEE7
    style K2 fill:#FFF9C4
    style K3 fill:#B3E5FC
    style K4 fill:#F8BBD0
    style K5 fill:#C8E6C9
```

```bash
kubectl apply -f kubernetes/
```

## Environment Configuration

```mermaid
mindmap
  root((Environment Config))
    Required
      GOOGLE_APPLICATION_CREDENTIALS
      GCP_PROJECT_ID
    Optional
      HUGGINGFACE_TOKEN
      OPENAI_API_KEY
    Files
      .env
      config/
      docker-compose.yml
```

- `.env` - Environment variables
- `config/` - Configuration files
- `docker-compose.yml` - Docker setup

## Service Ports

```mermaid
graph LR
    A[API Server] -->|8000| B[FastAPI]
    C[Web Frontend] -->|3000| D[React]
    E[Vector API] -->|8001| F[Vector Service]

    style A fill:#B3E5FC
    style C fill:#F8BBD0
    style E fill:#FFF9C4
```

- **API:** `http://localhost:8000`
- **Web:** `http://localhost:3000`
- **Vector API:** `http://localhost:8001` (if running)
