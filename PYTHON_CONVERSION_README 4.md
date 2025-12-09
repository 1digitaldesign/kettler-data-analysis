# Python Conversion Branch

This branch contains the Python conversion of the Kettler Data Analysis project, with a focus on ETL/ELT pipelines and embedded vector conversions.

## Overview

The codebase has been converted from R to Python, with special emphasis on:
- **ETL/ELT pipelines** with integrated vector embeddings
- **Data ingestion** with automatic vector conversion
- **Unified Python entry points** replacing R scripts

## Key Features

### Vector Embeddings Integration
- All data ingestion points automatically create vector embeddings
- Uses `sentence-transformers` with FAISS for efficient similarity search
- Embeddings stored in `data/vectors/` directory
- Supports CSV, JSON, PDF, Excel, and text data

### ETL/ELT Pipeline
- **Ingress**: Raw data ingestion with vector embeddings
- **Egress**: Cleaned data processing with vector embeddings
- **Source**: Source data processing
- **Research**: Research outputs processing
- **Evidence**: Evidence document processing (PDFs, Excel)
- **Scraped**: Scraped data processing

## Converted Components

### Core Pipeline
- ✅ `bin/run_pipeline.py` - Main pipeline runner (Python)
- ✅ `scripts/utils/paths.py` - Path utilities (Python)

### Extraction Scripts
- ✅ `scripts/extraction/extract_pdf_evidence.py` - PDF extraction with embeddings
- ✅ `scripts/extraction/extract_excel_evidence.py` - Excel extraction with embeddings
- ✅ `scripts/extraction/extract_all_evidence.py` - Master extraction script

### Analysis Scripts
- ✅ `bin/validate_data.py` - Data quality validation (Python)
- ✅ `bin/analyze_connections.py` - Connection analysis (Python)

### ETL Pipeline
- ✅ `scripts/etl/etl_pipeline.py` - Enhanced ETL pipeline
- ✅ `scripts/etl/vector_embeddings.py` - Vector embedding system

## Usage

### Running the Main Pipeline

```bash
# From project root
python bin/run_pipeline.py
```

### Running Individual Components

```bash
# Extract all evidence (PDFs + Excel) with vector embeddings
python scripts/extraction/extract_all_evidence.py

# Extract PDFs only
python scripts/extraction/extract_pdf_evidence.py

# Extract Excel files only
python scripts/extraction/extract_excel_evidence.py

# Run data validation
python bin/validate_data.py

# Run connection analysis
python bin/analyze_connections.py

# Run ETL pipeline
python scripts/etl/etl_pipeline.py
```

### Vector Embeddings

The vector embedding system automatically creates embeddings for:
- All CSV files (row-level embeddings)
- All JSON files (key-value pair embeddings)
- All PDF files (full-text embeddings)
- All Excel files (sheet-level embeddings)

Embeddings are stored in `data/vectors/` and can be searched using:

```python
from scripts.etl.vector_embeddings import VectorEmbeddingSystem

embedding_system = VectorEmbeddingSystem()
results = embedding_system.search_similar("your query text", top_k=10)
```

## Installation

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Key dependencies:
- `pandas` - Data manipulation
- `sentence-transformers` - Vector embeddings
- `faiss-cpu` - Vector similarity search
- `PyPDF2` / `pdfplumber` / `pypdf` - PDF processing
- `openpyxl` - Excel processing

## Migration Status

### Completed ✅
- Main pipeline runner
- PDF extraction with embeddings
- Excel extraction with embeddings
- Data validation
- Connection analysis
- ETL pipeline with vector embeddings
- Path utilities

### Pending ⏳
- Search scripts (web scraping) - Still in R
- Analysis scripts (fraud patterns, anomalies) - Still in R
- Report generation - Still in R

## Architecture

### Data Flow

```
Raw Data (CSV/JSON/PDF/Excel)
    ↓
Extraction Scripts (with vector embeddings)
    ↓
Cleaned Data
    ↓
ETL Pipeline (additional vector embeddings)
    ↓
Analysis Scripts
    ↓
Reports & Outputs
```

### Vector Embedding Flow

Every data ingestion point:
1. Reads data (CSV/JSON/PDF/Excel)
2. Extracts text/content
3. Creates vector embeddings
4. Stores in FAISS index
5. Saves metadata

## Benefits of Python Conversion

1. **Better ETL Integration**: Native Python ETL pipelines with vector embeddings
2. **Unified Language**: Single language (Python) instead of R + Python mix
3. **Better Libraries**: Access to rich Python ML/data science ecosystem
4. **Vector Search**: Built-in semantic search capabilities
5. **Performance**: Better performance for data processing tasks
6. **Maintainability**: Easier to maintain single-language codebase

## Notes

- R scripts are still available for backward compatibility
- Python scripts can call R scripts if needed (via subprocess)
- Vector embeddings are backward compatible with existing data
- All outputs maintain the same format as R versions

## Next Steps

1. Convert remaining search scripts to Python
2. Convert analysis scripts to Python
3. Convert report generation to Python
4. Add comprehensive tests
5. Update documentation
