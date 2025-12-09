#!/usr/bin/env python3
"""
Vector Embedding System
Creates embeddings for all data types (CSV, JSON, PDF, Excel)
"""

import os
import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import hashlib
import pickle
from datetime import datetime

# Hugging Face authentication
HF_WRITE_TOKEN = os.getenv('HF_WRITE_TOKEN', '')
HF_READ_TOKEN = os.getenv('HF_READ_TOKEN', '')

# Set Hugging Face tokens if available
if HF_WRITE_TOKEN:
    os.environ['HF_TOKEN'] = HF_WRITE_TOKEN
    os.environ['HUGGING_FACE_HUB_TOKEN'] = HF_WRITE_TOKEN
if HF_READ_TOKEN:
    os.environ['HF_READ_TOKEN'] = HF_READ_TOKEN

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available. Install with: pip install sentence-transformers")

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("Warning: faiss-cpu not available. Install with: pip install faiss-cpu")

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
VECTOR_STORE_DIR = PROJECT_ROOT / "data" / "vectors"
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

# Embedding model configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Lightweight, fast model
EMBEDDING_DIM = 384  # Dimension for all-MiniLM-L6-v2

class VectorEmbeddingSystem:
    """Manages vector embeddings for all data types"""

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model_name = model_name
        self.model = None
        self.vector_store = None
        self.metadata_store = {}
        self.vector_index_file = VECTOR_STORE_DIR / "vector_index.faiss"
        self.metadata_file = VECTOR_STORE_DIR / "metadata.json"

        if SENTENCE_TRANSFORMERS_AVAILABLE:
            print(f"Loading embedding model: {model_name}")
            # Use token for authentication if available
            model_kwargs = {}
            if HF_READ_TOKEN:
                model_kwargs['token'] = HF_READ_TOKEN
            self.model = SentenceTransformer(model_name, **model_kwargs)
        else:
            raise ImportError("sentence-transformers is required for vector embeddings")

        # Load existing vector store if available
        self._load_vector_store()

    def _load_vector_store(self):
        """Load existing vector store from disk"""
        if FAISS_AVAILABLE and self.vector_index_file.exists():
            try:
                self.vector_store = faiss.read_index(str(self.vector_index_file))
                print(f"Loaded existing vector store with {self.vector_store.ntotal} vectors")
            except Exception as e:
                print(f"Warning: Could not load existing vector store: {e}")
                self._create_new_index()
        else:
            self._create_new_index()

        # Load metadata
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    self.metadata_store = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load metadata: {e}")
                self.metadata_store = {}

    def _create_new_index(self):
        """Create a new FAISS index"""
        if FAISS_AVAILABLE:
            self.vector_store = faiss.IndexFlatL2(EMBEDDING_DIM)
        else:
            self.vector_store = None

    def _save_vector_store(self):
        """Save vector store to disk"""
        if FAISS_AVAILABLE and self.vector_store is not None:
            try:
                faiss.write_index(self.vector_store, str(self.vector_index_file))
                with open(self.metadata_file, 'w') as f:
                    json.dump(self.metadata_store, f, indent=2)
            except Exception as e:
                print(f"Error saving vector store: {e}")

    def _generate_id(self, content: str, source: str) -> str:
        """Generate unique ID for content"""
        combined = f"{source}:{content}"
        return hashlib.md5(combined.encode()).hexdigest()

    def _text_to_embedding(self, text: str) -> np.ndarray:
        """Convert text to embedding vector"""
        if not text or not text.strip():
            return np.zeros(EMBEDDING_DIM)

        # Truncate very long texts (model has limits)
        max_length = 512
        if len(text) > max_length:
            text = text[:max_length]

        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.astype('float32')

    def embed_text(self, text: str, source: str, metadata: Optional[Dict] = None) -> str:
        """Create embedding for text and add to vector store"""
        if not text or not text.strip():
            return None

        # Generate ID
        content_id = self._generate_id(text, source)

        # Check if already exists
        if content_id in self.metadata_store:
            return content_id

        # Create embedding
        embedding = self._text_to_embedding(text)

        # Add to vector store
        if FAISS_AVAILABLE and self.vector_store is not None:
            embedding_2d = embedding.reshape(1, -1)
            self.vector_store.add(embedding_2d)
            vector_index = self.vector_store.ntotal - 1
        else:
            vector_index = None

        # Store metadata
        self.metadata_store[content_id] = {
            'source': source,
            'text': text[:500],  # Store first 500 chars for reference
            'vector_index': vector_index,
            'created_at': datetime.now().isoformat(),
            'metadata': metadata or {}
        }

        return content_id

    def embed_dataframe(self, df: pd.DataFrame, source: str) -> List[str]:
        """Create embeddings for all rows in a DataFrame"""
        content_ids = []

        for idx, row in df.iterrows():
            # Combine all text columns
            text_parts = []
            for col in df.columns:
                value = row[col]
                if pd.notna(value):
                    text_parts.append(f"{col}: {str(value)}")

            text = " | ".join(text_parts)

            # Create metadata
            metadata = {
                'row_index': int(idx),
                'columns': list(df.columns),
                'data_type': 'dataframe'
            }

            content_id = self.embed_text(text, f"{source}:row_{idx}", metadata)
            if content_id:
                content_ids.append(content_id)

        return content_ids

    def embed_json(self, data: Union[Dict, List], source: str, path: str = "") -> List[str]:
        """Create embeddings for JSON data"""
        content_ids = []

        if isinstance(data, dict):
            # Embed each key-value pair
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key

                if isinstance(value, (dict, list)):
                    # Recursive for nested structures
                    content_ids.extend(self.embed_json(value, source, current_path))
                else:
                    # Embed as text
                    text = f"{key}: {str(value)}"
                    metadata = {
                        'json_path': current_path,
                        'data_type': 'json'
                    }
                    content_id = self.embed_text(text, f"{source}:{current_path}", metadata)
                    if content_id:
                        content_ids.append(content_id)

        elif isinstance(data, list):
            # Embed each item in list
            for idx, item in enumerate(data):
                current_path = f"{path}[{idx}]" if path else f"[{idx}]"

                if isinstance(item, (dict, list)):
                    content_ids.extend(self.embed_json(item, source, current_path))
                else:
                    text = str(item)
                    metadata = {
                        'json_path': current_path,
                        'data_type': 'json'
                    }
                    content_id = self.embed_text(text, f"{source}:{current_path}", metadata)
                    if content_id:
                        content_ids.append(content_id)

        return content_ids

    def search_similar(self, query_text: str, top_k: int = 10) -> List[Dict]:
        """Search for similar content"""
        if not FAISS_AVAILABLE or self.vector_store is None or self.vector_store.ntotal == 0:
            return []

        # Create query embedding
        query_embedding = self._text_to_embedding(query_text)
        query_embedding_2d = query_embedding.reshape(1, -1)

        # Search
        distances, indices = self.vector_store.search(query_embedding_2d, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            # Find metadata by vector index
            for content_id, metadata in self.metadata_store.items():
                if metadata.get('vector_index') == int(idx):
                    # Ensure all numeric values are Python native types
                    dist_float = float(dist) if hasattr(dist, 'item') else float(dist)
                    similarity_float = float(1 / (1 + dist_float))
                    results.append({
                        'content_id': str(content_id),
                        'distance': dist_float,
                        'similarity': similarity_float,
                        'source': str(metadata.get('source', '')),
                        'text': str(metadata.get('text', '')),
                        'metadata': dict(metadata.get('metadata', {}))
                    })
                    break

        return results

    def save(self):
        """Save vector store and metadata"""
        self._save_vector_store()
        print(f"Saved vector store with {len(self.metadata_store)} embeddings")

    def get_stats(self) -> Dict:
        """Get statistics about the vector store"""
        return {
            'total_embeddings': len(self.metadata_store),
            'vector_store_size': self.vector_store.ntotal if FAISS_AVAILABLE and self.vector_store else 0,
            'model': self.model_name,
            'dimension': EMBEDDING_DIM
        }
