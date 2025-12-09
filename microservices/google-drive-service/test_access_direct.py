#!/usr/bin/env python3
"""
Direct test script that doesn't require the service to be running
Tests Google Drive access directly using the credentials
"""

import sys
from pathlib import Path
import json

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_drive_access_direct():
    """Test Google Drive access directly"""
    print("=" * 70)
    print("Testing Google Drive Access Directly")
    print("=" * 70)
    print()
    
    # Check credentials file
    creds_file = PROJECT_ROOT / 'config' / 'gcp-credentials.json'
    if not creds_file.exists():
        print(f"✗ ERROR: Credentials file not found at {creds_file}")
        return False
    
    print(f"✓ Found credentials file: {creds_file}")
    
    try:
        with open(creds_file, 'r') as f:
            creds_data = json.load(f)
            service_account_email = creds_data.get('client_email')
            print(f"✓ Service Account: {service_account_email}")
    except Exception as e:
        print(f"✗ ERROR: Could not read credentials: {e}")
        return False
    
    print()
    print("To test access, you need to:")
    print("1. Grant access to the folder:")
    print(f"   Email: {service_account_email}")
    print("   Folder: https://drive.google.com/drive/folders/1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8")
    print()
    print("2. Start the service:")
    print("   cd microservices")
    print("   docker-compose up google-drive-service")
    print()
    print("3. Then run:")
    print("   python3 microservices/google-drive-service/test_access.py")
    print()
    
    # Try to import Google Drive libraries
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        print("✓ Google Drive libraries available")
        
        # Try to initialize client
        print()
        print("Attempting to initialize Google Drive client...")
        creds = service_account.Credentials.from_service_account_file(
            str(creds_file),
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        
        drive_service = build('drive', 'v3', credentials=creds)
        print("✓ Google Drive client initialized")
        
        # Test listing folder
        print()
        print("Testing folder access...")
        folder_id = "1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8"
        
        try:
            results = drive_service.files().list(
                q=f"'{folder_id}' in parents",
                pageSize=10,
                fields="files(id, name, mimeType)"
            ).execute()
            
            items = results.get('files', [])
            print(f"✓ SUCCESS! Found {len(items)} items in folder")
            print()
            
            if items:
                print("Folder contents:")
                for item in items:
                    print(f"  - {item.get('name')} ({item.get('mimeType', 'unknown')})")
            else:
                print("Folder is empty")
            
            return True
            
        except Exception as e:
            error_str = str(e)
            if "403" in error_str or "Forbidden" in error_str:
                print("✗ ACCESS DENIED (403)")
                print()
                print("The service account does not have access to this folder.")
                print("Please grant access:")
                print(f"1. Open: https://drive.google.com/drive/folders/{folder_id}")
                print("2. Click 'Share'")
                print(f"3. Add: {service_account_email}")
                print("4. Set permission: 'Viewer'")
                print("5. Click 'Share'")
            else:
                print(f"✗ ERROR: {e}")
            return False
        
    except ImportError as e:
        print(f"⚠ Google Drive libraries not installed")
        print("Install with: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        print()
        print("Or use Docker:")
        print("  docker-compose up google-drive-service")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_drive_access_direct()
    sys.exit(0 if success else 1)
