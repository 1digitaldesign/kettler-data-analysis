#!/usr/bin/env python3
"""
Download Google Drive Folder
Downloads all files from a specific Google Drive folder
"""

import sys
import argparse
from pathlib import Path
from scripts.microservices.google_drive_client import get_drive_client

def main():
    parser = argparse.ArgumentParser(description='Download Google Drive folder contents')
    parser.add_argument('folder_id', help='Google Drive folder ID')
    parser.add_argument('--output', '-o', default='data/drive_downloads', help='Output directory')
    parser.add_argument('--recursive', '-r', action='store_true', help='Download subfolders recursively')
    parser.add_argument('--list-only', '-l', action='store_true', help='Only list files, do not download')

    args = parser.parse_args()

    client = get_drive_client()
    if not client:
        print("Error: Could not initialize Google Drive client")
        sys.exit(1)

    print(f"Accessing Google Drive folder: {args.folder_id}")
    print()

    # List folder contents
    try:
        items = client.list_folder_contents(args.folder_id)
        print(f"Found {len(items)} items in folder")
        print()

        if args.list_only:
            print("Files in folder:")
            for item in items:
                mime_type = item.get('mimeType', 'unknown')
                size = item.get('size', 'N/A')
                print(f"  - {item['name']} ({mime_type}) - {size} bytes")
            return

        # Download files
        print(f"Downloading to: {args.output}")
        downloaded_files = client.download_folder(
            args.folder_id,
            args.output,
            recursive=args.recursive
        )

        print(f"\n✓ Downloaded {len(downloaded_files)} files:")
        for file_path in downloaded_files:
            print(f"  - {file_path}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
