#!/usr/bin/env python3
"""
GCP Authentication Helper
Sets up Google Cloud Platform authentication for Vertex AI and other GCP services
"""

import os
import json
from pathlib import Path

def setup_gcp_auth():
    """Setup GCP authentication from environment variables"""
    # Check for JSON credentials file path
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    if not creds_path:
        # Try default location
        project_root = Path(__file__).parent.parent.parent
        default_path = project_root / 'config' / 'gcp-credentials.json'
        if default_path.exists():
            creds_path = str(default_path)
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_path

    # Check for JSON credentials as environment variable
    gcp_creds_json = os.getenv('GCP_CREDENTIALS_JSON')
    if gcp_creds_json and not creds_path:
        try:
            # Parse JSON and write to temp file
            creds_data = json.loads(gcp_creds_json)
            temp_path = Path('/tmp/gcp-credentials.json')
            with open(temp_path, 'w') as f:
                json.dump(creds_data, f)
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(temp_path)
            creds_path = str(temp_path)
        except json.JSONDecodeError:
            print("Warning: GCP_CREDENTIALS_JSON is not valid JSON")

    # Set individual GCP environment variables if available
    if creds_path and Path(creds_path).exists():
        try:
            with open(creds_path, 'r') as f:
                creds = json.load(f)

            # Set individual environment variables for easy access
            os.environ['GCP_PROJECT_ID'] = creds.get('project_id', '')
            os.environ['GCP_CLIENT_EMAIL'] = creds.get('client_email', '')
            os.environ['GCP_CLIENT_ID'] = creds.get('client_id', '')
            os.environ['GCP_PRIVATE_KEY_ID'] = creds.get('private_key_id', '')

            print(f"✓ GCP authentication configured")
            print(f"  Project ID: {creds.get('project_id', 'N/A')}")
            print(f"  Client Email: {creds.get('client_email', 'N/A')}")
            return True
        except Exception as e:
            print(f"Warning: Could not load GCP credentials: {e}")
            return False

    # Check if individual environment variables are set
    if os.getenv('GCP_PROJECT_ID'):
        print("✓ GCP authentication configured via environment variables")
        return True

    print("⚠ GCP credentials not found. Vertex AI features may not work.")
    return False

def get_gcp_project_id() -> str:
    """Get GCP project ID"""
    return os.getenv('GCP_PROJECT_ID', '')

def get_gcp_region() -> str:
    """Get GCP region (default: us-central1)"""
    return os.getenv('GCP_REGION', 'us-central1')

def is_gcp_configured() -> bool:
    """Check if GCP is properly configured"""
    return bool(os.getenv('GOOGLE_APPLICATION_CREDENTIALS') or os.getenv('GCP_PROJECT_ID'))

if __name__ == '__main__':
    setup_gcp_auth()
    print(f"GCP Project ID: {get_gcp_project_id()}")
    print(f"GCP Region: {get_gcp_region()}")
    print(f"GCP Configured: {is_gcp_configured()}")
