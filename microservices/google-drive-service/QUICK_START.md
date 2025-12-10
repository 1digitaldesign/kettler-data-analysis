# Google Drive Service - Quick Start

## Step 1: Grant Service Account Access

Run the helper script to get instructions:

```bash
python microservices/google-drive-service/grant_access.py
```

Or manually:

1. **Open the folder in Google Drive:**
   ```
   https://drive.google.com/drive/folders/1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8
   ```

2. **Click "Share" button** (top right)

3. **Add this email:**
   ```
   fraud-analysis@claude-eval-20250615.iam.gserviceaccount.com
   ```

4. **Set permission:** Viewer (read-only)

5. **Uncheck "Notify people"** (optional)

6. **Click "Share"**

## Step 2: Start the Service

```bash
# Using docker-compose
cd microservices
docker-compose up google-drive-service

# OR run directly
cd microservices/google-drive-service
python -m uvicorn main:app --port 8008
```

## Step 3: Test Access

```bash
# Test access
python microservices/google-drive-service/test_access.py

# OR test manually
curl -X POST http://localhost:8008/drive/list \
  -H "Content-Type: application/json" \
  -d '{
    "folder_id": "1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8",
    "include_files": true,
    "include_folders": true,
    "max_results": 100
  }'
```

## Step 4: Use via API Gateway

Once the service is running, access it through the API Gateway:

```bash
curl -X POST http://localhost:8000/api/drive/list \
  -H "Content-Type: application/json" \
  -d '{
    "folder_id": "1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8"
  }'
```

## Troubleshooting

### Service Account Not Found
- Verify `config/gcp-credentials.json` exists
- Check that the file contains valid JSON

### Access Denied (403)
- Ensure you've granted access to the service account email
- Wait a few minutes for permissions to propagate
- Try refreshing the folder in Google Drive

### Service Not Running
- Check logs: `docker-compose logs google-drive-service`
- Verify port 8008 is available
- Check environment variables are set correctly
