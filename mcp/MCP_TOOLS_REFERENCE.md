# MCP Tools Reference

## Overview

This document lists all available MCP (Model Context Protocol) tools for the Kettler Data Analysis project.

## Google Drive Tools

### 1. `list_drive_folder`
List all files and folders in a Google Drive folder.

**Parameters:**
- `folder_id` (string, required): Google Drive folder ID

**Example:**
```bash
make mcp-drive-list FOLDER_ID=1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8
```

**Python:**
```python
from scripts.mcp.google_drive_mcp_server import GoogleDriveMCPServer
server = GoogleDriveMCPServer()
result = server.list_drive_folder('1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8')
```

### 2. `get_drive_file_info`
Get metadata for a Google Drive file.

**Parameters:**
- `file_id` (string, required): Google Drive file ID

### 3. `download_drive_file`
Download a file from Google Drive.

**Parameters:**
- `file_id` (string, required): Google Drive file ID
- `output_path` (string, optional): Local path to save the file

### 4. `export_google_doc`
Export a Google Doc to specified format.

**Parameters:**
- `file_id` (string, required): Google Drive file ID
- `output_path` (string, required): Local path to save the exported file
- `format` (string, optional): Export format - docx, pdf, txt, html, rtf (default: docx)

**Example:**
```bash
make mcp-drive-export-doc FILE_ID=15ew6ZHO0IS0IxwDpNlAMNPEQ6zQhu5KC OUTPUT_PATH=data/drive_downloads/readme.docx FORMAT=docx
```

### 5. `export_google_sheet`
Export a Google Sheet to specified format.

**Parameters:**
- `file_id` (string, required): Google Drive file ID
- `output_path` (string, required): Local path to save the exported file
- `format` (string, optional): Export format - xlsx, csv, pdf, ods, tsv (default: xlsx)

**Example:**
```bash
make mcp-drive-export-sheet FILE_ID=... OUTPUT_PATH=data/drive_downloads/sheet.xlsx FORMAT=xlsx
```

### 6. `download_drive_folder`
Download all files from a Google Drive folder recursively.

**Parameters:**
- `folder_id` (string, required): Google Drive folder ID
- `output_dir` (string, optional): Local directory to save files (default: data/drive_downloads)
- `recursive` (boolean, optional): Download subfolders recursively (default: true)

**Example:**
```bash
make mcp-drive-download FOLDER_ID=1Vgd8zKV5u1HPcJ0axMugFPzjPONAMDly OUTPUT_DIR=data/drive_downloads/Tai_v_Kettler_Master
```

### 7. `search_drive_files`
Search for files in Google Drive by name or query.

**Parameters:**
- `query` (string, required): Search query (file name or Drive search syntax)
- `folder_id` (string, optional): Limit search to specific folder

## Docker Tools

### 1. `list_containers`
List Docker containers.

**Example:**
```bash
make mcp-list
```

### 2. `get_service_status`
Get service status.

**Example:**
```bash
make mcp-status
```

### 3. `scale_service`
Scale a Docker service.

**Parameters:**
- `service` (string, required): Service name
- `replicas` (integer, required): Number of replicas

**Example:**
```bash
make mcp-scale SERVICE=python-etl REPLICAS=3
```

## Default Folders

**Root Folder:**
- ID: `1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8`
- Name: Root folder

**Tai_v_Kettler_Master:**
- ID: `1Vgd8zKV5u1HPcJ0axMugFPzjPONAMDly`
- Contains: 20+ items including documents, spreadsheets, and subfolders

## Supported Export Formats

### Google Docs
- `.docx` - Microsoft Word format
- `.pdf` - PDF format
- `.txt` - Plain text
- `.html` - HTML format
- `.rtf` - Rich Text Format

### Google Sheets
- `.xlsx` - Microsoft Excel format
- `.csv` - Comma-separated values
- `.pdf` - PDF format
- `.ods` - OpenDocument Spreadsheet
- `.tsv` - Tab-separated values

### Google Slides
- `.pptx` - Microsoft PowerPoint format
- `.pdf` - PDF format

### Google Drawings
- `.png` - PNG image format

## Quick Reference

```bash
# List all MCP tools
make mcp-tools-list

# List Drive folder contents
make mcp-drive-list FOLDER_ID=1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8

# Download entire folder
make mcp-drive-download FOLDER_ID=1Vgd8zKV5u1HPcJ0axMugFPzjPONAMDly

# Export Google Doc
make mcp-drive-export-doc FILE_ID=... OUTPUT_PATH=... FORMAT=docx

# Export Google Sheet
make mcp-drive-export-sheet FILE_ID=... OUTPUT_PATH=... FORMAT=xlsx
```

## Configuration Files

- `mcp/mcp_config.json` - Main MCP server configuration
- `mcp/google_drive_tools.json` - Google Drive tool definitions
- `mcp/tools_list.json` - Complete tools list with metadata
- `scripts/mcp/google_drive_mcp_server.py` - MCP server implementation
