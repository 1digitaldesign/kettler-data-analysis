# Architecture

Python-first architecture with unified modules and microservices.

## Layers

**Domain** (`scripts/architecture/models.py`)
- Entities: Firm, Connection, Violation, Evidence
- Value Objects: ViolationType, ConnectionType

**Repository** (`scripts/architecture/repository.py`)
- FirmRepository, FileRepository, VectorRepository
- Abstracted data access

**Services** (`scripts/architecture/services.py`)
- AnalysisService, ValidationService, ScrapingService
- Business logic abstraction

**Pipeline** (`scripts/architecture/pipeline.py`)
- Orchestrates services
- Error handling and retries

## Unified Modules

- `UnifiedAnalyzer` - Analysis operations
- `UnifiedSearcher` - Search operations
- `UnifiedValidator` - Validation operations
- `UnifiedReporter` - Report generation
- `UnifiedInvestigator` - Investigation operations

## Microservices

- API Gateway - Centralized routing
- Analysis Service - Distributed processing
- Google Drive Integration - File access

## ETL Pipeline

- Vector embeddings (Hugging Face)
- Data transformation
- Quality validation
