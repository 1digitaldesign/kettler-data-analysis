# Google Drive Service

Microservice for Google Drive operations in the Kettler Data Analysis system.

## Features

- **Read Operations:**
  - List folder contents
  - Download files from Google Drive
  - Export Google Docs/Sheets to various formats (PDF, DOCX, CSV, etc.)
  - Get file information

- **Write Operations (CRUD):**
  - Create files (from content or file path)
  - Update files (metadata and/or content)
  - Delete files
  - Move files between folders
  - Copy files

- **Additional Features:**
  - Full input validation
  - Redundancy and fallback mechanisms
  - Service account authentication with write access

## Endpoints

### List Folder
`POST /drive/list`
- List contents of a Google Drive folder
- Supports filtering files/folders
- Configurable max results

### Download File
`POST /drive/download`
- Download any file from Google Drive
- Supports custom output paths

### Export File
`POST /drive/export`
- Export Google Docs/Sheets to different formats
- Supported formats: PDF, DOCX, TXT, HTML, RTF, XLSX, CSV, ODS, TSV

### Get File Info
`GET /drive/info/{file_id}`
- Get metadata for a file
- Returns name, size, MIME type, timestamps, etc.

### Create File
`POST /drive/create`
- Create a new file in Google Drive
- Supports content string or file path upload
- Can specify parent folder

### Update File
`PUT /drive/update`
- Update file metadata and/or content
- Supports partial updates

### Delete File
`DELETE /drive/delete/{file_id}`
- Delete a file from Google Drive
- Returns confirmation

### Move File
`POST /drive/move`
- Move file to different folder
- Can remove from previous folder or keep in both

### Copy File
`POST /drive/copy`
- Create a copy of a file
- Can rename and move to different folder

## Setup

### 1. Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Drive API
4. Create OAuth 2.0 credentials
5. Download credentials JSON file

### 2. Authentication

Place credentials file as `credentials.json` in the service directory.

On first run, the service will:
1. Open browser for OAuth authentication
2. Save token to `token.pickle`
3. Use saved token for subsequent requests

### 3. Environment Variables

```bash
GOOGLE_DRIVE_TOKEN_FILE=/path/to/token.pickle
GOOGLE_DRIVE_CREDENTIALS_FILE=/path/to/credentials.json
PORT=8008
```

## Usage Examples

### List Folder Contents

```python
import requests

response = requests.post("http://localhost:8008/drive/list", json={
    "folder_id": "1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8",
    "include_files": True,
    "include_folders": True,
    "max_results": 100
})

print(response.json())
```

### Download File

```python
response = requests.post("http://localhost:8008/drive/download", json={
    "file_id": "file_id_here",
    "output_path": "/tmp/downloaded_file.pdf"
})
```

### Export Google Doc to PDF

```python
response = requests.post("http://localhost:8008/drive/export", json={
    "file_id": "google_doc_id",
    "format": "pdf",
    "output_path": "/tmp/exported.pdf"
})
```

## Integration with API Gateway

The service is automatically integrated with the API Gateway:

- `/api/drive/list` → Google Drive Service
- `/api/drive/download` → Google Drive Service
- `/api/drive/export` → Google Drive Service
- `/api/drive/info/{file_id}` → Google Drive Service

## Security

- Full read/write access (OAuth scope: `drive`)
- Input validation on all endpoints
- Sanitization of file paths
- Error handling prevents information leakage
- Service account authentication

## Testing

```bash
# Run tests
pytest tests/test_google_drive_service.py -v

# Test with mocked Google Drive API
pytest tests/test_google_drive_service.py::TestGoogleDriveServiceEndpoints -v
```

## Error Handling

The service includes:
- Input validation
- Redundancy mechanisms (retry, circuit breaker, timeout)
- Graceful degradation
- Comprehensive error messages

## Limitations

- Read-only access (no file upload/modification)
- Requires OAuth authentication
- Token refresh handled automatically
- Rate limits apply per Google Drive API quotas
