#!/usr/bin/env python3
"""
Hugging Face Authentication Helper
Configures Hugging Face tokens for the application
"""

import os
from pathlib import Path

def setup_huggingface_auth():
    """Setup Hugging Face authentication from environment variables"""
    hf_write_token = os.getenv('HF_WRITE_TOKEN', '')
    hf_read_token = os.getenv('HF_READ_TOKEN', '')

    # Set environment variables for Hugging Face
    if hf_write_token:
        os.environ['HF_TOKEN'] = hf_write_token
        os.environ['HUGGING_FACE_HUB_TOKEN'] = hf_write_token
        print("✓ Hugging Face write token configured")

    if hf_read_token:
        os.environ['HF_READ_TOKEN'] = hf_read_token
        print("✓ Hugging Face read token configured")

    # Try to login using huggingface_hub if available
    try:
        from huggingface_hub import login
        if hf_write_token:
            login(token=hf_write_token)
            print("✓ Logged in to Hugging Face Hub")
    except ImportError:
        pass  # huggingface_hub not required
    except Exception as e:
        print(f"Warning: Could not login to Hugging Face Hub: {e}")

    return {
        'write_token_set': bool(hf_write_token),
        'read_token_set': bool(hf_read_token)
    }

def test_huggingface_connection():
    """Test Hugging Face connection"""
    try:
        from huggingface_hub import whoami
        user_info = whoami()
        print(f"✓ Connected to Hugging Face as: {user_info.get('name', 'unknown')}")
        return True
    except Exception as e:
        print(f"✗ Hugging Face connection test failed: {e}")
        return False

if __name__ == '__main__':
    print("=== Hugging Face Authentication Setup ===")
    result = setup_huggingface_auth()
    print(f"\nWrite token: {'✓ Set' if result['write_token_set'] else '✗ Not set'}")
    print(f"Read token: {'✓ Set' if result['read_token_set'] else '✗ Not set'}")

    if result['write_token_set']:
        test_huggingface_connection()
