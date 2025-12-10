#!/usr/bin/env python3
"""
Service Discovery and Health Monitor
Monitors all microservices and provides service discovery
"""

import os
import time
import requests
import json
from typing import Dict, List
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Service registry - dynamically discover services
def get_service_url(service_name: str, default_port: int = 8000) -> str:
    """Get service URL from environment or use default"""
    env_var = f"{service_name.upper().replace('-', '_')}_SERVICE"
    service_host = os.getenv(env_var, f"{service_name}:{default_port}")
    if not service_host.startswith('http'):
        service_host = f"http://{service_host}"
    return service_host

SERVICES = {
    'vector-api': {
        'url': get_service_url('vector-api', 8000),
        'health_endpoint': '/health',
        'status': 'unknown',
        'last_check': None
    },
    'python-etl': {
        'url': get_service_url('python-etl', 8000),
        'health_endpoint': '/health',
        'status': 'unknown',
        'last_check': None
    }
}

def check_service_health(service_name: str, config: Dict) -> Dict:
    """Check health of a single service"""
    try:
        health_url = f"{config['url']}{config['health_endpoint']}"
        response = requests.get(health_url, timeout=5)

        if response.status_code == 200:
            return {
                'status': 'healthy',
                'response_time': response.elapsed.total_seconds(),
                'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else None
            }
        else:
            return {
                'status': 'unhealthy',
                'status_code': response.status_code
            }
    except requests.exceptions.RequestException as e:
        return {
            'status': 'unreachable',
            'error': str(e)
        }

def update_service_registry():
    """Update service registry with current health status"""
    for service_name, config in SERVICES.items():
        health = check_service_health(service_name, config)
        config['status'] = health['status']
        config['last_check'] = datetime.now().isoformat()
        config['health'] = health

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'service-discovery'}), 200

@app.route('/api/v1/services', methods=['GET'])
def list_services():
    """List all registered services"""
    update_service_registry()
    return jsonify({
        'services': SERVICES,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/v1/services/<service_name>', methods=['GET'])
def get_service(service_name: str):
    """Get status of a specific service"""
    if service_name not in SERVICES:
        return jsonify({'error': 'Service not found'}), 404

    config = SERVICES[service_name]
    health = check_service_health(service_name, config)
    config['status'] = health['status']
    config['last_check'] = datetime.now().isoformat()

    return jsonify({
        'service': service_name,
        'config': config,
        'health': health
    }), 200

@app.route('/api/v1/services/<service_name>/url', methods=['GET'])
def get_service_url(service_name: str):
    """Get URL for a specific service (service discovery)"""
    if service_name not in SERVICES:
        return jsonify({'error': 'Service not found'}), 404

    return jsonify({
        'service': service_name,
        'url': SERVICES[service_name]['url']
    }), 200

def background_health_check():
    """Background task to periodically check service health"""
    while True:
        update_service_registry()
        time.sleep(30)  # Check every 30 seconds

if __name__ == '__main__':
    import threading

    # Start background health check
    health_thread = threading.Thread(target=background_health_check, daemon=True)
    health_thread.start()

    # Run Flask app
    app.run(host='0.0.0.0', port=8080, debug=False)
