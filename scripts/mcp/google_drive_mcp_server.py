#!/usr/bin/env python3
"""
MCP Server for Google Drive Tools
Provides MCP-compatible interface for Google Drive operations
Implements stdio JSON-RPC protocol
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.microservices.google_drive_client import get_drive_client, GoogleDriveClient

class GoogleDriveMCPServer:
    """MCP Server for Google Drive operations"""

    def __init__(self):
        self.client: Optional[GoogleDriveClient] = None

    def _get_client(self) -> GoogleDriveClient:
        """Get or initialize Drive client"""
        if not self.client:
            self.client = get_drive_client()
            if not self.client:
                raise RuntimeError("Google Drive client not available")
        return self.client

    def list_drive_folder(self, folder_id: str) -> Dict[str, Any]:
        """List folder contents"""
        client = self._get_client()
        items = client.list_folder_contents(folder_id)
        return {
            "folder_id": folder_id,
            "items": items,
            "count": len(items)
        }

    def get_drive_file_info(self, file_id: str) -> Dict[str, Any]:
        """Get file metadata"""
        client = self._get_client()
        file_info = client.get_file_info(file_id)
        return file_info

    def download_drive_file(self, file_id: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Download a file"""
        client = self._get_client()
        content = client.download_file(file_id, output_path)
        file_info = client.get_file_info(file_id)

        result = {
            "file_id": file_id,
            "file_name": file_info.get('name', 'unknown'),
            "size": len(content),
            "downloaded": True
        }

        if output_path:
            result["output_path"] = output_path

        return result

    def export_google_doc(self, file_id: str, output_path: str, format: str = 'docx') -> Dict[str, Any]:
        """Export Google Doc"""
        client = self._get_client()
        exported_path = client.export_google_doc(file_id, output_path, format)
        file_info = client.get_file_info(file_id)

        return {
            "file_id": file_id,
            "file_name": file_info.get('name', 'unknown'),
            "export_format": format,
            "output_path": exported_path,
            "exported": True
        }

    def export_google_sheet(self, file_id: str, output_path: str, format: str = 'xlsx') -> Dict[str, Any]:
        """Export Google Sheet"""
        client = self._get_client()
        exported_path = client.export_google_sheet(file_id, output_path, format)
        file_info = client.get_file_info(file_id)

        return {
            "file_id": file_id,
            "file_name": file_info.get('name', 'unknown'),
            "export_format": format,
            "output_path": exported_path,
            "exported": True
        }

    def download_drive_folder(self, folder_id: str, output_dir: str = 'data/drive_downloads', recursive: bool = True) -> Dict[str, Any]:
        """Download folder contents"""
        client = self._get_client()
        downloaded_files = client.download_folder(folder_id, output_dir, recursive)

        return {
            "folder_id": folder_id,
            "output_dir": output_dir,
            "downloaded_files": downloaded_files,
            "count": len(downloaded_files),
            "recursive": recursive
        }

    def search_drive_files(self, query: str, folder_id: Optional[str] = None) -> Dict[str, Any]:
        """Search for files in Drive"""
        client = self._get_client()

        # Build search query
        search_query = f"name contains '{query}'"
        if folder_id:
            search_query += f" and '{folder_id}' in parents"
        search_query += " and trashed=false"

        try:
            results = []
            page_token = None

            while True:
                response = client.service.files().list(
                    q=search_query,
                    spaces='drive',
                    fields='nextPageToken, files(id, name, mimeType, size, modifiedTime, webViewLink)',
                    pageToken=page_token,
                    pageSize=100
                ).execute()

                files = response.get('files', [])
                results.extend(files)

                page_token = response.get('nextPageToken')
                if not page_token:
                    break

            return {
                "query": query,
                "folder_id": folder_id,
                "results": results,
                "count": len(results)
            }
        except Exception as e:
            return {
                "query": query,
                "error": str(e),
                "results": [],
                "count": 0
            }

