"""
Data Processing Service - FastAPI Server

Provides REST API endpoints for data processing, R script execution, and embedding generation
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv

from processors.r_processor import RProcessor
from processors.python_processor import PythonProcessor
from processors.embedding_generator import EmbeddingGenerator

load_dotenv()

app = FastAPI(
    title="Data Processing Service",
    description="Microservice for data processing, R script execution, and embedding generation",
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

# Initialize processors
r_processor = RProcessor()
python_processor = PythonProcessor()
embedding_generator = EmbeddingGenerator()

# Health check
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "data-processing-service",
        "timestamp": __import__("datetime").datetime.now().isoformat()
    }

# Request models
class ConsolidateRequest(BaseModel):
    state: Optional[str] = None
    output_format: str = "csv"

class GenerateLettersRequest(BaseModel):
    states: List[str]
    output_dir: Optional[str] = None

class EmbeddingRequest(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None

class BatchEmbeddingRequest(BaseModel):
    texts: List[str]
    metadata: Optional[List[Dict[str, Any]]] = None

# API Routes

@app.post("/api/v1/process/consolidate")
async def consolidate_findings(request: ConsolidateRequest):
    """
    Run consolidation scripts to combine license findings
    """
    try:
        result = await r_processor.run_consolidation_script(
            state=request.state,
            output_format=request.output_format
        )
        return {
            "status": "success",
            "result": result,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/process/generate-letters")
async def generate_letters(request: GenerateLettersRequest, background_tasks: BackgroundTasks):
    """
    Generate complaint letters for specified states
    """
    try:
        result = await r_processor.run_letter_generation_script(
            states=request.states,
            output_dir=request.output_dir
        )
        return {
            "status": "success",
            "result": result,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/process/embeddings")
async def generate_embeddings(request: EmbeddingRequest):
    """
    Generate embeddings for a single text
    """
    try:
        embedding = await embedding_generator.generate_embedding(
            text=request.text,
            metadata=request.metadata
        )
        return {
            "status": "success",
            "embedding": embedding.tolist(),
            "dimension": len(embedding),
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/process/embeddings/batch")
async def generate_batch_embeddings(request: BatchEmbeddingRequest):
    """
    Generate embeddings for multiple texts
    """
    try:
        embeddings = await embedding_generator.generate_batch_embeddings(
            texts=request.texts,
            metadata_list=request.metadata
        )
        return {
            "status": "success",
            "embeddings": [emb.tolist() for emb in embeddings],
            "count": len(embeddings),
            "dimension": len(embeddings[0]) if embeddings else 0,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/process/transform")
async def transform_data(data: Dict[str, Any]):
    """
    Transform data using Python processors
    """
    try:
        result = await python_processor.transform(data)
        return {
            "status": "success",
            "result": result,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3002)
