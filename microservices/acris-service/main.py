#!/usr/bin/env python3
"""
ACRIS Service
Handles ACRIS property records operations
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
    from scripts.scraping.acris_scraper import ACRISScraper
    ACRIS_AVAILABLE = True
except ImportError:
    ACRIS_AVAILABLE = False
    ACRISScraper = None

app = FastAPI(
    title="ACRIS Service",
    description="Microservice for ACRIS property records operations",
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
acris_scraper = None

if ACRIS_AVAILABLE:
    try:
        acris_scraper = ACRISScraper()
    except Exception as e:
        print(f"Warning: Could not initialize ACRIS scraper: {e}")


class BlockLotRequest(BaseModel):
    """Block/Lot search request"""
    borough: str
    block: str
    lot: str


class AddressRequest(BaseModel):
    """Address search request"""
    address: str
    borough: Optional[str] = None


class PartyRequest(BaseModel):
    """Party name search request"""
    party_name: str
    document_type: Optional[str] = None


class DocumentRequest(BaseModel):
    """Document ID search request"""
    document_id: str


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "acris",
        "acris_available": ACRIS_AVAILABLE,
        "acris_initialized": acris_scraper is not None
    }


@app.post("/acris/search/block-lot")
async def search_block_lot(request: BlockLotRequest):
    """Search ACRIS by block/lot"""
    if not acris_scraper:
        raise HTTPException(status_code=503, detail="ACRIS scraper not available")

    try:
        results = acris_scraper.search_by_block_lot(
            request.borough,
            request.block,
            request.lot
        )

        return {
            "status": "success",
            "results": results,
            "count": len(results) if isinstance(results, list) else 1
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/acris/search/address")
async def search_address(request: AddressRequest):
    """Search ACRIS by address"""
    if not acris_scraper:
        raise HTTPException(status_code=503, detail="ACRIS scraper not available")

    try:
        results = acris_scraper.search_by_address(
            request.address,
            request.borough
        )

        return {
            "status": "success",
            "results": results,
            "count": len(results) if isinstance(results, list) else 1
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/acris/search/party")
async def search_party(request: PartyRequest):
    """Search ACRIS by party name"""
    if not acris_scraper:
        raise HTTPException(status_code=503, detail="ACRIS scraper not available")

    try:
        results = acris_scraper.search_by_party_name(
            request.party_name,
            request.document_type
        )

        return {
            "status": "success",
            "results": results,
            "count": len(results) if isinstance(results, list) else 1
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/acris/search/document")
async def search_document(request: DocumentRequest):
    """Search ACRIS by document ID"""
    if not acris_scraper:
        raise HTTPException(status_code=503, detail="ACRIS scraper not available")

    try:
        result = acris_scraper.search_by_document_id(request.document_id)

        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8006"))
    uvicorn.run(app, host="0.0.0.0", port=port)
