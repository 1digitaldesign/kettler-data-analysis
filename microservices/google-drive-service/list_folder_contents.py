#!/usr/bin/env python3
"""
List Google Drive folder contents recursively
"""

import sys
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def list_folder(folder_id, drive_service, indent=0):
    """Recursively list folder contents"""
    prefix = "  " * indent

    try:
        results = drive_service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=100,
            fields="files(id, name, mimeType, size, modifiedTime)"
        ).execute()

        items = results.get('files', [])

        for item in items:
            name = item.get('name')
            mime_type = item.get('mimeType', '')
            size = item.get('size', 'N/A')
            modified = item.get('modifiedTime', 'N/A')

            if mime_type == 'application/vnd.google-apps.folder':
                print(f"{prefix}📁 {name}/")
                # Recursively list subfolder
                list_folder(item.get('id'), drive_service, indent + 1)
            else:
                print(f"{prefix}📄 {name} ({mime_type}) - {size} bytes")

        return items

    except Exception as e:
        print(f"{prefix}✗ Error listing folder: {e}")
        return []

def main():
    """Main function"""
    creds_file = PROJECT_ROOT / 'config' / 'gcp-credentials.json'
    root_folder_id = "1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8"

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        print("=" * 70)
        print("Google Drive Folder Structure")
        print("=" * 70)
        print()

        creds = service_account.Credentials.from_service_account_file(
            str(creds_file),
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )

        drive_service = build('drive', 'v3', credentials=creds)

        # Get root folder name
        root_info = drive_service.files().get(fileId=root_folder_id, fields="name").execute()
        root_name = root_info.get('name', 'Root Folder')

        print(f"📁 {root_name}/")
        print()

        # List contents recursively
        list_folder(root_folder_id, drive_service, indent=1)

        print()
        print("=" * 70)
        print("Folder listing complete")
        print("=" * 70)

    except ImportError:
        print("ERROR: Google Drive libraries not installed")
        print("Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
