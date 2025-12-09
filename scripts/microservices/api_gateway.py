#!/usr/bin/env python3
"""
API Gateway - Single entry point for all microservices
Provides routing, load balancing, and request aggregation
"""

import os
import requests
import time
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from functools import wraps
from typing import Dict, List, Optional
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Service registry
SERVICES = {
    'vector-api': {
        'url': os.getenv('VECTOR_API_SERVICE', 'http://vector-api:8000'),
        'health_endpoint': '/health',
        'routes': ['/api/v1/vector', '/api/v1/search', '/api/v1/stats', '/api/v1/embed']
    },
    'r-api': {
        'url': os.getenv('R_API_SERVICE', 'http://r-api:8001'),
        'health_endpoint': '/health',
        'routes': ['/api/v1/r', '/api/v1/analyze']
    },
    'python-etl': {
        'url': os.getenv('PYTHON_ETL_SERVICE', 'http://python-etl:8000'),
        'health_endpoint': '/health',
        'routes': ['/api/v1/etl']
    }
}

# Request metrics
request_metrics = {
    'total_requests': 0,
    'successful_requests': 0,
    'failed_requests': 0,
    'service_requests': {},
    'response_times': []
}

def log_request(func):
    """Decorator to log API requests"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        request_metrics['total_requests'] += 1

        try:
            result = func(*args, **kwargs)
            request_metrics['successful_requests'] += 1
            return result
        except Exception as e:
            request_metrics['failed_requests'] += 1
            logger.error(f"Request failed: {e}")
            raise
        finally:
            response_time = time.time() - start_time
            request_metrics['response_times'].append(response_time)
            if len(request_metrics['response_times']) > 1000:
                request_metrics['response_times'] = request_metrics['response_times'][-1000:]
    return wrapper

def route_to_service(path: str) -> Optional[Dict]:
    """Determine which service should handle the request"""
    for service_name, config in SERVICES.items():
        for route_prefix in config['routes']:
            if path.startswith(route_prefix):
                return {
                    'service': service_name,
                    'base_url': config['url'],
                    'path': path
                }
    return None

def proxy_request(service_config: Dict, path: str) -> Response:
    """Proxy request to appropriate service"""
    service_name = service_config['service']
    base_url = service_config['base_url']

    # Track service requests
    if service_name not in request_metrics['service_requests']:
        request_metrics['service_requests'][service_name] = 0
    request_metrics['service_requests'][service_name] += 1

    # Build target URL
    target_url = f"{base_url}{path}"

    # Forward request
    try:
        if request.method == 'GET':
            response = requests.get(
                target_url,
                params=request.args,
                headers=dict(request.headers),
                timeout=30
            )
        elif request.method == 'POST':
            response = requests.post(
                target_url,
                json=request.get_json(),
                headers=dict(request.headers),
                timeout=30
            )
        elif request.method == 'PUT':
            response = requests.put(
                target_url,
                json=request.get_json(),
                headers=dict(request.headers),
                timeout=30
            )
        elif request.method == 'DELETE':
            response = requests.delete(
                target_url,
                headers=dict(request.headers),
                timeout=30
            )
        else:
            return jsonify({'error': 'Method not allowed'}), 405

        # Return response
        return Response(
            response.content,
            status=response.status_code,
            headers=dict(response.headers)
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Error proxying to {service_name}: {e}")
        return jsonify({
            'error': f'Service {service_name} unavailable',
            'message': str(e)
        }), 503

@app.route('/health', methods=['GET'])
def health():
    """Gateway health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'api-gateway',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/v1/gateway/stats', methods=['GET'])
def gateway_stats():
    """Get gateway statistics"""
    avg_response_time = (
        sum(request_metrics['response_times']) / len(request_metrics['response_times'])
        if request_metrics['response_times'] else 0
    )

    return jsonify({
        'total_requests': request_metrics['total_requests'],
        'successful_requests': request_metrics['successful_requests'],
        'failed_requests': request_metrics['failed_requests'],
        'service_requests': request_metrics['service_requests'],
        'average_response_time': avg_response_time,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/v1/vector/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@log_request
def vector_api_proxy(subpath):
    """Proxy requests to vector API"""
    full_path = f"/api/v1/{subpath}"
    service_config = route_to_service(full_path)

    if not service_config:
        return jsonify({'error': 'Route not found'}), 404

    return proxy_request(service_config, full_path)

@app.route('/api/v1/search', methods=['GET', 'POST'])
@log_request
def search_proxy():
    """Proxy search requests to vector API"""
    service_config = route_to_service('/api/v1/search')
    if not service_config:
        return jsonify({'error': 'Service not found'}), 404
    return proxy_request(service_config, '/api/v1/search')

@app.route('/api/v1/stats', methods=['GET'])
@log_request
def stats_proxy():
    """Proxy stats requests to vector API"""
    service_config = route_to_service('/api/v1/stats')
    if not service_config:
        return jsonify({'error': 'Service not found'}), 404
    return proxy_request(service_config, '/api/v1/stats')

@app.route('/api/v1/embed', methods=['POST'])
@log_request
def embed_proxy():
    """Proxy embed requests to vector API"""
    service_config = route_to_service('/api/v1/embed')
    if not service_config:
        return jsonify({'error': 'Service not found'}), 404
    return proxy_request(service_config, '/api/v1/embed')

@app.route('/api/v1/analyze/<path:subpath>', methods=['GET', 'POST'])
@log_request
def analyze_proxy(subpath):
    """Proxy analysis requests to R API"""
    full_path = f"/api/v1/analyze/{subpath}"
    service_config = route_to_service(full_path)

    if not service_config:
        return jsonify({'error': 'Route not found'}), 404

    return proxy_request(service_config, full_path)

@app.route('/api/v1/etl/<path:subpath>', methods=['GET', 'POST'])
@log_request
def etl_proxy(subpath):
    """Proxy ETL requests to Python ETL service"""
    full_path = f"/api/v1/etl/{subpath}"
    service_config = route_to_service(full_path)

    if not service_config:
        return jsonify({'error': 'Route not found'}), 404

    return proxy_request(service_config, full_path)

@app.route('/', methods=['GET'])
def root():
    """API Gateway root endpoint"""
    return jsonify({
        'service': 'api-gateway',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'gateway_stats': '/api/v1/gateway/stats',
            'vector_api': '/api/v1/vector/*',
            'search': '/api/v1/search',
            'stats': '/api/v1/stats',
            'embed': '/api/v1/embed',
            'analyze': '/api/v1/analyze/*',
            'etl': '/api/v1/etl/*'
        }
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('GATEWAY_PORT', '8080'))
    app.run(host='0.0.0.0', port=port, debug=False)
