#!/usr/bin/env python3
"""
FastAPI Server for Web Interface
Provides REST API for the React frontend
"""

import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json

# Add scripts to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(PROJECT_ROOT / "bin"))

try:
from scripts.core.unified_analysis import UnifiedAnalyzer
from scripts.core.unified_search import UnifiedSearcher
from scripts.core.unified_validation import UnifiedValidator
from scripts.core.unified_reporting import UnifiedReporter
from scripts.core.unified_investigation import UnifiedInvestigator
from scripts.core.unified_scraping import UnifiedScraper
except ImportError as e:
    print(f"Warning: Could not import unified modules: {e}")
    UnifiedAnalyzer = UnifiedSearcher = UnifiedValidator = None
    UnifiedReporter = UnifiedInvestigator = UnifiedScraper = None
from scripts.etl.vector_embeddings import VectorEmbeddingSystem
from scripts.utils.paths import (
    DATA_SOURCE_DIR, DATA_ANALYSIS_DIR, RESEARCH_DIR,
    OUTPUTS_DIR, DATA_VECTORS_DIR
)

app = FastAPI(title="Kettler Data Analysis API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class SearchRequest(BaseModel):
    query: str
    top_k: int = 10

class DPORSearchRequest(BaseModel):
    query: str
    state: str = "all"

class ScrapingRequest(BaseModel):
    platform: str
    targets: List[str]

# Initialize analyzers (lazy loading)
_analyzer = None
_searcher = None
_validator = None
_reporter = None
_investigator = None
_scraper = None
_vector_system = None

def get_analyzer():
    global _analyzer
    if UnifiedAnalyzer is None:
        raise HTTPException(status_code=503, detail="UnifiedAnalyzer not available")
    if _analyzer is None:
        _analyzer = UnifiedAnalyzer()
        _analyzer.load_all_data()
    return _analyzer

def get_searcher():
    global _searcher
    if UnifiedSearcher is None:
        raise HTTPException(status_code=503, detail="UnifiedSearcher not available")
    if _searcher is None:
        _searcher = UnifiedSearcher()
    return _searcher

def get_validator():
    global _validator
    if _validator is None:
        _validator = UnifiedValidator()
    return _validator

def get_reporter():
    global _reporter
    if _reporter is None:
        _reporter = UnifiedReporter()
    return _reporter

def get_scraper():
    global _scraper
    if UnifiedScraper is None:
        raise HTTPException(status_code=503, detail="UnifiedScraper not available")
    if _scraper is None:
        _scraper = UnifiedScraper()
    return _scraper

def get_vector_system():
    global _vector_system
    if _vector_system is None:
        try:
            _vector_system = VectorEmbeddingSystem()
        except Exception as e:
            print(f"Warning: Could not initialize vector system: {e}")
            _vector_system = None
    return _vector_system

@app.get("/")
def root():
    return {"message": "Kettler Data Analysis API", "version": "1.0.0"}

@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        analyzer = get_analyzer()
        firms = analyzer.data.get('firms', [])

        # Load connections if available
        connections_file = DATA_ANALYSIS_DIR / "dpor_skidmore_connections.csv"
        connections_count = 0
        if connections_file.exists():
            import pandas as pd
            df = pd.read_csv(connections_file)
            connections_count = len(df)

        # Load violations
        violations_file = RESEARCH_DIR / "violations" / "all_violations_compiled.json"
        violations_count = 0
        if violations_file.exists():
            with open(violations_file, 'r') as f:
                violations_data = json.load(f)
                violations_count = sum(len(v) if isinstance(v, list) else 0 for v in violations_data.values())

        # Load fraud indicators
        fraud_file = RESEARCH_DIR / "fraud_indicators.json"
        fraud_count = 0
        if fraud_file.exists():
            with open(fraud_file, 'r') as f:
                fraud_data = json.load(f)
                fraud_count = sum(len(v) if isinstance(v, list) else 0 for v in fraud_data.values())

        return {
            "totalFirms": len(firms) if isinstance(firms, list) else (firms.shape[0] if hasattr(firms, 'shape') else 0),
            "totalConnections": connections_count,
            "violationsFound": violations_count,
            "fraudIndicators": fraud_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search/vector")
def vector_search(request: SearchRequest):
    """Vector similarity search"""
    try:
        vector_system = get_vector_system()
        if vector_system is None:
            return {"results": [], "message": "Vector system not available"}

        results = vector_system.search_similar(request.query, top_k=request.top_k)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search/dpor")
def dpor_search(request: DPORSearchRequest):
    """DPOR database search"""
    try:
        searcher = get_searcher()
        results = searcher.search_dpor(request.state, [request.query])
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search/regulatory")
def regulatory_search():
    """Get regulatory agencies"""
    try:
        searcher = get_searcher()
        agencies = searcher.search_regulatory_agencies()
        return {"agencies": agencies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analysis/{analysis_type}")
def run_analysis(analysis_type: str):
    """Run specific analysis"""
    try:
        analyzer = get_analyzer()

        if analysis_type == "fraud":
            results = analyzer.analyze_fraud_patterns()
        elif analysis_type == "nexus":
            results = analyzer.analyze_nexus_patterns()
        elif analysis_type == "timeline":
            results = analyzer.analyze_timeline()
        elif analysis_type == "anomalies":
            results = analyzer.consolidate_anomalies()
        elif analysis_type == "violations":
            reporter = get_reporter()
            results = reporter.compile_all_violations()
        else:
            raise HTTPException(status_code=400, detail=f"Unknown analysis type: {analysis_type}")

        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/visualization/data")
def get_visualization_data():
    """Get data for visualizations"""
    try:
        # Load connection data
        connections_file = DATA_ANALYSIS_DIR / "dpor_skidmore_connections.csv"
        connection_data = []
        if connections_file.exists():
            import pandas as pd
            df = pd.read_csv(connections_file)
            if 'connection_type' in df.columns:
                connection_counts = df['connection_type'].value_counts()
                connection_data = [{"name": k, "value": int(v)} for k, v in connection_counts.items()]

        # Load violation data
        violations_file = RESEARCH_DIR / "violations" / "all_violations_compiled.json"
        violation_data = []
        if violations_file.exists():
            with open(violations_file, 'r') as f:
                violations = json.load(f)
                violation_data = [
                    {"name": k.replace('_', ' ').title(), "value": len(v) if isinstance(v, list) else 0}
                    for k, v in violations.items()
                ]

        return {
            "connections": connection_data,
            "violations": violation_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ACRISSearchRequest(BaseModel):
    search_type: str  # block_lot, address, party_name, document_id
    borough: Optional[str] = None
    block: Optional[str] = None
    lot: Optional[str] = None
    address: Optional[str] = None
    party_name: Optional[str] = None
    document_id: Optional[str] = None
    document_type: Optional[str] = None

@app.post("/api/scraping/scrape")
def run_scraping(request: ScrapingRequest):
    """Run web scraping"""
    try:
        scraper = get_scraper()

        if request.platform == "airbnb":
            results = scraper.scrape_airbnb(request.targets)
        elif request.platform == "vrbo":
            results = scraper.scrape_vrbo(request.targets)
        elif request.platform == "front":
            results = scraper.scrape_front_websites(request.targets)
        elif request.platform == "multi":
            results = scraper.scrape_multi_platform(request.targets)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown platform: {request.platform}")

        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scraping/acris")
def run_acris_search(request: ACRISSearchRequest):
    """Search NYC ACRIS property records"""
    try:
        scraper = get_scraper()
        
        kwargs = {}
        if request.borough:
            kwargs['borough'] = request.borough
        if request.block:
            kwargs['block'] = request.block
        if request.lot:
            kwargs['lot'] = request.lot
        if request.address:
            kwargs['address'] = request.address
        if request.party_name:
            kwargs['party_name'] = request.party_name
        if request.document_id:
            kwargs['document_id'] = request.document_id
        if request.document_type:
            kwargs['document_type'] = request.document_type
        
        results = scraper.scrape_acris(request.search_type, **kwargs)
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/scraping/platforms")
def get_scraping_platforms():
    """Get available scraping platforms"""
    return {
        "platforms": [
            {"id": "airbnb", "name": "Airbnb", "description": "Scrape Airbnb listings"},
            {"id": "vrbo", "name": "VRBO", "description": "Scrape VRBO listings"},
            {"id": "front", "name": "Front Websites", "description": "Scrape company websites"},
            {"id": "multi", "name": "Multi-Platform", "description": "Scrape across multiple platforms"},
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
