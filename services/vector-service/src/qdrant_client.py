"""
Qdrant Client Wrapper
Provides convenient methods for Qdrant operations
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os
import logging

logger = logging.getLogger(__name__)

class QdrantClientWrapper:
    """Wrapper for Qdrant client with convenience methods"""

    def __init__(self):
        QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
        QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
        QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")

        self.client = QdrantClient(
            host=QDRANT_HOST,
            port=QDRANT_PORT,
            api_key=QDRANT_API_KEY if QDRANT_API_KEY else None
        )
        logger.info(f"Qdrant client initialized: {QDRANT_HOST}:{QDRANT_PORT}")

    def ensure_collection(self, collection_name: str, vector_size: int):
        """Ensure collection exists, create if not"""
        try:
            collections = self.client.get_collections()
            existing_names = [c.name for c in collections.collections]

            if collection_name not in existing_names:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {collection_name}")
            else:
                logger.debug(f"Collection already exists: {collection_name}")
        except Exception as e:
            logger.error(f"Error ensuring collection {collection_name}: {e}")
            raise

    def get_client(self):
        """Get the underlying Qdrant client"""
        return self.client
