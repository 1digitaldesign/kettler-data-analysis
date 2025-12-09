#!/usr/bin/env python3
"""
Google Drive API Service
REST API service for accessing Google Drive files
"""

import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from typing import Dict, List
import logging
from io import BytesIO

from scripts.microservices.google_drive_client import get_drive_client, GoogleDriveClient

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_client() -> GoogleDriveClient:
    """Get Google Drive client"""
    client = get_drive_client()
    if not client:
        raise RuntimeError("Google Drive client not available")
    return client

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    try:
        client = get_client()
        return jsonify({
            'status': 'healthy',
            'service': 'google-drive-api',
            'project_id': client.project_id
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/v1/drive/folder/<folder_id>/list', methods=['GET'])
def list_folder(folder_id: str):
    """List contents of a Google Drive folder"""
    try:
        client = get_client()
        items = client.list_folder_contents(folder_id)
        return jsonify({
            'folder_id': folder_id,
            'items': items,
            'count': len(items)
        }), 200
    except Exception as e:
        logger.error(f"Error listing folder: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/drive/file/<file_id>/info', methods=['GET'])
def get_file_info(file_id: str):
    """Get file metadata"""
    try:
        client = get_client()
        file_info = client.get_file_info(file_id)
        return jsonify(file_info), 200
    except Exception as e:
        logger.error(f"Error getting file info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/drive/file/<file_id>/download', methods=['GET'])
def download_file(file_id: str):
    """Download a file from Google Drive"""
    try:
        client = get_client()
        file_info = client.get_file_info(file_id)
        file_name = file_info.get('name', 'file')
        mime_type = file_info.get('mimeType', '')

        # Download file content
        content = client.download_file(file_id)

        # Sanitize filename and determine extension
        safe_file_name = file_name.replace('/', '_').replace('\\', '_').replace('..', '_')
        ext = client._get_file_extension(mime_type, file_name)
        download_name = f"{safe_file_name}{ext}"

        return send_file(
            BytesIO(content),
            mimetype=mime_type,
            as_attachment=True,
            download_name=download_name
        )
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/drive/file/<file_id>/export', methods=['GET'])
def export_file(file_id: str):
    """Export Google Workspace file (Docs, Sheets, etc.)"""
    import tempfile
    import os

    try:
        export_format = request.args.get('format', 'docx')
        client = get_client()
        file_info = client.get_file_info(file_id)
        mime_type = file_info.get('mimeType', '')
        file_name = file_info.get('name', 'file')

        # Create unique temporary file path
        format_ext_map = {
            'docx': '.docx', 'pdf': '.pdf', 'txt': '.txt', 'html': '.html', 'rtf': '.rtf',
            'xlsx': '.xlsx', 'csv': '.csv', 'ods': '.ods', 'tsv': '.tsv'
        }
        ext = format_ext_map.get(export_format, f'.{export_format}')
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        temp_path = temp_file.name
        temp_file.close()

        try:
            # Determine export method based on file type
            if 'spreadsheet' in mime_type:
                exported_path = client.export_google_sheet(file_id, temp_path, format=export_format)
            elif 'document' in mime_type:
                exported_path = client.export_google_doc(file_id, temp_path, format=export_format)
            else:
                os.unlink(temp_path)
                return jsonify({'error': 'File type not supported for export'}), 400

            # Read exported file content
            with open(exported_path, 'rb') as f:
                file_content = f.read()

            # Clean up temp file
            os.unlink(exported_path)

            # Sanitize filename for download
            safe_file_name = file_name.replace('/', '_').replace('\\', '_').replace('..', '_')
            return send_file(
                BytesIO(file_content),
                mimetype='application/octet-stream',
                as_attachment=True,
                download_name=f"{safe_file_name}{ext}"
            )
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise
    except Exception as e:
        logger.error(f"Error exporting file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/drive/folder/<folder_id>/download', methods=['POST'])
def download_folder(folder_id: str):
    """Download all files from a folder"""
    try:
        data = request.get_json() or {}
        output_dir = data.get('output_dir', 'data/drive_downloads')
        recursive = data.get('recursive', True)

        client = get_client()
        downloaded_files = client.download_folder(folder_id, output_dir, recursive=recursive)

        return jsonify({
            'folder_id': folder_id,
            'output_dir': output_dir,
            'downloaded_files': downloaded_files,
            'count': len(downloaded_files)
        }), 200
    except Exception as e:
        logger.error(f"Error downloading folder: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('DRIVE_API_PORT', '8084'))
    app.run(host='0.0.0.0', port=port, debug=False)
