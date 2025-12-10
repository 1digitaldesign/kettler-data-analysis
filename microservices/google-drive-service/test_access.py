#!/usr/bin/env python3
"""
Test script to verify Google Drive access
"""

import sys
from pathlib import Path
import requests
import json

def test_folder_access(folder_id: str, service_url: str = "http://localhost:8008"):
    """Test access to a Google Drive folder"""
    print(f"Testing access to folder: {folder_id}")
    print(f"Service URL: {service_url}")
    print()

    try:
        # Test health check first
        health_response = requests.get(f"{service_url}/health", timeout=5)
        if health_response.status_code != 200:
            print(f"ERROR: Service health check failed: {health_response.status_code}")
            return False

        health_data = health_response.json()
        print("Service Health:")
        print(f"  Status: {health_data.get('status')}")
        print(f"  Google Drive Available: {health_data.get('google_drive_available')}")
        print(f"  Drive Client Initialized: {health_data.get('drive_client_initialized')}")
        print()

        if not health_data.get('drive_client_initialized'):
            print("ERROR: Google Drive client is not initialized")
            print("Check credentials and ensure service account has access")
            return False

        # Test listing folder
        print("Testing folder list...")
        list_response = requests.post(
            f"{service_url}/drive/list",
            json={
                "folder_id": folder_id,
                "include_files": True,
                "include_folders": True,
                "max_results": 100
            },
            timeout=30
        )

        if list_response.status_code == 200:
            data = list_response.json()
            print("✓ SUCCESS: Folder access granted!")
            print()
            print(f"Folder ID: {data.get('folder_id')}")
            print(f"Items found: {data.get('count', 0)}")
            print()

            items = data.get('items', [])
            if items:
                print("Sample items:")
                for item in items[:5]:
                    print(f"  - {item.get('name')} ({item.get('mimeType', 'unknown')})")
                if len(items) > 5:
                    print(f"  ... and {len(items) - 5} more")
            else:
                print("Folder is empty")

            return True
        elif list_response.status_code == 403:
            print("✗ ERROR: Access denied (403 Forbidden)")
            print()
            print("The service account does not have access to this folder.")
            print("Please grant access:")
            print("1. Open the folder in Google Drive")
            print("2. Click 'Share'")
            print("3. Add: fraud-analysis@claude-eval-20250615.iam.gserviceaccount.com")
            print("4. Set permission to 'Viewer'")
            return False
        elif list_response.status_code == 404:
            print("✗ ERROR: Folder not found (404)")
            print("Check that the folder ID is correct")
            return False
        else:
            print(f"✗ ERROR: Request failed with status {list_response.status_code}")
            print(f"Response: {list_response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("✗ ERROR: Could not connect to service")
        print("Make sure the Google Drive service is running:")
        print("  docker-compose up google-drive-service")
        print("  OR")
        print("  cd microservices/google-drive-service && python -m uvicorn main:app --port 8008")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

def main():
    """Main function"""
    folder_id = "1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8"

    # Try API Gateway first, then direct service
    if test_folder_access(folder_id, "http://localhost:8000"):
        print("\n✓ Access verified through API Gateway!")
    elif test_folder_access(folder_id, "http://localhost:8008"):
        print("\n✓ Access verified through Google Drive Service!")
    else:
        print("\n✗ Access test failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
