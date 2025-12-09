#!/usr/bin/env python3
"""
Helper script to grant service account access to Google Drive folder
and verify access
"""

import sys
from pathlib import Path
import json

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def get_service_account_email():
    """Get service account email from credentials"""
    creds_file = PROJECT_ROOT / 'config' / 'gcp-credentials.json'

    if not creds_file.exists():
        print(f"ERROR: Credentials file not found at {creds_file}")
        return None

    try:
        with open(creds_file, 'r') as f:
            creds = json.load(f)
            return creds.get('client_email')
    except Exception as e:
        print(f"ERROR: Could not read credentials: {e}")
        return None

def main():
    """Main function"""
    print("=" * 70)
    print("Google Drive Service Account Access Setup")
    print("=" * 70)
    print()

    # Get service account email
    service_account_email = get_service_account_email()

    if not service_account_email:
        print("Could not determine service account email.")
        return

    print(f"Service Account Email: {service_account_email}")
    print()
    print("To grant access to a Google Drive folder:")
    print()
    print("1. Open Google Drive in your browser:")
    print("   https://drive.google.com/drive/folders/1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8")
    print()
    print("2. Right-click on the folder → Click 'Share'")
    print()
    print("3. In the 'Add people and groups' field, paste:")
    print(f"   {service_account_email}")
    print()
    print("4. Select permission: 'Editor' (for CRUD operations) or 'Viewer' (read-only)")
    print()
    print("5. Uncheck 'Notify people' (optional)")
    print()
    print("6. Click 'Share'")
    print()
    print("=" * 70)
    print("After granting access, test with:")
    print("=" * 70)
    print()
    print("curl -X POST http://localhost:8008/drive/list \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{")
    print('    "folder_id": "1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8",')
    print('    "include_files": true,')
    print('    "include_folders": true,')
    print('    "max_results": 100')
    print("  }'")
    print()
    print("Or use the API Gateway:")
    print("curl -X POST http://localhost:8000/api/drive/list \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{")
    print('    "folder_id": "1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8"')
    print("  }'")
    print()

if __name__ == "__main__":
    main()
