#!/usr/bin/env python3
"""
Metrics Collector Service
Collects and aggregates metrics from all microservices
"""

import os
import time
import requests
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from typing import Dict, List
import logging
from collections import defaultdict

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Metrics storage
metrics_store: Dict[str, List[Dict]] = defaultdict(list)
service_endpoints = {
    'vector-api': os.getenv('VECTOR_API_SERVICE', 'http://vector-api:8000'),
    'r-api': os.getenv('R_API_SERVICE', 'http://r-api:8001'),
    'python-etl': os.getenv('PYTHON_ETL_SERVICE', 'http://python-etl:8000'),
    'service-discovery': os.getenv('SERVICE_DISCOVERY_URL', 'http://service-discovery:8080'),
    'api-gateway': os.getenv('API_GATEWAY_URL', 'http://api-gateway:8080'),
    'message-queue': os.getenv('MESSAGE_QUEUE_URL', 'http://message-queue:8082')
}

def collect_service_metrics(service_name: str, base_url: str) -> Dict:
    """Collect metrics from a service"""
    metrics = {
        'service': service_name,
        'timestamp': datetime.now().isoformat(),
        'health': 'unknown',
        'response_time': None,
        'error': None
    }

    try:
        start_time = time.time()
        response = requests.get(f"{base_url}/health", timeout=5)
        response_time = time.time() - start_time

        if response.status_code == 200:
            metrics['health'] = 'healthy'
            metrics['response_time'] = response_time
            data = response.json()
            metrics['data'] = data
        else:
            metrics['health'] = 'unhealthy'
            metrics['error'] = f"HTTP {response.status_code}"
    except Exception as e:
        metrics['health'] = 'unreachable'
        metrics['error'] = str(e)

    return metrics

def collect_all_metrics():
    """Collect metrics from all services"""
    all_metrics = []

    for service_name, base_url in service_endpoints.items():
        metrics = collect_service_metrics(service_name, base_url)
        all_metrics.append(metrics)

        # Store metrics (keep last 1000)
        metrics_store[service_name].append(metrics)
        if len(metrics_store[service_name]) > 1000:
            metrics_store[service_name] = metrics_store[service_name][-1000:]

    return all_metrics

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'metrics-collector',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/v1/metrics', methods=['GET'])
def get_metrics():
    """Get current metrics from all services"""
    metrics = collect_all_metrics()
    return jsonify({
        'metrics': metrics,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/v1/metrics/<service_name>', methods=['GET'])
def get_service_metrics(service_name: str):
    """Get metrics for a specific service"""
    if service_name not in metrics_store:
        return jsonify({'error': 'Service not found'}), 404

    # Get time range
    hours = int(request.args.get('hours', 1))
    cutoff_time = datetime.now() - timedelta(hours=hours)

    recent_metrics = [
        m for m in metrics_store[service_name]
        if datetime.fromisoformat(m['timestamp']) > cutoff_time
    ]

    # Calculate statistics
    healthy_count = sum(1 for m in recent_metrics if m['health'] == 'healthy')
    response_times = [m['response_time'] for m in recent_metrics if m['response_time']]

    stats = {
        'service': service_name,
        'total_samples': len(recent_metrics),
        'healthy_samples': healthy_count,
        'health_percentage': (healthy_count / len(recent_metrics) * 100) if recent_metrics else 0,
        'average_response_time': sum(response_times) / len(response_times) if response_times else None,
        'min_response_time': min(response_times) if response_times else None,
        'max_response_time': max(response_times) if response_times else None,
        'recent_metrics': recent_metrics[-10:]  # Last 10 samples
    }

    return jsonify(stats), 200

@app.route('/api/v1/metrics/summary', methods=['GET'])
def get_summary():
    """Get summary of all service metrics"""
    summary = []

    for service_name in service_endpoints.keys():
        if service_name in metrics_store and metrics_store[service_name]:
            recent = metrics_store[service_name][-1]
            summary.append({
                'service': service_name,
                'health': recent.get('health', 'unknown'),
                'response_time': recent.get('response_time'),
                'last_check': recent.get('timestamp')
            })

    return jsonify({
        'summary': summary,
        'timestamp': datetime.now().isoformat()
    }), 200

def background_collection():
    """Background task to collect metrics periodically"""
    interval = int(os.getenv('METRICS_COLLECTION_INTERVAL', '30'))

    while True:
        try:
            collect_all_metrics()
            logger.info(f"Collected metrics from {len(service_endpoints)} services")
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")

        time.sleep(interval)

if __name__ == '__main__':
    import threading

    # Start background collection
    collection_thread = threading.Thread(target=background_collection, daemon=True)
    collection_thread.start()

    port = int(os.getenv('METRICS_COLLECTOR_PORT', '8083'))
    app.run(host='0.0.0.0', port=port, debug=False)
