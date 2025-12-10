#!/usr/bin/env python3
"""
Scraping Microservice
Handles all web scraping operations
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

from scripts.architecture import ScrapingService, RepositoryFactory
from scripts.utils.paths import DATA_SCRAPED_DIR

app = FastAPI(
    title="Scraping Service",
    description="Microservice for web scraping operations",
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
file_repository = RepositoryFactory.create_file_repository(str(DATA_SCRAPED_DIR))
scraping_service = ScrapingService(file_repository)


class ScrapingRequest(BaseModel):
    """Scraping request model"""
    targets: List[str]
    options: Optional[Dict[str, Any]] = None


class ACRISRequest(BaseModel):
    """ACRIS request model"""
    search_type: str
    params: Dict[str, Any]


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "scraping"
    }


@app.post("/scrape/airbnb")
async def scrape_airbnb(request: ScrapingRequest):
    """Scrape Airbnb listings"""
    try:
        results = scraping_service.execute(
            "airbnb",
            request.targets,
            max_pages=request.options.get("max_pages", 3) if request.options else 3
        )
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scrape/vrbo")
async def scrape_vrbo(request: ScrapingRequest):
    """Scrape VRBO listings"""
    try:
        results = scraping_service.execute(
            "vrbo",
            request.targets,
            max_pages=request.options.get("max_pages", 3) if request.options else 3
        )
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scrape/front")
async def scrape_front(request: ScrapingRequest):
    """Scrape Front website"""
    try:
        results = scraping_service.execute("front", request.targets)
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scrape/acris")
async def scrape_acris(request: ACRISRequest):
    """Scrape ACRIS property records"""
    try:
        results = scraping_service.execute(
            "acris",
            [],
            search_type=request.search_type,
            **request.params
        )
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8002"))
    uvicorn.run(app, host="0.0.0.0", port=port)
