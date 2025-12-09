#!/usr/bin/env python3
"""
Generate a tree diagram of Google Drive folder structure
"""

import sys
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def get_folder_structure(drive_service, folder_id, indent=0, max_depth=10):
    """Recursively get folder structure"""
    if indent > max_depth:
        return []
    
    structure = []
    prefix = "│  " * indent
    last_prefix = "└── " if indent > 0 else ""
    
    try:
        results = drive_service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=1000,
            orderBy="name",
            fields="files(id, name, mimeType, size, modifiedTime)"
        ).execute()
        
        items = sorted(results.get('files', []), key=lambda x: (x.get('mimeType') != 'application/vnd.google-apps.folder', x.get('name', '').lower()))
        
        for i, item in enumerate(items):
            name = item.get('name')
            mime_type = item.get('mimeType', '')
            size = item.get('size', 'N/A')
            is_last = i == len(items) - 1
            
            if indent == 0:
                connector = "📁 " if mime_type == 'application/vnd.google-apps.folder' else "📄 "
            else:
                connector = "├── " if not is_last else "└── "
            
            if mime_type == 'application/vnd.google-apps.folder':
                structure.append(f"{prefix}{connector}{name}/")
                # Recursively get subfolder structure
                sub_structure = get_folder_structure(drive_service, item.get('id'), indent + 1, max_depth)
                structure.extend(sub_structure)
            else:
                # Format file with size
                size_str = f" ({size} bytes)" if size != 'N/A' else ""
                structure.append(f"{prefix}{connector}{name}{size_str}")
        
        return structure
        
    except Exception as e:
        structure.append(f"{prefix}✗ Error: {e}")
        return structure

def main():
    """Main function"""
    creds_file = PROJECT_ROOT / 'config' / 'gcp-credentials.json'
    root_folder_id = "1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8"
    
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        
        print("=" * 80)
        print("Google Drive Folder Structure - Tree Diagram")
        print("=" * 80)
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
        
        # Get structure
        structure = get_folder_structure(drive_service, root_folder_id, indent=1)
        
        for line in structure:
            print(line)
        
        print()
        print("=" * 80)
        print("Tree diagram complete")
        print("=" * 80)
        
        # Save to file
        output_file = PROJECT_ROOT / 'microservices' / 'google-drive-service' / 'drive_structure_tree.txt'
        with open(output_file, 'w') as f:
            f.write(f"Google Drive Folder Structure - Tree Diagram\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"📁 {root_name}/\n\n")
            for line in structure:
                f.write(line + "\n")
        
        print(f"\nTree diagram saved to: {output_file}")
        
    except ImportError:
        print("ERROR: Google Drive libraries not installed")
        print("Install with: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
