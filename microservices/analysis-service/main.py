#!/usr/bin/env python3
"""
Analysis Microservice
Handles all data analysis operations
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Any, Optional
import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.validation import (
    validate_dict, validate_string, validate_list,
    ValidationError
)
from utils.redundancy import with_redundancy

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.architecture import (
    RepositoryFactory, AnalysisService,
    FraudAnalysisStrategy, NexusAnalysisStrategy,
    ConnectionAnalysisStrategy, ViolationAnalysisStrategy
)
from scripts.utils.paths import DATA_SOURCE_DIR

app = FastAPI(
    title="Analysis Service",
    description="Microservice for data analysis operations",
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
firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.json"
if not firms_file.exists():
    firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.csv"

firm_repository = None
analysis_service = None

if firms_file.exists():
    firm_repository = RepositoryFactory.create_firm_repository(str(firms_file))
    analysis_service = AnalysisService(firm_repository)


class AnalysisRequest(BaseModel):
    """Analysis request model with validation"""
    filters: Optional[Dict[str, Any]] = Field(None, max_length=1000)
    options: Optional[Dict[str, Any]] = Field(None, max_length=1000)
    
    @validator('filters')
    def validate_filters(cls, v):
        if v is not None:
            if not isinstance(v, dict):
                raise ValueError("filters must be a dictionary")
            if len(str(v)) > 10000:  # Limit size
                raise ValueError("filters too large")
        return v
    
    @validator('options')
    def validate_options(cls, v):
        if v is not None:
            if not isinstance(v, dict):
                raise ValueError("options must be a dictionary")
            if len(str(v)) > 10000:  # Limit size
                raise ValueError("options too large")
        return v


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "analysis",
        "repository_initialized": firm_repository is not None
    }


@with_redundancy(
    func_key="analyze_fraud",
    cache_key=None,
    alternatives=None,
    fallback_func=lambda: {"status": "degraded", "results": {}, "message": "Service degraded"}
)
@app.post("/analyze/fraud")
async def analyze_fraud(request: AnalysisRequest):
    """Analyze fraud patterns with redundancy"""
    # Input validation (Fallback 1)
    try:
        if request.filters:
            validate_dict(request.filters, "filters")
        if request.options:
            validate_dict(request.options, "options")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Service availability (Fallback 2)
    if not analysis_service:
        raise HTTPException(status_code=503, detail="Analysis service not initialized")
    
    # Execute with redundancy (Fallbacks 3-6 handled by decorator)
    try:
        results = analysis_service.analyze_fraud_patterns()
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        logger.error(f"Error in fraud analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/nexus")
async def analyze_nexus(request: AnalysisRequest):
    """Analyze nexus patterns"""
    if not analysis_service:
        raise HTTPException(status_code=503, detail="Analysis service not initialized")

    try:
        results = analysis_service.analyze_nexus_patterns()
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/connections")
async def analyze_connections(request: AnalysisRequest):
    """Analyze connections"""
    if not analysis_service:
        raise HTTPException(status_code=503, detail="Analysis service not initialized")

    try:
        results = analysis_service.analyze_connections()
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/violations")
async def analyze_violations(request: AnalysisRequest):
    """Analyze violations"""
    if not analysis_service:
        raise HTTPException(status_code=503, detail="Analysis service not initialized")

    try:
        results = analysis_service.analyze_violations()
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/all")
async def analyze_all(request: AnalysisRequest):
    """Run all analyses"""
    if not analysis_service:
        raise HTTPException(status_code=503, detail="Analysis service not initialized")

    try:
        results = analysis_service.execute()
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", "8001"))
    uvicorn.run(app, host="0.0.0.0", port=port)
