# Kubernetes Configuration

Kubernetes manifests for deploying Kettler Data Analysis services in a Kubernetes cluster.

## Prerequisites

- Kubernetes cluster (Docker Desktop, minikube, or cloud provider)
- kubectl configured
- Persistent volumes configured

## Structure

```
kubernetes/
├── python-etl-deployment.yaml    # Python ETL service
├── r-analysis-deployment.yaml    # R analysis service
├── vector-api-deployment.yaml     # Vector API service
├── persistent-volumes.yaml        # PVC definitions
└── configmap.yaml                 # ConfigMap for scripts
```

## Deployment

### 1. Create Persistent Volumes

```bash
kubectl apply -f kubernetes/persistent-volumes.yaml
```

### 2. Create ConfigMap (if needed)

```bash
kubectl create configmap kettler-scripts-config --from-file=scripts/
```

### 3. Deploy Services

```bash
# Deploy Python ETL (2 replicas)
kubectl apply -f kubernetes/python-etl-deployment.yaml

# Deploy R Analysis (3 replicas)
kubectl apply -f kubernetes/r-analysis-deployment.yaml

# Deploy Vector API (2 replicas)
kubectl apply -f kubernetes/vector-api-deployment.yaml
```

### 4. Scale Services

```bash
# Scale Python ETL to 5 replicas
kubectl scale deployment python-etl --replicas=5

# Scale R Analysis to 4 replicas
kubectl scale deployment r-analysis --replicas=4
```

## Parallel Execution

Services are configured for parallel execution:

- **python-etl**: 2 replicas (scalable)
- **r-analysis**: 3 replicas (scalable)
- **vector-api**: 2 replicas (load balanced)

## Monitoring

```bash
# Check pod status
kubectl get pods -l app=python-etl

# View logs
kubectl logs -l app=python-etl --tail=100

# Describe deployment
kubectl describe deployment python-etl

# Check service endpoints
kubectl get svc python-etl-service
```

## Resource Management

Each deployment has resource limits:
- **CPU**: 0.5-2 cores
- **Memory**: 1-4GB

Adjust in deployment YAML files as needed.

## Persistent Storage

Services use PersistentVolumeClaims:
- `kettler-data-pvc`: 50GB for data
- `kettler-research-pvc`: 20GB for research
- `kettler-evidence-pvc`: 30GB for evidence
- `kettler-outputs-pvc`: 10GB for outputs

## Networking

Services communicate via ClusterIP services:
- `python-etl-service`: Port 8000
- `r-analysis-service`: Port 8001
- `vector-api-service`: Port 8000 (LoadBalancer)

## Cleanup

```bash
# Delete deployments
kubectl delete -f kubernetes/python-etl-deployment.yaml
kubectl delete -f kubernetes/r-analysis-deployment.yaml
kubectl delete -f kubernetes/vector-api-deployment.yaml

# Delete PVCs (optional)
kubectl delete -f kubernetes/persistent-volumes.yaml
```

## Docker Desktop Integration

For Docker Desktop Kubernetes:

1. Enable Kubernetes in Docker Desktop settings
2. Ensure context is set: `kubectl config use-context docker-desktop`
3. Deploy as above

## Cloud Provider Deployment

For cloud providers (GKE, EKS, AKS):

1. Configure kubectl for your cluster
2. Adjust storage classes in `persistent-volumes.yaml`
3. Deploy as above
4. Configure LoadBalancer services for external access
