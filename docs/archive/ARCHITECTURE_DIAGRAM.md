# Data Architecture Diagrams

**Version:** 1.0.0
**Last Updated:** 2025-12-08

## Overview

This document provides visual representations of the data architecture using ASCII diagrams and descriptions.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA ARCHITECTURE                        │
│                    Kettler Data Analysis Project                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                                  │
├─────────────────────────────────────────────────────────────────┤
│  • Virginia DPOR Website (Web Scraping)                        │
│  • State Regulatory Databases (APIs/Scraping)                   │
│  • Short-term Rental Platforms (Airbnb, VRBO)                  │
│  • Legal Documents (PDFs, Text Files)                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INGESTION LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  • Web Scrapers (Playwright/Selenium)                          │
│  • API Clients                                                  │
│  • File Processors                                             │
│  • Manual Entry Tools                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STORAGE LAYER (Data Zones)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ SOURCE ZONE  │  │   RAW ZONE   │  │ CLEANED ZONE │       │
│  │  (Bronze)    │  │   (Bronze)   │  │   (Silver)   │       │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤       │
│  │ • Immutable  │  │ • As-is      │  │ • Validated  │       │
│  │ • JSON/CSV   │  │ • CSV/JSON   │  │ • Parquet    │       │
│  │ • Complete   │  │ • Raw        │  │ • Standardized│      │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ ANALYSIS     │  │   SCRAPED    │  │   VECTORS    │       │
│  │   ZONE       │  │     ZONE     │  │     ZONE     │       │
│  │  (Gold)      │  │              │  │              │       │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤       │
│  │ • Aggregated │  │ • Platform   │  │ • Embeddings │       │
│  │ • Enriched   │  │   Data       │  │ • FAISS      │       │
│  │ • Optimized  │  │ • JSON       │  │ • Semantic   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PROCESSING LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  • ETL Pipelines                                                │
│  • Data Transformations                                         │
│  • Schema Validation                                            │
│  • Data Quality Checks                                          │
│  • Data Enrichment                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ANALYTICS LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  • Statistical Analysis                                         │
│  • Connection Analysis                                          │
│  • Pattern Detection                                            │
│  • Machine Learning Models                                      │
│  • Business Intelligence                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  • Reports                                                      │
│  • Dashboards                                                   │
│  • APIs                                                         │
│  • Visualizations                                               │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA FLOW PATTERNS                           │
└─────────────────────────────────────────────────────────────────┘

PATTERN 1: Source → Cleaned → Analysis
─────────────────────────────────────────
DPOR Website
    │
    ├─[Web Scraping]─→ Raw Zone (CSV)
    │                      │
    │                      ├─[Extract]─→ Source Zone (JSON)
    │                      │
    │                      └─[Transform & Validate]─→ Cleaned Zone (Parquet)
    │                                                 │
    │                                                 └─[Aggregate]─→ Analysis Zone
    │                                                                     │
    │                                                                     └─→ Reports

PATTERN 2: Scraped → Normalized → Analysis
────────────────────────────────────────────
Rental Platforms (Airbnb, VRBO)
    │
    ├─[Scraping]─→ Scraped Zone (JSON)
    │                 │
    │                 └─[Normalize]─→ Cleaned Zone
    │                                    │
    │                                    └─[Join with Firms]─→ Analysis Zone

PATTERN 3: Source → Vector → Semantic Search
──────────────────────────────────────────────
Source Data (JSON/Text)
    │
    ├─[Text Extraction]─→ Text Processing
    │                         │
    │                         └─[Generate Embeddings]─→ Vector Zone (FAISS)
    │                                                      │
    │                                                      └─[Query]─→ Semantic Search Results
```

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENTITY RELATIONSHIPS                         │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────┐
                    │   INDIVIDUAL │
                    │   (Person)   │
                    └──────┬───────┘
                           │
                           │ serves_as (1:N)
                           │
                    ┌──────▼───────┐
                    │     FIRM     │
                    │  (Business)  │
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        │ has_license (1:1)│                  │ located_at (N:1)
        │                  │                  │
┌───────▼───────┐          │          ┌───────▼───────┐
│    LICENSE    │          │          │   ADDRESS    │
│  (Regulatory) │          │          │  (Location)  │
└───────────────┘          │          └──────────────┘
                           │
                           │ connected_to (N:M)
                           │
                    ┌──────▼───────┐
                    │  CONNECTION   │
                    │ (Relationship)│
                    └──────────────┘

                    ┌──────────────┐
                    │    LISTING    │
                    │   (Property)  │
                    └──────┬────────┘
                           │
                           │ listed_on (N:1)
                           │
                    ┌──────▼───────┐
                    │   PLATFORM    │
                    │  (Airbnb/VRBO)│
                    └───────────────┘
```

## Data Zone Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA ZONES DETAIL                            │
└─────────────────────────────────────────────────────────────────┘

