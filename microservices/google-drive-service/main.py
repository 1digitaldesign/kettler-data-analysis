#!/usr/bin/env python3
"""
Google Drive Microservice
Handles Google Drive operations (list, download, export)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Any, Optional
import sys
from pathlib import Path
import os
import logging

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.validation import (
    validate_string, validate_dict, ValidationError
)
from utils.redundancy import with_redundancy

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Google Drive Service",
    description="Microservice for Google Drive operations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Google Drive API client (will be initialized if credentials available)
drive_client = None

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload, MediaIoBaseUpload
from googleapiclient.errors import HttpError
import io
import pickle

    GOOGLE_DRIVE_AVAILABLE = True

    def initialize_drive_client():
        """Initialize Google Drive API client"""
        global drive_client

        SCOPES = ['https://www.googleapis.com/auth/drive']
        creds = None

        # Try service account first (from config/gcp-credentials.json)
        service_account_file = os.getenv(
            'GOOGLE_APPLICATION_CREDENTIALS',
            str(Path(__file__).parent.parent.parent / 'config' / 'gcp-credentials.json')
        )

        if os.path.exists(service_account_file):
            try:
                from google.oauth2 import service_account
                creds = service_account.Credentials.from_service_account_file(
                    service_account_file,
                    scopes=SCOPES
                )
                logger.info("Using service account credentials")
            except Exception as e:
                logger.warning(f"Could not use service account credentials: {e}")

        # Fallback to OAuth 2.0 if service account not available
        if not creds:
            token_file = os.getenv('GOOGLE_DRIVE_TOKEN_FILE', 'token.pickle')
            credentials_file = os.getenv(
                'GOOGLE_DRIVE_CREDENTIALS_FILE',
                str(Path(__file__).parent / 'credentials.json')
            )

            if os.path.exists(token_file):
                try:
                    with open(token_file, 'rb') as token:
                        creds = pickle.load(token)
                except Exception as e:
                    logger.warning(f"Could not load token file: {e}")

            # If there are no (valid) credentials available, try OAuth flow
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                    except Exception as e:
                        logger.warning(f"Could not refresh token: {e}")
                        creds = None

                if not creds:
                    if os.path.exists(credentials_file):
                        try:
                            flow = InstalledAppFlow.from_client_secrets_file(
                                credentials_file, SCOPES)
                            creds = flow.run_local_server(port=0)
                            # Save the credentials for the next run
                            with open(token_file, 'wb') as token:
                                pickle.dump(creds, token)
                        except Exception as e:
                            logger.warning(f"OAuth flow failed: {e}")
                            return None
                    else:
                        logger.warning("No Google Drive credentials found (neither service account nor OAuth)")
                        return None

        try:
            drive_client = build('drive', 'v3', credentials=creds)
            logger.info("Google Drive client initialized successfully")
            return drive_client
        except Exception as e:
            logger.error(f"Error initializing Google Drive client: {e}")
            return None

    # Try to initialize on startup
    drive_client = initialize_drive_client()

except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False
    logger.warning("Google Drive API libraries not available. Install with: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")


class ListFolderRequest(BaseModel):
    """List folder request model"""
    folder_id: str = Field(..., min_length=1, max_length=100)
    include_files: bool = True
    include_folders: bool = True
    max_results: int = Field(100, ge=1, le=1000)

    @validator('folder_id')
    def validate_folder_id(cls, v):
        return validate_string(v, "folder_id", min_length=1, max_length=100)


class DownloadFileRequest(BaseModel):
    """Download file request model"""
    file_id: str = Field(..., min_length=1, max_length=100)
    output_path: Optional[str] = None

    @validator('file_id')
    def validate_file_id(cls, v):
        return validate_string(v, "file_id", min_length=1, max_length=100)


class ExportFileRequest(BaseModel):
    """Export file request model"""
    file_id: str = Field(..., min_length=1, max_length=100)
    format: str = Field(..., min_length=1, max_length=20)
    output_path: Optional[str] = None

    @validator('file_id')
    def validate_file_id(cls, v):
        return validate_string(v, "file_id", min_length=1, max_length=100)

    @validator('format')
    def validate_format(cls, v):
        valid_formats = ['pdf', 'docx', 'txt', 'html', 'rtf', 'xlsx', 'csv', 'ods', 'tsv']
        if v.lower() not in valid_formats:
            raise ValueError(f"Format must be one of: {', '.join(valid_formats)}")
        return v.lower()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "google-drive",
        "google_drive_available": GOOGLE_DRIVE_AVAILABLE,
        "drive_client_initialized": drive_client is not None
    }


@with_redundancy(
    func_key="list_folder",
    cache_key=None,
    alternatives=None,
    fallback_func=lambda folder_id: {"status": "degraded", "items": [], "message": "Google Drive unavailable"}
)
@app.post("/drive/list")
async def list_folder(request: ListFolderRequest):
    """List folder contents"""
    if not drive_client:
        raise HTTPException(status_code=503, detail="Google Drive client not initialized")

    try:
        # Build query
        query_parts = [f"'{request.folder_id}' in parents"]

        if request.include_files and request.include_folders:
            pass  # Include both
        elif request.include_files:
            query_parts.append("mimeType != 'application/vnd.google-apps.folder'")
        elif request.include_folders:
            query_parts.append("mimeType = 'application/vnd.google-apps.folder'")

        query = " and ".join(query_parts)

        # List files
        results = drive_client.files().list(
            q=query,
            pageSize=request.max_results,
            fields="nextPageToken, files(id, name, mimeType, size, modifiedTime, createdTime)"
        ).execute()

        items = results.get('files', [])

        return {
            "status": "success",
            "folder_id": request.folder_id,
            "items": items,
            "count": len(items)
        }

    except Exception as e:
        logger.error(f"Error listing folder: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@with_redundancy(
    func_key="download_file",
    cache_key=None,
    alternatives=None,
    fallback_func=lambda file_id: {"status": "error", "message": "Download failed"}
)
@app.post("/drive/download")
async def download_file(request: DownloadFileRequest):
    """Download file from Google Drive"""
    if not drive_client:
        raise HTTPException(status_code=503, detail="Google Drive client not initialized")

    try:
        # Get file metadata
        file_metadata = drive_client.files().get(fileId=request.file_id).execute()
        file_name = file_metadata.get('name', 'download')

        # Download file
        request_download = drive_client.files().get_media(fileId=request.file_id)
        file_content = io.BytesIO()
        downloader = MediaIoBaseDownload(file_content, request_download)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        file_content.seek(0)
        content = file_content.read()

        # Determine output path
        if request.output_path:
            output_path = Path(request.output_path)
        else:
            output_path = Path(f"/tmp/{file_name}")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        with open(output_path, 'wb') as f:
            f.write(content)

        return {
            "status": "success",
            "file_id": request.file_id,
            "file_name": file_name,
            "output_path": str(output_path),
            "size": len(content)
        }

    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@with_redundancy(
    func_key="export_file",
    cache_key=None,
    alternatives=None,
    fallback_func=lambda file_id, format: {"status": "error", "message": "Export failed"}
)
@app.post("/drive/export")
async def export_file(request: ExportFileRequest):
    """Export Google Docs/Sheets to different format"""
    if not drive_client:
        raise HTTPException(status_code=503, detail="Google Drive client not initialized")

    try:
        # Get file metadata
        file_metadata = drive_client.files().get(fileId=request.file_id).execute()
        file_name = file_metadata.get('name', 'export')
        mime_type = file_metadata.get('mimeType', '')

        # Map format to MIME type
        format_mime_map = {
            'pdf': 'application/pdf',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'txt': 'text/plain',
            'html': 'text/html',
            'rtf': 'application/rtf',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'csv': 'text/csv',
            'ods': 'application/vnd.oasis.opendocument.spreadsheet',
            'tsv': 'text/tab-separated-values',
        }

        export_mime = format_mime_map.get(request.format)
        if not export_mime:
            raise HTTPException(status_code=400, detail=f"Invalid export format: {request.format}")

        # Export file
        request_export = drive_client.files().export_media(
            fileId=request.file_id,
            mimeType=export_mime
        )

        file_content = io.BytesIO()
        downloader = MediaIoBaseDownload(file_content, request_export)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        file_content.seek(0)
        content = file_content.read()

        # Determine output path
        if request.output_path:
            output_path = Path(request.output_path)
        else:
            extension = request.format
            output_path = Path(f"/tmp/{file_name}.{extension}")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        with open(output_path, 'wb') as f:
            f.write(content)

        return {
            "status": "success",
            "file_id": request.file_id,
            "file_name": file_name,
            "format": request.format,
            "output_path": str(output_path),
            "size": len(content)
        }

    except Exception as e:
        logger.error(f"Error exporting file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/drive/info/{file_id}")
async def get_file_info(file_id: str):
    """Get file information"""
    if not drive_client:
        raise HTTPException(status_code=503, detail="Google Drive client not initialized")

    try:
        file_metadata = drive_client.files().get(
            fileId=file_id,
            fields="id, name, mimeType, size, modifiedTime, createdTime, parents, webViewLink, webContentLink"
        ).execute()

        return {
            "status": "success",
            "file": file_metadata
        }

    except Exception as e:
        logger.error(f"Error getting file info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class CreateFileRequest(BaseModel):
    """Create file request model"""
    file_name: str = Field(..., min_length=1, max_length=255)
    folder_id: Optional[str] = None
    content: Optional[str] = None
    file_path: Optional[str] = None
    mime_type: str = Field("text/plain", max_length=100)

    @validator('file_name')
    def validate_file_name(cls, v):
        return validate_string(v, "file_name", min_length=1, max_length=255)


class UpdateFileRequest(BaseModel):
    """Update file request model"""
    file_id: str = Field(..., min_length=1, max_length=100)
    file_name: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None
    file_path: Optional[str] = None
    mime_type: Optional[str] = Field(None, max_length=100)

    @validator('file_id')
    def validate_file_id(cls, v):
        return validate_string(v, "file_id", min_length=1, max_length=100)


@with_redundancy(
    func_key="create_file",
    cache_key=None,
    alternatives=None,
    fallback_func=lambda: {"status": "error", "message": "File creation failed"}
)
@app.post("/drive/create")
async def create_file(request: CreateFileRequest):
    """Create a new file in Google Drive"""
    if not drive_client:
        raise HTTPException(status_code=503, detail="Google Drive client not initialized")

    try:
        # Prepare file metadata
        file_metadata = {
            'name': request.file_name
        }

        if request.folder_id:
            file_metadata['parents'] = [request.folder_id]

        # Prepare file content
        if request.file_path:
            # Upload from file path
            media = MediaFileUpload(
                request.file_path,
                mimetype=request.mime_type,
                resumable=True
            )
        elif request.content:
            # Upload from content string
            file_content = io.BytesIO(request.content.encode('utf-8'))
            media = MediaIoBaseUpload(
                file_content,
                mimetype=request.mime_type,
                resumable=True
            )
        else:
            # Create empty file
            media = MediaIoBaseUpload(
                io.BytesIO(b''),
                mimetype=request.mime_type,
                resumable=True
            )

        # Create file
        file = drive_client.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, mimeType, size, parents, webViewLink'
        ).execute()

        return {
            "status": "success",
            "file": file,
            "message": f"File '{request.file_name}' created successfully"
        }

    except Exception as e:
        logger.error(f"Error creating file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@with_redundancy(
    func_key="update_file",
    cache_key=None,
    alternatives=None,
    fallback_func=lambda: {"status": "error", "message": "File update failed"}
)
@app.put("/drive/update")
async def update_file(request: UpdateFileRequest):
    """Update an existing file in Google Drive"""
    if not drive_client:
        raise HTTPException(status_code=503, detail="Google Drive client not initialized")

    try:
        # Prepare file metadata
        file_metadata = {}
        if request.file_name:
            file_metadata['name'] = request.file_name

        # Prepare file content if provided
        media = None
        if request.file_path:
            # Update from file path
            mime_type = request.mime_type or 'application/octet-stream'
            media = MediaFileUpload(
                request.file_path,
                mimetype=mime_type,
                resumable=True
            )
        elif request.content:
            # Update from content string
            mime_type = request.mime_type or 'text/plain'
            file_content = io.BytesIO(request.content.encode('utf-8'))
            media = MediaIoBaseUpload(
                file_content,
                mimetype=mime_type,
                resumable=True
            )

        # Update file
        if media:
            # Update both metadata and content
            file = drive_client.files().update(
                fileId=request.file_id,
                body=file_metadata,
                media_body=media,
                fields='id, name, mimeType, size, modifiedTime, webViewLink'
            ).execute()
        else:
            # Update metadata only
            file = drive_client.files().update(
                fileId=request.file_id,
                body=file_metadata,
                fields='id, name, mimeType, size, modifiedTime, webViewLink'
            ).execute()

        return {
            "status": "success",
            "file": file,
            "message": f"File '{request.file_id}' updated successfully"
        }

    except Exception as e:
        logger.error(f"Error updating file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@with_redundancy(
    func_key="delete_file",
    cache_key=None,
    alternatives=None,
    fallback_func=lambda: {"status": "error", "message": "File deletion failed"}
)
@app.delete("/drive/delete/{file_id}")
async def delete_file(file_id: str):
    """Delete a file from Google Drive"""
    if not drive_client:
        raise HTTPException(status_code=503, detail="Google Drive client not initialized")

    try:
        # Get file info before deletion
        file_info = drive_client.files().get(
            fileId=file_id,
            fields="id, name"
        ).execute()

        file_name = file_info.get('name', file_id)

        # Delete file
        drive_client.files().delete(fileId=file_id).execute()

        return {
            "status": "success",
            "message": f"File '{file_name}' deleted successfully",
            "file_id": file_id
        }

    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class MoveFileRequest(BaseModel):
    """Move file request model"""
    file_id: str = Field(..., min_length=1, max_length=100)
    target_folder_id: str = Field(..., min_length=1, max_length=100)
    remove_from_previous: bool = True

    @validator('file_id')
    def validate_file_id(cls, v):
        return validate_string(v, "file_id", min_length=1, max_length=100)

    @validator('target_folder_id')
    def validate_target_folder_id(cls, v):
        return validate_string(v, "target_folder_id", min_length=1, max_length=100)


@app.post("/drive/move")
async def move_file(request: MoveFileRequest):
    """Move a file to a different folder"""
    if not drive_client:
        raise HTTPException(status_code=503, detail="Google Drive client not initialized")

    try:
        # Get current parents
        file_info = drive_client.files().get(
            fileId=request.file_id,
            fields="parents"
        ).execute()

        previous_parents = ",".join(file_info.get('parents', []))

        # Move file
        file = drive_client.files().update(
            fileId=request.file_id,
            addParents=request.target_folder_id,
            removeParents=previous_parents if request.remove_from_previous else None,
            fields='id, name, parents'
        ).execute()

        return {
            "status": "success",
            "file": file,
            "message": f"File moved to folder '{request.target_folder_id}'"
        }

    except Exception as e:
        logger.error(f"Error moving file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class CopyFileRequest(BaseModel):
    """Copy file request model"""
    file_id: str = Field(..., min_length=1, max_length=100)
    new_name: Optional[str] = None
    target_folder_id: Optional[str] = None

    @validator('file_id')
    def validate_file_id(cls, v):
        return validate_string(v, "file_id", min_length=1, max_length=100)


@app.post("/drive/copy")
async def copy_file(request: CopyFileRequest):
    """Copy a file in Google Drive"""
    if not drive_client:
        raise HTTPException(status_code=503, detail="Google Drive client not initialized")

    try:
        # Prepare copy metadata
        copy_metadata = {}
        if request.new_name:
            copy_metadata['name'] = request.new_name
        if request.target_folder_id:
            copy_metadata['parents'] = [request.target_folder_id]

        # Copy file
        copied_file = drive_client.files().copy(
            fileId=request.file_id,
            body=copy_metadata,
            fields='id, name, mimeType, size, parents, webViewLink'
        ).execute()

        return {
            "status": "success",
            "file": copied_file,
            "message": f"File copied successfully"
        }

    except Exception as e:
        logger.error(f"Error copying file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8008"))
    uvicorn.run(app, host="0.0.0.0", port=port)
