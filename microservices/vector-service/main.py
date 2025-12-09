#!/usr/bin/env python3
"""
Vector Service
Handles vector embeddings and similarity search
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import sys
from pathlib import Path
import os

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from scripts.etl.vector_embeddings import VectorEmbeddingSystem
    VECTOR_SYSTEM_AVAILABLE = True
except ImportError:
    VECTOR_SYSTEM_AVAILABLE = False
    VectorEmbeddingSystem = None

from scripts.architecture import RepositoryFactory
from scripts.utils.paths import DATA_VECTORS_DIR

app = FastAPI(
    title="Vector Service",
    description="Microservice for vector embeddings and similarity search",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service
vector_repository = RepositoryFactory.create_vector_repository(str(DATA_VECTORS_DIR))
vector_system = None

if VECTOR_SYSTEM_AVAILABLE:
    try:
        vector_system = VectorEmbeddingSystem()
    except Exception as e:
        print(f"Warning: Could not initialize vector system: {e}")


class EmbedRequest(BaseModel):
    """Embedding request model"""
    texts: List[str]
    model: Optional[str] = None


class SearchRequest(BaseModel):
    """Search request model"""
    query: str
    top_k: int = 10
    filters: Optional[Dict[str, Any]] = None


class IndexRequest(BaseModel):
    """Index request model"""
    documents: List[Dict[str, Any]]


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "vector",
        "vector_system_available": VECTOR_SYSTEM_AVAILABLE,
        "vector_system_initialized": vector_system is not None
    }


@app.post("/vectors/embed")
async def create_embeddings(request: EmbedRequest):
    """Create embeddings for texts"""
    if not vector_system:
        raise HTTPException(status_code=503, detail="Vector system not available")

    try:
        embeddings = []
        for text in request.texts:
            embedding = vector_system.create_embedding(text)
            embeddings.append({
                "text": text,
                "embedding": embedding.tolist() if hasattr(embedding, 'tolist') else embedding
            })

        return {
            "status": "success",
            "embeddings": embeddings,
            "count": len(embeddings)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/vectors/search")
async def vector_search(request: SearchRequest):
    """Vector similarity search"""
    if not vector_repository:
        raise HTTPException(status_code=503, detail="Vector repository not available")

    try:
        # Create query embedding
        if vector_system:
            query_embedding = vector_system.create_embedding(request.query)
            query_vector = query_embedding.tolist() if hasattr(query_embedding, 'tolist') else query_embedding
        else:
            raise HTTPException(status_code=503, detail="Vector system not available for search")

        # Search
        results = vector_repository.search_similar(query_vector, top_k=request.top_k)

        return {
            "status": "success",
            "query": request.query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/vectors/index")
async def index_documents(request: IndexRequest):
    """Index documents"""
    if not vector_system or not vector_repository:
        raise HTTPException(status_code=503, detail="Vector system not available")

    try:
        indexed = []
        for doc in request.documents:
            # Create embedding
            text = doc.get("text", doc.get("content", ""))
            embedding = vector_system.create_embedding(text)

            # Store in repository
            doc_id = doc.get("id", doc.get("_id", f"doc_{len(indexed)}"))
            doc_data = {
                "id": doc_id,
                "text": text,
                "metadata": doc.get("metadata", {}),
                "embedding": embedding.tolist() if hasattr(embedding, 'tolist') else embedding
            }
            vector_repository.save(doc_data)
            indexed.append(doc_id)

        return {
            "status": "success",
            "indexed": indexed,
            "count": len(indexed)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/vectors/status")
async def vector_status():
    """Get vector service status"""
    return {
        "status": "healthy",
        "vector_system_available": VECTOR_SYSTEM_AVAILABLE,
        "vector_system_initialized": vector_system is not None,
        "repository_initialized": vector_repository is not None
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8004"))
    uvicorn.run(app, host="0.0.0.0", port=port)
