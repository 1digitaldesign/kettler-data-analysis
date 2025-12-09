#!/bin/bash
# Deployment script for microservices to GCP Cloud Run

set -e

PROJECT_ID=${GCP_PROJECT_ID:-"your-project-id"}
REGION=${GCP_REGION:-"us-central1"}

echo "Deploying microservices to GCP Cloud Run..."
echo "Project: $PROJECT_ID"
echo "Region: $REGION"

# Build and deploy each service
SERVICES=(
    "api-gateway:8000"
    "analysis-service:8001"
    "scraping-service:8002"
    "validation-service:8003"
    "vector-service:8004"
    "gis-service:8005"
    "acris-service:8006"
    "data-service:8007"
)

for service_port in "${SERVICES[@]}"; do
    IFS=':' read -r service port <<< "$service_port"
    echo ""
    echo "Building $service..."

    # Build Docker image
    docker build -t gcr.io/$PROJECT_ID/$service -f Dockerfile \
        --build-arg SERVICE=$service \
        --build-arg PORT=$port .

    # Push to Container Registry
    docker push gcr.io/$PROJECT_ID/$service

    # Deploy to Cloud Run
    echo "Deploying $service to Cloud Run..."
    gcloud run deploy $service \
        --image gcr.io/$PROJECT_ID/$service \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated \
        --memory 2Gi \
        --cpu 2 \
        --timeout 300 \
        --max-instances 10 \
        --set-env-vars "PORT=$port"

    # Get service URL
    SERVICE_URL=$(gcloud run services describe $service --region $REGION --format 'value(status.url)')
    echo "$service deployed at: $SERVICE_URL"
done

echo ""
echo "All services deployed successfully!"
echo ""
echo "Update your API Gateway environment variables with the service URLs:"
echo "ANALYSIS_SERVICE_URL=https://analysis-service-xxx.run.app"
echo "SCRAPING_SERVICE_URL=https://scraping-service-xxx.run.app"
echo "VALIDATION_SERVICE_URL=https://validation-service-xxx.run.app"
echo "VECTOR_SERVICE_URL=https://vector-service-xxx.run.app"
echo "GIS_SERVICE_URL=https://gis-service-xxx.run.app"
echo "ACRIS_SERVICE_URL=https://acris-service-xxx.run.app"
echo "DATA_SERVICE_URL=https://data-service-xxx.run.app"