def handle_mcp_request(request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Handle MCP request

    Returns None for notifications (requests without id) - JSON-RPC 2.0 spec
    Returns response dict for requests with id
    """
    method = request.get('method')
    params = request.get('params', {})
    request_id = request.get('id')

    # Check if this is a notification (no id) - JSON-RPC 2.0 says don't respond
    is_notification = request_id is None

    # Validate JSON-RPC request
    if 'jsonrpc' not in request or request.get('jsonrpc') != '2.0':
        if is_notification:
            return None  # Don't respond to notifications
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32600,
                "message": "Invalid Request"
            }
        }

    if not method:
        if is_notification:
            return None  # Don't respond to notifications
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32600,
                "message": "Invalid Request: method is required"
            }
        }

    try:
        if method == 'initialize':
            if is_notification:
                return None  # Don't respond to notifications
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "google-drive",
                        "version": "1.0.0"
                    }
                }
            }

        elif method == 'tools/list':
            if is_notification:
                return None  # Don't respond to notifications
            server = GoogleDriveMCPServer()
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "drive_operation",
                            "description": "Perform Google Drive operations: list folder contents, download files, or export Google Docs/Sheets. Use operation='list' to browse folders, operation='download' for regular files, or operation='export' with format parameter for Google Docs/Sheets.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "operation": {
                                        "type": "string",
                                        "enum": ["list", "download", "export"],
                                        "description": "Operation type: 'list' to browse folders, 'download' for files, 'export' for Google Docs/Sheets"
                                    },
                                    "folder_id": {
                                        "type": "string",
                                        "description": "Google Drive folder ID (required for 'list' operation)"
                                    },
                                    "file_id": {
                                        "type": "string",
                                        "description": "Google Drive file ID (required for 'download' or 'export' operations)"
                                    },
                                    "output_path": {
                                        "type": "string",
                                        "description": "Local path to save the file (optional for 'list', required for 'download'/'export')"
                                    },
                                    "format": {
                                        "type": "string",
                                        "description": "Export format for Google Docs/Sheets: docx, pdf, txt, html, rtf, xlsx, csv, ods, tsv (required for 'export' operation)"
                                    }
                                },
                                "required": ["operation"]
                            }
                        }
                    ]
                }
            }

        elif method == 'tools/call':
            if is_notification:
                return None  # Don't respond to notifications
            server = GoogleDriveMCPServer()
            tool_name = params.get('name')
            tool_args = params.get('arguments', {})

            if tool_name == 'drive_operation':
                operation = tool_args.get('operation')

                if operation == 'list':
                    folder_id = tool_args.get('folder_id')
                    if not folder_id:
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {
                                "code": -32602,
                                "message": "folder_id is required for 'list' operation"
                            }
                        }
                    result = server.list_drive_folder(folder_id)

                elif operation == 'download':
                    file_id = tool_args.get('file_id')
                    if not file_id:
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {
                                "code": -32602,
                                "message": "file_id is required for 'download' operation"
                            }
                        }
                    result = server.download_drive_file(
                        file_id,
                        tool_args.get('output_path')
                    )

                elif operation == 'export':
                    file_id = tool_args.get('file_id')
                    format_type = tool_args.get('format')

                    if not file_id:
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {
                                "code": -32602,
                                "message": "file_id is required for 'export' operation"
                            }
                        }
                    if not format_type:
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {
                                "code": -32602,
                                "message": "format is required for 'export' operation"
                            }
                        }

                    # Get file info to determine if it's a Google Doc/Sheet
                    file_info = server.get_drive_file_info(file_id)
                    mime_type = file_info.get('mimeType', '')
                    output_path = tool_args.get('output_path') or f"data/drive_downloads/{file_info.get('name', 'file')}.{format_type}"

                    if 'google-apps.document' in mime_type:
                        result = server.export_google_doc(file_id, output_path, format_type)
                    elif 'google-apps.spreadsheet' in mime_type:
                        result = server.export_google_sheet(file_id, output_path, format_type)
                    else:
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {
                                "code": -32602,
                                "message": f"File is not a Google Doc or Sheet. Use 'download' operation instead."
                            }
                        }
                else:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32602,
                            "message": f"Invalid operation: {operation}. Must be 'list', 'download', or 'export'"
                        }
                    }
            else:
                if is_notification:
                    return None  # Don't respond to notifications
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {tool_name}"
                    }
                }

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }

        else:
            if is_notification:
                return None  # Don't respond to notifications
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }

    except KeyError as e:
        if is_notification:
            return None  # Don't respond to notifications
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32602,
                "message": f"Invalid params: missing required parameter {str(e)}"
            }
        }
    except Exception as e:
        if is_notification:
            return None  # Don't respond to notifications
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32000,
                "message": str(e)
            }
        }

def main():
    """Main MCP server loop - reads from stdin, writes to stdout"""
    # Suppress any print statements that might interfere
    import sys
    import os

    # Redirect stderr to avoid interfering with JSON output
    # But keep it for actual errors

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
            except json.JSONDecodeError as e:
                # For parse errors, we can't determine if it was a notification
                # So we send an error response (JSON-RPC 2.0 allows this)
                # But use a numeric id since Cursor doesn't accept null
                error_response = {
                    "jsonrpc": "2.0",
                    "id": -1,  # Use numeric id for parse errors
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }
                print(json.dumps(error_response), flush=True)
                continue

            # Handle request
            response = handle_mcp_request(request)

            # Only send response if not None (None means notification - no response)
            # JSON-RPC 2.0: notifications (requests without id) don't get responses
            if response is not None:
                print(json.dumps(response), flush=True)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        # Only send error response if we can determine it's a JSON-RPC request
        # Otherwise, log to stderr
        import sys
        print(f"Internal error: {str(e)}", file=sys.stderr)

if __name__ == '__main__':
    main()
