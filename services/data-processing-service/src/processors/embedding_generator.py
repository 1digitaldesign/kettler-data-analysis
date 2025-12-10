"""
Embedding Generator
Generates embeddings using sentence-transformers
"""

from sentence_transformers import SentenceTransformer
import numpy as np
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Generate embeddings for text data"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding generator with specified model

        Args:
            model_name: HuggingFace model name for sentence transformers
        """
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.dimension = self.model.get_sentence_embedding_dimension()
        logger.info(f"Embedding model loaded. Dimension: {self.dimension}")

    async def generate_embedding(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> np.ndarray:
        """
        Generate embedding for a single text

        Args:
            text: Text to embed
            metadata: Optional metadata (not used in embedding, but returned)

        Returns:
            numpy array of embeddings
        """
        try:
            if not text or not text.strip():
                raise ValueError("Text cannot be empty")

            embedding = self.model.encode(text, normalize_embeddings=True)
            logger.debug(f"Generated embedding for text (length: {len(text)})")

            return embedding

        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    async def generate_batch_embeddings(
        self,
        texts: List[str],
        metadata_list: Optional[List[Dict[str, Any]]] = None
    ) -> List[np.ndarray]:
        """
        Generate embeddings for multiple texts (batch processing)

        Args:
            texts: List of texts to embed
            metadata_list: Optional list of metadata dicts

        Returns:
            List of numpy arrays
        """
        try:
            if not texts:
                raise ValueError("Texts list cannot be empty")

            # Filter empty texts
            valid_texts = [t for t in texts if t and t.strip()]
            if not valid_texts:
                raise ValueError("No valid texts to embed")

            embeddings = self.model.encode(
                valid_texts,
                normalize_embeddings=True,
                show_progress_bar=False,
                batch_size=32
            )

            logger.info(f"Generated {len(embeddings)} embeddings in batch")

            return embeddings.tolist() if isinstance(embeddings, np.ndarray) else embeddings

        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the embedding model"""
        return {
            "model_name": self.model_name,
            "dimension": self.dimension,
            "max_seq_length": self.model.max_seq_length if hasattr(self.model, 'max_seq_length') else None
        }
