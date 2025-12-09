#!/usr/bin/env python3
"""
Validation Microservice
Handles all data validation operations
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

from scripts.architecture import ValidationService, RepositoryFactory
from scripts.utils.paths import DATA_SOURCE_DIR

app = FastAPI(
    title="Validation Service",
    description="Microservice for data validation operations",
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
validation_service = None

if firms_file.exists():
    firm_repository = RepositoryFactory.create_firm_repository(str(firms_file))
    validation_service = ValidationService(firm_repository)


class ValidationRequest(BaseModel):
    """Validation request model"""
    data: Any
    validation_type: str


class BatchValidationRequest(BaseModel):
    """Batch validation request model"""
    items: List[Dict[str, Any]]
    validation_type: str


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "validation",
        "repository_initialized": firm_repository is not None
    }


@app.post("/validate/license")
async def validate_license(request: ValidationRequest):
    """Validate license number"""
    if not validation_service:
        raise HTTPException(status_code=503, detail="Validation service not initialized")

    try:
        result = validation_service.execute("license", request.data)
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/validate/address")
async def validate_address(request: ValidationRequest):
    """Validate address"""
    if not validation_service:
        raise HTTPException(status_code=503, detail="Validation service not initialized")

    try:
        result = validation_service.execute("address", request.data)
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/validate/firm")
async def validate_firm(request: ValidationRequest):
    """Validate firm"""
    if not validation_service:
        raise HTTPException(status_code=503, detail="Validation service not initialized")

    try:
        # Convert dict to Firm if needed
        from scripts.architecture.models import Firm
        if isinstance(request.data, dict):
            firm = Firm(**request.data)
        else:
            firm = request.data

        result = validation_service.execute("firm", firm)
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/validate/batch")
async def validate_batch(request: BatchValidationRequest):
    """Batch validation"""
    if not validation_service:
        raise HTTPException(status_code=503, detail="Validation service not initialized")

    try:
        results = []
        for item in request.items:
            result = validation_service.execute(request.validation_type, item)
            results.append(result)

        return {
            "status": "success",
            "results": results,
            "total": len(results),
            "valid": sum(1 for r in results if r.get("valid", False)),
            "invalid": sum(1 for r in results if not r.get("valid", False))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8003"))
    uvicorn.run(app, host="0.0.0.0", port=port)
