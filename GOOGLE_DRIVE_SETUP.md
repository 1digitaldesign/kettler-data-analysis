# Google Drive API Setup

## Overview

This project is configured to access Google Drive files, documents, and spreadsheets using the Google Drive API.

## Configuration

### Service Account Permissions

The service account (`fraud-analysis@claude-eval-20250615.iam.gserviceaccount.com`) needs:
1. **Drive API enabled** in the GCP project
2. **Access to the target folder** - The folder owner needs to share the folder with the service account email

### Sharing Folder with Service Account

To access the folder `1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8`:

1. Open the folder in Google Drive
2. Click "Share" button
3. Add the service account email: `fraud-analysis@claude-eval-20250615.iam.gserviceaccount.com`
4. Grant "Viewer" or "Editor" permissions
5. Click "Send"

## Usage

### Command Line

```bash
# List files in folder
python scripts/microservices/download_drive_folder.py 1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8 --list-only

# Download all files
python scripts/microservices/download_drive_folder.py 1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8 --output data/drive_downloads --recursive
```

### Python Code

```python
from scripts.microservices.google_drive_client import get_drive_client

# Get client
client = get_drive_client()

# List folder contents
items = client.list_folder_contents('1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8')

# Download a file
content = client.download_file(file_id, 'output/path/file.docx')

# Export Google Doc
client.export_google_doc(file_id, 'output/path/file.docx', format='docx')

# Export Google Sheet
client.export_google_sheet(file_id, 'output/path/file.xlsx', format='xlsx')

# Download entire folder
downloaded_files = client.download_folder('1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8', 'output/dir', recursive=True)
```

### REST API

The Drive API service runs on port 8084:

```bash
# Health check
curl http://localhost:8084/health

# List folder contents
curl http://localhost:8084/api/v1/drive/folder/1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8/list

# Get file info
curl http://localhost:8084/api/v1/drive/file/{file_id}/info

# Download file
curl http://localhost:8084/api/v1/drive/file/{file_id}/download -o file.docx

# Export Google Doc
curl "http://localhost:8084/api/v1/drive/file/{file_id}/export?format=docx" -o file.docx

# Download folder
curl -X POST http://localhost:8084/api/v1/drive/folder/1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8/download \
  -H "Content-Type: application/json" \
  -d '{"output_dir": "data/drive_downloads", "recursive": true}'
```

## Supported File Types

### Google Workspace Files
- **Google Docs** → Export as: .docx, .pdf, .txt, .html, .rtf
- **Google Sheets** → Export as: .xlsx, .csv, .pdf, .ods, .tsv
- **Google Slides** → Export as: .pptx, .pdf
- **Google Drawings** → Export as: .png

### Regular Files
- PDFs
- Images
- Text files
- Any file stored in Drive

## Docker Service

The Drive API service is available as a Docker service:

```bash
# Start service
docker-compose up -d drive-api

# Check logs
docker-compose logs -f drive-api

# Test health
curl http://localhost:8084/health
```

## Troubleshooting

### "Permission Denied" Error

1. Ensure the folder is shared with the service account email
2. Check that Drive API is enabled in GCP Console
3. Verify service account has necessary IAM roles

### "API Not Enabled" Error

1. Go to GCP Console → APIs & Services → Library
2. Search for "Google Drive API"
3. Click "Enable"

### "File Not Found" Error

1. Verify the folder/file ID is correct
2. Ensure the service account has access to the file/folder
3. Check that the file hasn't been deleted or moved

## Security Notes

- Service account credentials are stored securely in `config/gcp-credentials.json`
- Only read-only access is requested by default
- Files are downloaded to local `data/drive_downloads/` directory
- Downloaded files are not automatically committed to git

## Target Folder

**Folder ID**: `1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8`
**Folder Name**: `Tai_v_Kettler_Master`

Make sure this folder is shared with: `fraud-analysis@claude-eval-20250615.iam.gserviceaccount.com`
