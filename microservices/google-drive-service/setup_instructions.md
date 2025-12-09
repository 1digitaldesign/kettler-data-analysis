# Google Drive Service Setup Instructions

## Authentication Methods

The service supports two authentication methods:

### 1. Service Account (Recommended for Production)

The service will automatically use the service account credentials from `config/gcp-credentials.json` if available.

**Setup:**
1. The credentials file is already at `config/gcp-credentials.json`
2. Grant the service account access to the Google Drive folder:
   - Open Google Drive
   - Right-click the folder → Share
   - Add email: `fraud-analysis@claude-eval-20250615.iam.gserviceaccount.com`
   - Grant "Viewer" access
3. The service will automatically use these credentials

**Environment Variable:**
```bash
GOOGLE_APPLICATION_CREDENTIALS=/path/to/config/gcp-credentials.json
```

### 2. OAuth 2.0 (For Development/User Access)

If service account is not available, the service falls back to OAuth 2.0.

**Setup:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select project: `claude-eval-20250615`
3. Enable Google Drive API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download as `credentials.json` in `microservices/google-drive-service/`
6. On first run, browser will open for authentication
7. Token saved to `token.pickle` for future use

## Current Configuration

The service is configured to use:
- **Service Account**: `config/gcp-credentials.json`
- **Service Account Email**: `fraud-analysis@claude-eval-20250615.iam.gserviceaccount.com`
- **Project**: `claude-eval-20250615`

## Testing

To test the service with the folder you mentioned:

```python
import requests

# List folder contents
response = requests.post("http://localhost:8008/drive/list", json={
    "folder_id": "1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8",
    "include_files": True,
    "include_folders": True,
    "max_results": 100
})

print(response.json())
```

## Troubleshooting

### Service Account Not Working

1. Verify service account has access to the folder
2. Check that `config/gcp-credentials.json` exists and is valid
3. Ensure Google Drive API is enabled in the project

### OAuth Not Working

1. Verify `credentials.json` exists in service directory
2. Check OAuth consent screen is configured
3. Ensure redirect URIs are set correctly

### Both Methods Fail

The service will return 503 if neither authentication method works. Check logs for specific error messages.
