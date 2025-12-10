#!/usr/bin/env python3
"""
GIS Service
Handles GIS file conversion operations
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
    from scripts.gis.gis_converter import GISConverter
    GIS_CONVERTER_AVAILABLE = True
except ImportError:
    GIS_CONVERTER_AVAILABLE = False
    GISConverter = None

app = FastAPI(
    title="GIS Service",
    description="Microservice for GIS file conversion operations",
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
gis_converter = None

if GIS_CONVERTER_AVAILABLE:
    try:
        gis_converter = GISConverter()
    except Exception as e:
        print(f"Warning: Could not initialize GIS converter: {e}")


class ConvertRequest(BaseModel):
    """Convert request model"""
    input_file: str
    output_format: str = "geojson"
    output_file: Optional[str] = None
    target_srs: Optional[str] = None


class BatchConvertRequest(BaseModel):
    """Batch convert request model"""
    input_files: List[str]
    output_format: str = "geojson"
    output_dir: Optional[str] = None
    target_srs: Optional[str] = None


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "gis",
        "gis_converter_available": GIS_CONVERTER_AVAILABLE,
        "gis_converter_initialized": gis_converter is not None
    }


@app.post("/gis/convert")
async def convert_gis(request: ConvertRequest):
    """Convert GIS file"""
    if not gis_converter:
        raise HTTPException(status_code=503, detail="GIS converter not available")

    try:
        input_path = Path(request.input_file)
        output_path = Path(request.output_file) if request.output_file else None

        result = gis_converter.convert_file(
            input_path,
            output_path,
            request.output_format,
            request.target_srs
        )

        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/gis/info/{file_path:path}")
async def get_gis_info(file_path: str):
    """Get GIS file info"""
    if not gis_converter:
        raise HTTPException(status_code=503, detail="GIS converter not available")

    try:
        file_path_obj = Path(file_path)
        info = gis_converter.get_file_info(file_path_obj)

        return {
            "status": "success",
            "info": info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/gis/batch")
async def batch_convert_gis(request: BatchConvertRequest):
    """Batch convert GIS files"""
    if not gis_converter:
        raise HTTPException(status_code=503, detail="GIS converter not available")

    try:
        input_files = [Path(f) for f in request.input_files]
        output_dir = Path(request.output_dir) if request.output_dir else None

        results = gis_converter.batch_convert(
            input_files,
            request.output_format,
            output_dir,
            request.target_srs
        )

        return {
            "status": "success",
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8005"))
    uvicorn.run(app, host="0.0.0.0", port=port)
