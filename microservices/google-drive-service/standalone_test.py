#!/usr/bin/env python3
"""
Standalone test that installs dependencies and tests Google Drive access
"""

import subprocess
import sys
from pathlib import Path
import json

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "--user", "--break-system-packages",
            "google-api-python-client", "google-auth-httplib2", "google-auth-oauthlib"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Dependencies installed")
        return True
    except Exception as e:
        print(f"⚠ Could not install dependencies: {e}")
        print("Please install manually: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        return False

def test_access():
    """Test Google Drive access"""
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    creds_file = PROJECT_ROOT / 'config' / 'gcp-credentials.json'
    folder_id = "1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8"
    
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        
        print("Initializing Google Drive client...")
        creds = service_account.Credentials.from_service_account_file(
            str(creds_file),
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        
        drive_service = build('drive', 'v3', credentials=creds)
        print("✓ Client initialized")
        
        print(f"\nTesting access to folder: {folder_id}")
        results = drive_service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=10,
            fields="files(id, name, mimeType, size)"
        ).execute()
        
        items = results.get('files', [])
        print(f"\n✓ SUCCESS! Found {len(items)} items")
        
        if items:
            print("\nFolder contents:")
            for item in items:
                size = item.get('size', 'N/A')
                print(f"  - {item.get('name')} ({item.get('mimeType', 'unknown')}) - {size} bytes")
        
        return True
        
    except ImportError:
        if install_dependencies():
            return test_access()
        return False
    except Exception as e:
        error_str = str(e)
        if "403" in error_str or "Forbidden" in error_str:
            print("\n✗ ACCESS DENIED")
            print("\nPlease grant access:")
            print("1. Open: https://drive.google.com/drive/folders/1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8")
            print("2. Click 'Share'")
            print("3. Add: fraud-analysis@claude-eval-20250615.iam.gserviceaccount.com")
            print("4. Set permission: 'Viewer'")
            print("5. Click 'Share'")
        else:
            print(f"\n✗ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("Google Drive Access Test")
    print("=" * 70)
    print()
    
    success = test_access()
    sys.exit(0 if success else 1)
