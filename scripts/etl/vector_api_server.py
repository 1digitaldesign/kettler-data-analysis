#!/usr/bin/env python3
"""
Vector API Server
REST API for querying vector embeddings
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.etl.vector_embeddings import VectorEmbeddingSystem

app = Flask(__name__)
CORS(app)

# Initialize vector system
vector_system = None

def get_vector_system():
    global vector_system
    if vector_system is None:
        vector_system = VectorEmbeddingSystem()
    return vector_system

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/v1/search', methods=['POST'])
def search():
    """Search for similar content"""
    try:
        data = request.json
        query_text = data.get('query', '')
        top_k = data.get('top_k', 10)

        if not query_text:
            return jsonify({'error': 'query parameter is required'}), 400

        vs = get_vector_system()
        results = vs.search_similar(query_text, top_k=top_k)

        return jsonify({
            'query': query_text,
            'results': results,
            'count': len(results)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/stats', methods=['GET'])
def stats():
    """Get vector store statistics"""
    try:
        vs = get_vector_system()
        stats = vs.get_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/embed', methods=['POST'])
def embed():
    """Create embedding for text"""
    try:
        data = request.json
        text = data.get('text', '')
        source = data.get('source', 'api')
        metadata = data.get('metadata', {})

        if not text:
            return jsonify({'error': 'text parameter is required'}), 400

        vs = get_vector_system()
        content_id = vs.embed_text(text, source, metadata)
        vs.save()

        return jsonify({
            'content_id': content_id,
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
