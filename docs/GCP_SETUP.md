# GCP and Vertex AI Setup

## Overview

This project is configured to use Google Cloud Platform (GCP) services including Vertex AI for machine learning and AI capabilities.

## Configuration

### Credentials File

The GCP service account credentials are stored at:
```
config/gcp-credentials.json
```

**⚠️ Important**: This file is gitignored and should NOT be committed to the repository.

### Environment Variables

Add the following to your `.env` file:

```bash
# GCP Project ID
GCP_PROJECT_ID=claude-eval-20250615

# GCP Region (default: us-central1)
GCP_REGION=us-central1

# Optional: GCP Credentials as JSON string (if not using file)
# GCP_CREDENTIALS_JSON={"type":"service_account",...}
```

### Docker Configuration

The `docker-compose.yml` file automatically:
- Mounts the `config/` directory to `/app/config` in containers
- Sets `GOOGLE_APPLICATION_CREDENTIALS=/app/config/gcp-credentials.json`
- Passes GCP environment variables to all services

## Services Configured

All microservices have access to GCP credentials:
- ✅ Python ETL Service
- ✅ Vector API Service
- ✅ Service Discovery
- ✅ API Gateway
- ✅ Message Queue
- ✅ Metrics Collector

## Usage

### Python Code

```python
from scripts.microservices.gcp_auth import setup_gcp_auth, get_gcp_project_id
from scripts.microservices.vertex_ai_client import get_vertex_ai_client

# Setup authentication
setup_gcp_auth()

# Get project ID
project_id = get_gcp_project_id()

# Use Vertex AI client
client = get_vertex_ai_client()
if client:
    models = client.list_models()
    # Use Vertex AI services...
```

### Environment Variables

The following environment variables are available in all containers:

- `GOOGLE_APPLICATION_CREDENTIALS` - Path to credentials file
- `GCP_PROJECT_ID` - GCP project ID
- `GCP_REGION` - GCP region (default: us-central1)
- `GCP_CLIENT_EMAIL` - Service account email
- `GCP_CLIENT_ID` - Service account client ID

## Vertex AI Features

The project includes a Vertex AI client (`scripts/microservices/vertex_ai_client.py`) that provides:

- Model listing
- Prediction endpoints
- Endpoint management

## Required Python Packages

The following packages are installed via `requirements.txt`:

- `google-cloud-aiplatform>=1.38.0` - Vertex AI SDK
- `google-cloud-storage>=2.10.0` - Cloud Storage
- `google-auth>=2.23.0` - Authentication
- `google-auth-oauthlib>=1.1.0` - OAuth2
- `google-auth-httplib2>=0.1.1` - HTTP transport

## Verification

Test GCP configuration:

```bash
# Test authentication
python scripts/microservices/gcp_auth.py

# Test Vertex AI client
python scripts/microservices/vertex_ai_client.py
```

## Security Notes

1. **Never commit credentials**: The `config/gcp-credentials.json` file is gitignored
2. **Use service accounts**: The credentials use a service account, not user credentials
3. **Limit permissions**: Ensure the service account has only necessary permissions
4. **Rotate credentials**: Regularly rotate service account keys

## Troubleshooting

### Credentials Not Found

If you see "GCP credentials not found":
1. Ensure `config/gcp-credentials.json` exists
2. Check file permissions (should be readable)
3. Verify `GOOGLE_APPLICATION_CREDENTIALS` environment variable

### Vertex AI Not Available

If Vertex AI libraries are not available:
```bash
pip install google-cloud-aiplatform google-cloud-storage google-auth
```

### Authentication Errors

If you get authentication errors:
1. Verify the service account has necessary permissions
2. Check that the project ID matches your GCP project
3. Ensure the credentials file is valid JSON

## Next Steps

1. Configure Vertex AI endpoints/models as needed
2. Set up GCP resources (Cloud Storage buckets, etc.)
3. Configure IAM permissions for the service account
4. Test Vertex AI integration with your models
