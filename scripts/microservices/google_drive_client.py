#!/usr/bin/env python3
"""
Google Drive API Client
Accesses Google Drive files, documents, and spreadsheets
"""

import os
import json
import io
from pathlib import Path
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

# Try to import Google Drive API libraries
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
    from googleapiclient.errors import HttpError
    DRIVE_API_AVAILABLE = True
except ImportError:
    DRIVE_API_AVAILABLE = False
    # Don't print warnings to stdout when used as MCP server
    import sys
    if hasattr(sys, 'stderr'):
        print("Google Drive API libraries not installed. Install with: pip install google-api-python-client", file=sys.stderr)

# Google Drive API scopes
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]

def get_drive_service():
    """Get authenticated Google Drive service"""
    if not DRIVE_API_AVAILABLE:
        raise ImportError("Google Drive API libraries not available")

    # Setup GCP authentication
    from scripts.microservices.gcp_auth import setup_gcp_auth

    if not setup_gcp_auth():
        raise ValueError("GCP credentials not configured")

    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds_path or not Path(creds_path).exists():
        raise FileNotFoundError(f"GCP credentials file not found: {creds_path}")

    # Load credentials
    creds = service_account.Credentials.from_service_account_file(
        creds_path,
        scopes=SCOPES
    )

    # Build Drive API service
    service = build('drive', 'v3', credentials=creds)

    logger.info("Google Drive service initialized")
    return service

