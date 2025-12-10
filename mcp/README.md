# MCP Configuration for Google Drive

## Overview

This directory contains MCP (Model Context Protocol) server configuration and tools for Google Drive integration.

## Files

- `mcp_config.json` - Main MCP server configuration
- `google_drive_tools.json` - Tool definitions for Google Drive operations
- `../scripts/mcp/google_drive_mcp_server.py` - MCP server implementation

## Available Tools

### 1. `list_drive_folder`
List all files and folders in a Google Drive folder.

**Parameters:**
- `folder_id` (required): Google Drive folder ID

**Example:**
```json
{
  "method": "list_drive_folder",
  "params": {
    "folder_id": "1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8"
  }
}
```

### 2. `get_drive_file_info`
Get metadata for a Google Drive file.

**Parameters:**
- `file_id` (required): Google Drive file ID

### 3. `download_drive_file`
Download a file from Google Drive.

**Parameters:**
- `file_id` (required): Google Drive file ID
- `output_path` (optional): Local path to save the file

### 4. `export_google_doc`
Export a Google Doc to specified format.

**Parameters:**
- `file_id` (required): Google Drive file ID
- `output_path` (required): Local path to save the exported file
- `format` (optional): Export format (docx, pdf, txt, html, rtf) - default: docx

### 5. `export_google_sheet`
Export a Google Sheet to specified format.

**Parameters:**
- `file_id` (required): Google Drive file ID
- `output_path` (required): Local path to save the exported file
- `format` (optional): Export format (xlsx, csv, pdf, ods, tsv) - default: xlsx

### 6. `download_drive_folder`
Download all files from a Google Drive folder recursively.

**Parameters:**
- `folder_id` (required): Google Drive folder ID
- `output_dir` (optional): Local directory to save files - default: data/drive_downloads
- `recursive` (optional): Download subfolders recursively - default: true

### 7. `search_drive_files`
Search for files in Google Drive by name or query.

**Parameters:**
- `query` (required): Search query (file name or Drive search syntax)
- `folder_id` (optional): Limit search to specific folder

## Usage

### Testing MCP Server

```bash
python scripts/mcp/google_drive_mcp_server.py
```

### Using with MCP Client

The MCP server can be used with any MCP-compatible client. The server handles JSON-RPC style requests.

**Example Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "list_drive_folder",
  "params": {
    "folder_id": "1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8"
  }
}
```

**Example Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "folder_id": "1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8",
    "items": [...],
    "count": 1
  }
}
```

## Configuration

The MCP server uses the same GCP credentials as the main application:
- Credentials file: `config/gcp-credentials.json`
- Project ID: `claude-eval-20250615`
- Region: `us-central1`

## Integration

The MCP server integrates with:
- Google Drive API client (`scripts/microservices/google_drive_client.py`)
- GCP authentication (`scripts/microservices/gcp_auth.py`)
- Docker service (`drive-api` on port 8084)

## Target Folder

Default folder ID: `1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8`
Folder name: `Tai_v_Kettler_Master`
