# Vector Embedding and ETL Pipeline

This directory contains the vector embedding system and ETL/ELT pipeline for processing all data types in the project.

## Overview

The system automatically:
1. **Extracts** data from all sources (CSV, JSON, PDF, Excel)
2. **Transforms** data into vector embeddings using sentence transformers
3. **Loads** embeddings into a FAISS vector store for fast similarity search

## Components

### Python Components

- **`vector_embeddings.py`**: Core vector embedding system
  - Creates embeddings using sentence-transformers
  - Stores embeddings in FAISS index
  - Provides similarity search functionality

- **`etl_pipeline.py`**: ETL pipeline orchestrator
  - Processes all data types (CSV, JSON, PDF, Excel)
  - Handles ingress (raw), egress (cleaned), and all data sources
  - Tracks processed files to avoid reprocessing

### R Components

- **`vector_query.R`**: R interface for querying vector embeddings
- **`auto_etl_hook.R`**: Automatic ETL trigger when data is accessed
- **`chat_data_hook.R`**: Hook for chat sessions to auto-run ETL
- **`integrate_with_loaders.R`**: Integration with existing data loaders

## Usage

### Running Full ETL Pipeline

```bash
# Python
python3 scripts/etl/etl_pipeline.py

# R
Rscript scripts/etl/vector_query.R etl
```

### Processing Specific Files/Directories

```bash
# Process a single file
python3 scripts/etl/etl_pipeline.py --file data/raw/sample.csv

# Process a directory
python3 scripts/etl/etl_pipeline.py --dir data/research

# Force reprocessing
python3 scripts/etl/etl_pipeline.py --force
```

### Querying Similar Content

```r
# In R
source("scripts/etl/vector_query.R")
results <- query_similar("Caitlin Skidmore", top_k = 10)
print(results)
```

### Automatic ETL in Chat Sessions

Add this to the beginning of any analysis script:

```r
source("scripts/etl/chat_data_hook.R")
# Now all data loading will automatically trigger ETL
```

## Data Flow

1. **Ingress**: Raw data files → Vector embeddings
2. **Egress**: Cleaned data files → Vector embeddings
3. **Source**: Source data files → Vector embeddings
4. **Research**: Research JSON files → Vector embeddings
5. **Evidence**: PDF evidence files → Vector embeddings
6. **Scraped**: Scraped data files → Vector embeddings

## Vector Store Location

All embeddings are stored in:
- `data/vectors/vector_index.faiss` - FAISS vector index
- `data/vectors/metadata.json` - Metadata for all embeddings
- `data/vectors/processed_files.json` - List of processed files
- `data/vectors/etl_results.json` - ETL pipeline results

## Dependencies

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Key dependencies:
- `sentence-transformers` - For creating embeddings
- `faiss-cpu` - For vector similarity search
- `pandas` - For data processing
- `numpy` - For numerical operations

R dependencies:
- `reticulate` - For Python integration
- `jsonlite` - For JSON processing

## Integration with Existing Code

The ETL pipeline is automatically integrated into:
- `run_full_pipeline.R` - Runs ETL as Step 5
- Data loading functions - Auto-triggers ETL when data is accessed
- Chat sessions - Auto-runs ETL when data is loaded

## Performance

- Embeddings are created incrementally (only new/changed files)
- Vector store is persisted to disk
- Similarity search is fast (FAISS index)
- Model: `all-MiniLM-L6-v2` (384 dimensions, fast and efficient)

## Statistics

Get vector store statistics:
```r
source("scripts/etl/vector_query.R")
stats <- get_vector_stats()
print(stats)
```
