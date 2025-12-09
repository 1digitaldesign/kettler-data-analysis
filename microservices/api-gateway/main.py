#!/usr/bin/env python3
"""
API Gateway for Microservices Architecture
Routes requests from Next.js/Vercel to GCP microservices
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import os
import sys
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.validation import validate_json_payload, sanitize_input
from utils.redundancy import redundancy_manager, with_redundancy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Kettler Data Analysis API Gateway",
    description="Gateway for routing requests to microservices",
    version="1.0.0"
)

# CORS configuration for Next.js/Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
        os.getenv("NEXT_PUBLIC_VERCEL_URL", ""),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs from environment variables (Cloud Run URLs in production)
SERVICE_URLS = {
    "analysis": os.getenv("ANALYSIS_SERVICE_URL", "http://localhost:8001"),
    "scraping": os.getenv("SCRAPING_SERVICE_URL", "http://localhost:8002"),
    "validation": os.getenv("VALIDATION_SERVICE_URL", "http://localhost:8003"),
    "vector": os.getenv("VECTOR_SERVICE_URL", "http://localhost:8004"),
    "gis": os.getenv("GIS_SERVICE_URL", "http://localhost:8005"),
    "acris": os.getenv("ACRIS_SERVICE_URL", "http://localhost:8006"),
    "data": os.getenv("DATA_SERVICE_URL", "http://localhost:8007"),
    "google-drive": os.getenv("GOOGLE_DRIVE_SERVICE_URL", "http://localhost:8008"),
}

# HTTP client with timeout
http_client = httpx.AsyncClient(timeout=30.0)


@with_redundancy(
    func_key="forward_request",
    cache_key=None,  # Don't cache by default
    alternatives=None,
    fallback_func=None
)
async def forward_request(
    service_name: str,
    path: str,
    method: str = "GET",
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Forward request to microservice with redundancy"""
    # Validate inputs
    service_name = sanitize_input(service_name, "string")
    path = sanitize_input(path, "string")

    # Fallback 1: Check service availability
    service_url = SERVICE_URLS.get(service_name)
    if not service_url:
        # Fallback 2: Try alternative service URLs
        alt_urls = [
            os.getenv(f"{service_name.upper()}_SERVICE_URL_ALT1"),
            os.getenv(f"{service_name.upper()}_SERVICE_URL_ALT2"),
        ]
        for alt_url in alt_urls:
            if alt_url:
                service_url = alt_url
                break

        if not service_url:
            raise HTTPException(status_code=503, detail=f"Service {service_name} not available")

    url = f"{service_url}{path}"

    # Fallback 3: Validate and sanitize data
    if data:
        try:
            data = validate_json_payload(data)
            # Sanitize string values
            data = {k: sanitize_input(v, "string") if isinstance(v, str) else v for k, v in data.items()}
        except Exception as e:
            logger.warning(f"Data validation warning: {e}")

    # Fallback 4-6: Execute with retry, timeout, and circuit breaker (handled by decorator)
    try:
        if method == "GET":
            response = await http_client.get(url, params=params)
        elif method == "POST":
            response = await http_client.post(url, json=data, params=params)
        elif method == "PUT":
            response = await http_client.put(url, json=data, params=params)
        elif method == "DELETE":
            response = await http_client.delete(url, params=params)
        else:
            raise HTTPException(status_code=405, detail=f"Method {method} not allowed")

        response.raise_for_status()
        return response.json()

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error from {service_name}: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.RequestError as e:
        logger.error(f"Request error to {service_name}: {e}")
        raise HTTPException(status_code=503, detail=f"Service {service_name} unavailable")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    services_status = {}
    for service_name, service_url in SERVICE_URLS.items():
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{service_url}/health")
                services_status[service_name] = "healthy" if response.status_code == 200 else "unhealthy"
        except Exception as e:
            services_status[service_name] = f"error: {str(e)}"

    return {
        "status": "ok",
        "gateway": "healthy",
        "services": services_status
    }


# Analysis Service Routes
@app.post("/api/analysis/fraud")
async def analyze_fraud(request: Request):
    """Route to fraud analysis"""
    data = await request.json()
    return await forward_request("analysis", "/analyze/fraud", "POST", data)


@app.post("/api/analysis/nexus")
async def analyze_nexus(request: Request):
    """Route to nexus analysis"""
    data = await request.json()
    return await forward_request("analysis", "/analyze/nexus", "POST", data)


@app.post("/api/analysis/connections")
async def analyze_connections(request: Request):
    """Route to connection analysis"""
    data = await request.json()
    return await forward_request("analysis", "/analyze/connections", "POST", data)


@app.post("/api/analysis/violations")
async def analyze_violations(request: Request):
    """Route to violation analysis"""
    data = await request.json()
    return await forward_request("analysis", "/analyze/violations", "POST", data)


@app.post("/api/analysis/all")
async def analyze_all(request: Request):
    """Route to run all analyses"""
    data = await request.json()
    return await forward_request("analysis", "/analyze/all", "POST", data)


# Scraping Service Routes
@app.post("/api/scraping/airbnb")
async def scrape_airbnb(request: Request):
    """Route to Airbnb scraping"""
    data = await request.json()
    return await forward_request("scraping", "/scrape/airbnb", "POST", data)


@app.post("/api/scraping/vrbo")
async def scrape_vrbo(request: Request):
    """Route to VRBO scraping"""
    data = await request.json()
    return await forward_request("scraping", "/scrape/vrbo", "POST", data)