class GoogleDriveClient:
    """Client for Google Drive operations"""

    def __init__(self):
        if not DRIVE_API_AVAILABLE:
            raise ImportError("Google Drive API libraries not available")

        self.service = get_drive_service()
        self.project_id = os.getenv('GCP_PROJECT_ID', '')

    def list_folder_contents(self, folder_id: str) -> List[Dict]:
        """List all files and folders in a Drive folder"""
        try:
            results = []
            page_token = None

            while True:
                query = f"'{folder_id}' in parents and trashed=false"

                response = self.service.files().list(
                    q=query,
                    spaces='drive',
                    fields='nextPageToken, files(id, name, mimeType, size, modifiedTime, webViewLink, webContentLink)',
                    pageToken=page_token,
                    pageSize=100
                ).execute()

                files = response.get('files', [])
                results.extend(files)

                page_token = response.get('nextPageToken')
                if not page_token:
                    break

            logger.info(f"Found {len(results)} items in folder {folder_id}")
            return results

        except HttpError as e:
            logger.error(f"Error listing folder contents: {e}")
            raise

    def get_file_info(self, file_id: str) -> Dict:
        """Get file metadata"""
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields='id, name, mimeType, size, modifiedTime, createdTime, webViewLink, webContentLink, parents'
            ).execute()
            return file
        except HttpError as e:
            logger.error(f"Error getting file info: {e}")
            raise

    def download_file(self, file_id: str, output_path: Optional[str] = None) -> bytes:
        """Download a file from Google Drive"""
        try:
            file_info = self.get_file_info(file_id)
            file_name = file_info.get('name', 'unknown')
            mime_type = file_info.get('mimeType', '')

            # Handle Google Workspace files differently
            if 'google-apps' in mime_type:
                # Export Google Docs/Sheets/Slides
                export_mime_type = self._get_export_mime_type(mime_type)
                if export_mime_type:
                    request = self.service.files().export_media(
                        fileId=file_id,
                        mimeType=export_mime_type
                    )
                else:
                    raise ValueError(f"Cannot export file type: {mime_type}")
            else:
                # Regular file download
                request = self.service.files().get_media(fileId=file_id)

            # Download file
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    logger.debug(f"Download progress: {int(status.progress() * 100)}%")

            content = file_content.getvalue()

            # Save to file if output path provided
            if output_path:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(content)
                logger.info(f"Downloaded {file_name} to {output_path}")

            return content

        except HttpError as e:
            logger.error(f"Error downloading file: {e}")
            raise

    def _get_export_mime_type(self, mime_type: str) -> Optional[str]:
        """Get export MIME type for Google Workspace files"""
        export_map = {
            'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx
            'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
            'application/vnd.google-apps.presentation': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',  # .pptx
            'application/vnd.google-apps.drawing': 'image/png',  # .png
            'application/vnd.google-apps.script': 'application/vnd.google-apps.script+json',  # JSON
        }
        return export_map.get(mime_type)

    def export_google_doc(self, file_id: str, output_path: str, format: str = 'docx') -> str:
        """Export Google Doc to specified format"""
        format_map = {
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'pdf': 'application/pdf',
            'txt': 'text/plain',
            'html': 'text/html',
            'rtf': 'application/rtf'
        }

        mime_type = format_map.get(format.lower())
        if not mime_type:
            raise ValueError(f"Unsupported format: {format}")

        try:
            request = self.service.files().export_media(
                fileId=file_id,
                mimeType=mime_type
            )

            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(file_content.getvalue())

            logger.info(f"Exported Google Doc to {output_path}")
            return output_path

        except HttpError as e:
            logger.error(f"Error exporting Google Doc: {e}")
            raise

    def export_google_sheet(self, file_id: str, output_path: str, format: str = 'xlsx') -> str:
        """Export Google Sheet to specified format"""
        format_map = {
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'csv': 'text/csv',
            'pdf': 'application/pdf',
            'ods': 'application/vnd.oasis.opendocument.spreadsheet',
            'tsv': 'text/tab-separated-values'
        }

        mime_type = format_map.get(format.lower())
        if not mime_type:
            raise ValueError(f"Unsupported format: {format}")

        try:
            request = self.service.files().export_media(
                fileId=file_id,
                mimeType=mime_type
            )

            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(file_content.getvalue())

            logger.info(f"Exported Google Sheet to {output_path}")
            return output_path

        except HttpError as e:
            logger.error(f"Error exporting Google Sheet: {e}")
            raise

    def download_folder(self, folder_id: str, output_dir: str, recursive: bool = True) -> List[str]:
        """Download all files from a folder"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        downloaded_files = []
        items = self.list_folder_contents(folder_id)

        for item in items:
            item_id = item['id']
            item_name = item['name']
            mime_type = item.get('mimeType', '')

            # Handle folders recursively
            if mime_type == 'application/vnd.google-apps.folder' and recursive:
                subfolder_path = output_path / item_name
                sub_files = self.download_folder(item_id, str(subfolder_path), recursive=True)
                downloaded_files.extend(sub_files)
                continue

            # Determine file extension
            ext = self._get_file_extension(mime_type, item_name)
            file_path = output_path / f"{item_name}{ext}"

            try:
                self.download_file(item_id, str(file_path))
                downloaded_files.append(str(file_path))
            except Exception as e:
                logger.error(f"Error downloading {item_name}: {e}")

        return downloaded_files

    def _get_file_extension(self, mime_type: str, file_name: str) -> str:
        """Get appropriate file extension"""
        # Check if file already has extension
        if '.' in file_name:
            return ''

        ext_map = {
            'application/vnd.google-apps.document': '.docx',
            'application/vnd.google-apps.spreadsheet': '.xlsx',
            'application/vnd.google-apps.presentation': '.pptx',
            'application/pdf': '.pdf',
            'text/plain': '.txt',
            'text/csv': '.csv',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
        }

        return ext_map.get(mime_type, '')

def get_drive_client() -> Optional[GoogleDriveClient]:
    """Get Google Drive client instance"""
    if not DRIVE_API_AVAILABLE:
        return None

    try:
        return GoogleDriveClient()
    except Exception as e:
        logger.error(f"Could not initialize Google Drive client: {e}")
        return None

if __name__ == '__main__':
    import sys

    # Test with the provided folder ID
    folder_id = '1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8'

    try:
        client = get_drive_client()
        if not client:
            print("⚠ Google Drive client not available")
            sys.exit(1)

        print(f"✓ Google Drive client initialized")
        print(f"  Project ID: {client.project_id}")
        print()

        print(f"Listing contents of folder: {folder_id}")
        items = client.list_folder_contents(folder_id)

        print(f"\nFound {len(items)} items:")
        for item in items:
            mime_type = item.get('mimeType', 'unknown')
            size = item.get('size', 'N/A')
            modified = item.get('modifiedTime', 'N/A')
            print(f"  - {item['name']} ({mime_type})")
            print(f"    ID: {item['id']}")
            print(f"    Size: {size}, Modified: {modified}")
            print()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
