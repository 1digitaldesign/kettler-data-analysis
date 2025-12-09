#!/usr/bin/env python3
"""
Data Repository Service
Handles data access and storage operations
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

from scripts.architecture import RepositoryFactory, Firm
from scripts.utils.paths import DATA_SOURCE_DIR

app = FastAPI(
    title="Data Repository Service",
    description="Microservice for data access and storage operations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize repository
firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.json"
if not firms_file.exists():
    firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.csv"

firm_repository = None

if firms_file.exists():
    firm_repository = RepositoryFactory.create_firm_repository(str(firms_file))


class FirmCreate(BaseModel):
    """Firm creation model"""
    firm_id: str
    firm_name: str
    address: str
    principal_broker: Optional[str] = None
    license_number: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class FirmUpdate(BaseModel):
    """Firm update model"""
    firm_name: Optional[str] = None
    address: Optional[str] = None
    principal_broker: Optional[str] = None
    license_number: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "data",
        "repository_initialized": firm_repository is not None
    }


@app.get("/data/firms")
async def get_firms(
    principal_broker: Optional[str] = None,
    address: Optional[str] = None,
    state: Optional[str] = None
):
    """Get firms with optional filters"""
    if not firm_repository:
        raise HTTPException(status_code=503, detail="Firm repository not initialized")

    try:
        filters = {}
        if principal_broker:
            return firm_repository.find_by_principal_broker(principal_broker)
        if address:
            return firm_repository.find_by_address(address)

        firms = firm_repository.find_all(filters if filters else None)
        return {
            "status": "success",
            "firms": [firm.to_dict() for firm in firms],
            "count": len(firms)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/data/firms/{firm_id}")
async def get_firm(firm_id: str):
    """Get firm by ID"""
    if not firm_repository:
        raise HTTPException(status_code=503, detail="Firm repository not initialized")

    try:
        firm = firm_repository.find_by_id(firm_id)
        if not firm:
            raise HTTPException(status_code=404, detail="Firm not found")

        return {
            "status": "success",
            "firm": firm.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/data/firms")
async def create_firm(request: FirmCreate):
    """Create firm"""
    if not firm_repository:
        raise HTTPException(status_code=503, detail="Firm repository not initialized")

    try:
        firm = Firm(
            firm_id=request.firm_id,
            firm_name=request.firm_name,
            address=request.address,
            principal_broker=request.principal_broker,
            license_number=request.license_number,
            state=request.state,
            phone=request.phone,
            email=request.email,
            metadata=request.metadata or {}
        )

        saved_firm = firm_repository.save(firm)

        return {
            "status": "success",
            "firm": saved_firm.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/data/firms/{firm_id}")
async def update_firm(firm_id: str, request: FirmUpdate):
    """Update firm"""
    if not firm_repository:
        raise HTTPException(status_code=503, detail="Firm repository not initialized")

    try:
        firm = firm_repository.find_by_id(firm_id)
        if not firm:
            raise HTTPException(status_code=404, detail="Firm not found")

        # Update fields
        if request.firm_name:
            firm.firm_name = request.firm_name
        if request.address:
            firm.address = request.address
        if request.principal_broker is not None:
            firm.principal_broker = request.principal_broker
        if request.license_number is not None:
            firm.license_number = request.license_number
        if request.state is not None:
            firm.state = request.state
        if request.phone is not None:
            firm.phone = request.phone
        if request.email is not None:
            firm.email = request.email
        if request.metadata:
            firm.metadata.update(request.metadata)

        updated_firm = firm_repository.save(firm)

        return {
            "status": "success",
            "firm": updated_firm.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/data/firms/{firm_id}")
async def delete_firm(firm_id: str):
    """Delete firm"""
    if not firm_repository:
        raise HTTPException(status_code=503, detail="Firm repository not initialized")

    try:
        deleted = firm_repository.delete(firm_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Firm not found")

        return {
            "status": "success",
            "message": f"Firm {firm_id} deleted"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8007"))
    uvicorn.run(app, host="0.0.0.0", port=port)