@app.post("/api/scraping/front")
async def scrape_front(request: Request):
    """Route to Front website scraping"""
    data = await request.json()
    return await forward_request("scraping", "/scrape/front", "POST", data)


@app.post("/api/scraping/acris")
async def scrape_acris(request: Request):
    """Route to ACRIS scraping"""
    data = await request.json()
    return await forward_request("scraping", "/scrape/acris", "POST", data)


# Validation Service Routes
@app.post("/api/validation/license")
async def validate_license(request: Request):
    """Route to license validation"""
    data = await request.json()
    return await forward_request("validation", "/validate/license", "POST", data)


@app.post("/api/validation/address")
async def validate_address(request: Request):
    """Route to address validation"""
    data = await request.json()
    return await forward_request("validation", "/validate/address", "POST", data)


@app.post("/api/validation/firm")
async def validate_firm(request: Request):
    """Route to firm validation"""
    data = await request.json()
    return await forward_request("validation", "/validate/firm", "POST", data)


@app.post("/api/validation/batch")
async def validate_batch(request: Request):
    """Route to batch validation"""
    data = await request.json()
    return await forward_request("validation", "/validate/batch", "POST", data)


# Vector Service Routes
@app.post("/api/vectors/embed")
async def create_embeddings(request: Request):
    """Route to create embeddings"""
    data = await request.json()
    return await forward_request("vector", "/vectors/embed", "POST", data)


@app.post("/api/vectors/search")
async def vector_search(request: Request):
    """Route to vector similarity search"""
    data = await request.json()
    return await forward_request("vector", "/vectors/search", "POST", data)


@app.post("/api/vectors/index")
async def index_documents(request: Request):
    """Route to index documents"""
    data = await request.json()
    return await forward_request("vector", "/vectors/index", "POST", data)


@app.get("/api/vectors/status")
async def vector_status():
    """Route to vector service status"""
    return await forward_request("vector", "/vectors/status", "GET")


# GIS Service Routes
@app.post("/api/gis/convert")
async def convert_gis(request: Request):
    """Route to GIS file conversion"""
    data = await request.json()
    return await forward_request("gis", "/gis/convert", "POST", data)


@app.get("/api/gis/info/{file_path:path}")
async def gis_info(file_path: str):
    """Route to get GIS file info"""
    return await forward_request("gis", f"/gis/info/{file_path}", "GET")


@app.post("/api/gis/batch")
async def batch_convert_gis(request: Request):
    """Route to batch GIS conversion"""
    data = await request.json()
    return await forward_request("gis", "/gis/batch", "POST", data)


# ACRIS Service Routes
@app.post("/api/acris/search/block-lot")
async def acris_block_lot(request: Request):
    """Route to ACRIS block/lot search"""
    data = await request.json()
    return await forward_request("acris", "/acris/search/block-lot", "POST", data)


@app.post("/api/acris/search/address")
async def acris_address(request: Request):
    """Route to ACRIS address search"""
    data = await request.json()
    return await forward_request("acris", "/acris/search/address", "POST", data)


@app.post("/api/acris/search/party")
async def acris_party(request: Request):
    """Route to ACRIS party name search"""
    data = await request.json()
    return await forward_request("acris", "/acris/search/party", "POST", data)


@app.post("/api/acris/search/document")
async def acris_document(request: Request):
    """Route to ACRIS document ID search"""
    data = await request.json()
    return await forward_request("acris", "/acris/search/document", "POST", data)


# Data Repository Service Routes
@app.get("/api/data/firms")
async def get_firms(params: Optional[Dict[str, Any]] = None):
    """Route to get firms"""
    return await forward_request("data", "/data/firms", "GET", params=params)


@app.get("/api/data/firms/{firm_id}")
async def get_firm(firm_id: str):
    """Route to get firm by ID"""
    return await forward_request("data", f"/data/firms/{firm_id}", "GET")


@app.post("/api/data/firms")
async def create_firm(request: Request):
    """Route to create firm"""
    data = await request.json()
    return await forward_request("data", "/data/firms", "POST", data)


@app.put("/api/data/firms/{firm_id}")
async def update_firm(firm_id: str, request: Request):
    """Route to update firm"""
    data = await request.json()
    return await forward_request("data", f"/data/firms/{firm_id}", "PUT", data)


@app.delete("/api/data/firms/{firm_id}")
async def delete_firm(firm_id: str):
    """Route to delete firm"""
    return await forward_request("data", f"/data/firms/{firm_id}", "DELETE")


# Google Drive Service Routes
@app.post("/api/drive/list")
async def list_drive_folder(request: Request):
    """Route to list Google Drive folder"""
    data = await request.json()
    return await forward_request("google-drive", "/drive/list", "POST", data)


@app.post("/api/drive/download")
async def download_drive_file(request: Request):
    """Route to download Google Drive file"""
    data = await request.json()
    return await forward_request("google-drive", "/drive/download", "POST", data)


@app.post("/api/drive/export")
async def export_drive_file(request: Request):
    """Route to export Google Drive file"""
    data = await request.json()
    return await forward_request("google-drive", "/drive/export", "POST", data)


@app.get("/api/drive/info/{file_id}")
async def get_drive_file_info(file_id: str):
    """Route to get Google Drive file info"""
    return await forward_request("google-drive", f"/drive/info/{file_id}", "GET")


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown"""
    await http_client.aclose()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
