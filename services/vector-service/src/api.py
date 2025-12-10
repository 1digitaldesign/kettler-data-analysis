"""
Vector Service - FastAPI Server

Provides REST API endpoints for vector storage, similarity search, and Qdrant operations
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from embeddings import EmbeddingGenerator

load_dotenv()

app = FastAPI(
    title="Vector Service",
    description="Microservice for vector storage and similarity search using Qdrant",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Qdrant client
QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")

qdrant_client = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT,
    api_key=QDRANT_API_KEY if QDRANT_API_KEY else None
)

# Initialize embedding generator
embedding_generator = EmbeddingGenerator()

# Collection names
COLLECTIONS = {
    "license_findings": "license_findings",
    "employees": "employees",
    "violations": "violations"
}

# Initialize collections on startup
@app.on_event("startup")
async def initialize_collections():
    """Create collections if they don't exist"""
    for collection_name in COLLECTIONS.values():
        try:
            collections = qdrant_client.get_collections()
            existing_names = [c.name for c in collections.collections]

            if collection_name not in existing_names:
                qdrant_client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=embedding_generator.dimension,
                        distance=Distance.COSINE
                    )
                )
                print(f"Created collection: {collection_name}")
        except Exception as e:
            print(f"Error initializing collection {collection_name}: {e}")

# Health check
@app.get("/health")
async def health():
    try:
        # Check Qdrant connection
        collections = qdrant_client.get_collections()
        return {
            "status": "healthy",
            "service": "vector-service",
            "qdrant_connected": True,
            "collections": len(collections.collections),
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "vector-service",
            "qdrant_connected": False,
            "error": str(e),
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }

# Request models
class StoreVectorRequest(BaseModel):
    collection: str
    text: str
    metadata: Dict[str, Any]
    id: Optional[str] = None

class BatchStoreVectorRequest(BaseModel):
    collection: str
    items: List[Dict[str, Any]]  # List of {text, metadata, id}

class SearchRequest(BaseModel):
    collection: str
    query_text: str
    limit: int = 10
    score_threshold: Optional[float] = None
    filter: Optional[Dict[str, Any]] = None

# API Routes

@app.post("/api/v1/vectors/store")
async def store_vector(request: StoreVectorRequest):
    """
    Store a single vector with metadata
    """
    try:
        if request.collection not in COLLECTIONS.values():
            raise HTTPException(status_code=400, detail=f"Invalid collection: {request.collection}")

        # Generate embedding
        embedding = await embedding_generator.generate_embedding(request.text)

        # Prepare point
        point_id = request.id or __import__("uuid").uuid4().hex
        point = PointStruct(
            id=point_id,
            vector=embedding.tolist(),
            payload=request.metadata
        )

        # Store in Qdrant
        qdrant_client.upsert(
            collection_name=request.collection,
            points=[point]
        )

        return {
            "status": "success",
            "id": point_id,
            "collection": request.collection,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/vectors/store/batch")
async def store_batch_vectors(request: BatchStoreVectorRequest):
    """
    Store multiple vectors in batch
    """
    try:
        if request.collection not in COLLECTIONS.values():
            raise HTTPException(status_code=400, detail=f"Invalid collection: {request.collection}")

        # Generate embeddings for all texts
        texts = [item["text"] for item in request.items]
        embeddings = await embedding_generator.generate_batch_embeddings(texts)

        # Prepare points
        points = []
        for i, item in enumerate(request.items):
            point_id = item.get("id") or __import__("uuid").uuid4().hex
            point = PointStruct(
                id=point_id,
                vector=embeddings[i],
                payload=item.get("metadata", {})
            )
            points.append(point)

        # Store in Qdrant
        qdrant_client.upsert(
            collection_name=request.collection,
            points=points
        )

        return {
            "status": "success",
            "count": len(points),
            "collection": request.collection,
            "ids": [p.id for p in points],
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/vectors/search")
async def search_vectors(request: SearchRequest):
    """
    Search for similar vectors
    """
    try:
        if request.collection not in COLLECTIONS.values():
            raise HTTPException(status_code=400, detail=f"Invalid collection: {request.collection}")

        # Generate query embedding
        query_embedding = await embedding_generator.generate_embedding(request.query_text)

        # Build filter if provided
        qdrant_filter = None
        if request.filter:
            from qdrant_client.models import Filter, FieldCondition, MatchValue
            conditions = []
            for key, value in request.filter.items():
                conditions.append(
                    FieldCondition(key=key, match=MatchValue(value=value))
                )
            if conditions:
                qdrant_filter = Filter(must=conditions)

        # Search
        search_results = qdrant_client.search(
            collection_name=request.collection,
            query_vector=query_embedding.tolist(),
            limit=request.limit,
            score_threshold=request.score_threshold,
            query_filter=qdrant_filter
        )

        # Format results
        results = []
        for result in search_results:
            results.append({
                "id": result.id,
                "score": result.score,
                "metadata": result.payload
            })

        return {
            "status": "success",
            "query": request.query_text,
            "results": results,
            "count": len(results),
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/vectors/{collection}/{id}")
async def get_vector(collection: str, id: str):
    """
    Retrieve a specific vector by ID
    """
    try:
        if collection not in COLLECTIONS.values():
            raise HTTPException(status_code=400, detail=f"Invalid collection: {collection}")

        result = qdrant_client.retrieve(
            collection_name=collection,
            ids=[id]
        )

        if not result:
            raise HTTPException(status_code=404, detail="Vector not found")

        point = result[0]
        return {
            "status": "success",
            "id": point.id,
            "metadata": point.payload,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/vectors/collections")
async def list_collections():
    """
    List all collections
    """
    try:
        collections = qdrant_client.get_collections()
        return {
            "status": "success",
            "collections": [
                {
                    "name": c.name,
                    "vectors_count": qdrant_client.get_collection(c.name).vectors_count
                }
                for c in collections.collections
            ],
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/vectors/{collection}/{id}")
async def delete_vector(collection: str, id: str):
    """
    Delete a vector by ID
    """
    try:
        if collection not in COLLECTIONS.values():
            raise HTTPException(status_code=400, detail=f"Invalid collection: {collection}")

        qdrant_client.delete(
            collection_name=collection,
            points_selector=[id]
        )

        return {
            "status": "success",
            "id": id,
            "collection": collection,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3003)