SOURCE ZONE (Bronze - Immutable)
├── skidmore_all_firms_complete.json      [38 firms, complete]
├── skidmore_individual_licenses.json      [40+ licenses]
└── skidmore_firms_database.csv           [CSV export]

RAW ZONE (Bronze - As-Is)
├── sample_dpor_results.csv               [Raw scraped data]
└── [Other raw ingestion files]

CLEANED ZONE (Silver - Validated)
├── dpor_all_cleaned.csv                  [Validated, standardized]
└── [Parquet files for analytics]

ANALYSIS ZONE (Gold - Aggregated)
├── dpor_validated.csv                    [Quality flags added]
├── dpor_skidmore_connections.csv          [Connection analysis]
├── data_quality_report.json              [Quality metrics]
└── analysis_summary.json                 [Summary statistics]

SCRAPED ZONE (External Data)
├── airbnb_listings_john_carlyle.json
├── vrbo_listings_john_carlyle.json
├── front_website_listings.json
└── additional_str_listings.json

VECTOR ZONE (Embeddings)
├── vector_index.faiss                    [Vector search index]
├── etl_results.json                      [ETL metadata]
├── metadata.json                         [Vector metadata]
└── processed_files.json                  [Processing log]
```

## Processing Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROCESSING PIPELINE                           │
└─────────────────────────────────────────────────────────────────┘

1. INGESTION
   ┌─────────────┐
   │ Data Source │
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │   Extract   │
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │  Raw Zone   │
   └─────────────┘

2. VALIDATION
   ┌─────────────┐
   │  Raw Zone   │
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │  Validate   │──→ Schema Validation
   │   Schema    │──→ Business Rules
   └──────┬──────┘──→ Data Quality Checks
          │
          ▼
   ┌─────────────┐
   │ Cleaned Zone│
   └─────────────┘

3. TRANSFORMATION
   ┌─────────────┐
   │ Cleaned Zone│
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │ Transform   │──→ Standardize Formats
   │             │──→ Enrich Data
   │             │──→ Calculate Metrics
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │ Analysis    │
   │    Zone     │
   └─────────────┘

4. ANALYTICS
   ┌─────────────┐
   │ Analysis    │
   │    Zone     │
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │  Analyze    │──→ Statistical Analysis
   │             │──→ Pattern Detection
   │             │──→ Connection Analysis
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │   Reports   │
   └─────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                             │
└─────────────────────────────────────────────────────────────────┘

STORAGE
├── File System (Local/Network)
├── Formats: Parquet, JSON, CSV
└── Vector DB: FAISS

PROCESSING
├── Python 3.x
├── Pandas (Data Manipulation)
├── SQL (Query Interface)
└── Custom Scripts (ETL)

VALIDATION
├── JSON Schema
├── Great Expectations
└── Custom Validators

DOCUMENTATION
├── Markdown (Human-readable)
├── JSON Schema (Machine-readable)
└── SQL DDL (Database schemas)

TOOLS
├── Git (Version Control)
├── Python Scripts (Automation)
└── Validation Scripts (Quality)
```

## Access Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA ACCESS PATTERNS                         │
└─────────────────────────────────────────────────────────────────┘

READ PATTERNS
├── Sequential Scan (Full Table)
│   └─→ Use: Parquet with columnar storage
│
├── Index Lookup (Primary Key)
│   └─→ Use: Indexed columns, hash tables
│
├── Filtered Scan (WHERE clause)
│   └─→ Use: Partitioning, predicate pushdown
│
└── Aggregation (GROUP BY)
    └─→ Use: Pre-aggregated views, materialized tables

WRITE PATTERNS
├── Batch Insert (ETL)
│   └─→ Use: Bulk load, append mode
│
├── Incremental Update
│   └─→ Use: Merge operations, upsert
│
└── Streaming (Real-time)
    └─→ Use: Append-only, event log
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    ACCESS CONTROL                                │
├─────────────────────────────────────────────────────────────────┤
│  • Role-Based Access Control (RBAC)                            │
│  • Data Classification (Public, Internal, Confidential)        │
│  • Permission Matrix                                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    DATA PROTECTION                               │
├─────────────────────────────────────────────────────────────────┤
│  • Encryption at Rest                                           │
│  • Encryption in Transit                                        │
│  • Data Masking (PII)                                           │
│  • Audit Logging                                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    COMPLIANCE                                    │
├─────────────────────────────────────────────────────────────────┤
│  • Data Retention Policies                                      │
│  • Access Audit Trails                                          │
│  • Data Lineage Tracking                                        │
│  • Regulatory Compliance                                        │
└─────────────────────────────────────────────────────────────────┘
```

## References

- [Data Architecture](./DATA_ARCHITECTURE.md) - Detailed architecture documentation
- [Data Ontology](./DATA_ONTOLOGY.md) - Entity definitions and relationships
- [Schema Documentation](./SCHEMA.md) - Database schema details
