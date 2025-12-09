#!/usr/bin/env python3
"""
Message Queue Service
Provides async message processing for microservices
"""

import os
import json
import time
import threading
from queue import Queue, Empty
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from typing import Dict, List, Optional
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory message queues (in production, use Redis/RabbitMQ)
queues: Dict[str, Queue] = {}
queue_stats: Dict[str, Dict] = {}

def get_queue(queue_name: str) -> Queue:
    """Get or create a queue"""
    if queue_name not in queues:
        queues[queue_name] = Queue()
        queue_stats[queue_name] = {
            'total_messages': 0,
            'processed_messages': 0,
            'failed_messages': 0,
            'created_at': datetime.now().isoformat()
        }
    return queues[queue_name]

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'message-queue',
        'queues': list(queues.keys()),
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/v1/queue/<queue_name>/publish', methods=['POST'])
def publish(queue_name: str):
    """Publish a message to a queue"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        queue = get_queue(queue_name)
        message = {
            'id': f"{queue_name}_{int(time.time() * 1000)}",
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'queue': queue_name
        }

        queue.put(message)
        queue_stats[queue_name]['total_messages'] += 1

        logger.info(f"Published message to {queue_name}: {message['id']}")

        return jsonify({
            'message_id': message['id'],
            'queue': queue_name,
            'status': 'published'
        }), 201
    except Exception as e:
        logger.error(f"Error publishing to {queue_name}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/queue/<queue_name>/consume', methods=['GET'])
def consume(queue_name: str):
    """Consume a message from a queue"""
    try:
        timeout = int(request.args.get('timeout', 5))
        queue = get_queue(queue_name)

        try:
            message = queue.get(timeout=timeout)
            queue_stats[queue_name]['processed_messages'] += 1

            return jsonify({
                'message': message,
                'status': 'consumed'
            }), 200
        except Empty:
            return jsonify({
                'message': None,
                'status': 'no_messages',
                'timeout': timeout
            }), 204
    except Exception as e:
        logger.error(f"Error consuming from {queue_name}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/queue/<queue_name>/stats', methods=['GET'])
def queue_stats_endpoint(queue_name: str):
    """Get queue statistics"""
    if queue_name not in queues:
        return jsonify({'error': 'Queue not found'}), 404

    stats = queue_stats[queue_name].copy()
    queue = queues[queue_name]
    stats['pending_messages'] = queue.qsize()

    return jsonify(stats), 200

@app.route('/api/v1/queues', methods=['GET'])
def list_queues():
    """List all queues"""
    return jsonify({
        'queues': [
            {
                'name': name,
                'size': queue.qsize(),
                'stats': queue_stats.get(name, {})
            }
            for name, queue in queues.items()
        ]
    }), 200

@app.route('/api/v1/queue/<queue_name>/ack', methods=['POST'])
def acknowledge(queue_name: str):
    """Acknowledge message processing"""
    try:
        data = request.get_json()
        message_id = data.get('message_id')

        if not message_id:
            return jsonify({'error': 'message_id required'}), 400

        # In a real implementation, track message processing
        logger.info(f"Acknowledged message {message_id} from {queue_name}")

        return jsonify({
            'message_id': message_id,
            'status': 'acknowledged'
        }), 200
    except Exception as e:
        logger.error(f"Error acknowledging message: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('MESSAGE_QUEUE_PORT', '8082'))
    app.run(host='0.0.0.0', port=port, debug=False)
