# Data Architecture

**Version:** 1.0.0
**Last Updated:** 2025-12-08
**Status:** Active

## Executive Summary

This document describes the data architecture for the Kettler Data Analysis project. The architecture follows modern data lakehouse principles, supporting structured, semi-structured, and unstructured data with a focus on scalability, governance, and analytical performance.

## Architecture Principles

### 1. Unified Data Platform
- **Single Source of Truth**: Centralized data storage with clear lineage
- **Multi-Format Support**: Structured (CSV, Parquet), Semi-structured (JSON), Unstructured (Text, PDFs)
- **Schema-on-Read**: Flexible schema application during query time
- **Schema-on-Write**: Enforced schemas for critical data

### 2. Data Quality and Governance
- **Schema Validation**: Automated validation against defined schemas
- **Data Lineage**: Track data from source to consumption
- **Access Control**: Role-based access to sensitive data
- **Audit Trail**: Complete audit logging for compliance

### 3. Scalability and Performance
- **Partitioning**: Data partitioned by date, state, or entity type
- **Indexing**: Strategic indexes for common query patterns
- **Caching**: Frequently accessed data cached for performance
- **Compression**: Efficient storage formats (Parquet, GZIP)

### 4. Open Standards
- **Open Formats**: Parquet, JSON, CSV for vendor independence
- **Standard APIs**: RESTful APIs for data access
- **SQL Interface**: Standard SQL for querying
- **Version Control**: Git-based schema versioning

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  Reports | Dashboards | APIs | Applications                 │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                    ANALYTICS LAYER                           │
│  Analysis | ML Models | Business Intelligence              │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                    PROCESSING LAYER                         │
│  ETL | Transformations | Validations | Enrichments         │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                    STORAGE LAYER                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Source  │  │   Raw    │  │  Cleaned │  │ Analysis │   │
│  │  (JSON)  │  │  (CSV)   │  │ (Parquet)│  │  (JSON)  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │ Scraped  │  │  Vectors  │  │ Metadata │                 │
│  │  (JSON)  │  │  (FAISS)  │  │  (JSON)  │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                    INGESTION LAYER                          │
│  Web Scraping | APIs | Manual Entry | File Upload         │
└─────────────────────────────────────────────────────────────┘
```

## Data Zones

### 1. Source Zone (Bronze Layer)
**Purpose**: Original, unmodified source data

**Characteristics**:
- **Format**: JSON, CSV
- **Schema**: Flexible, may vary
- **Retention**: Permanent (immutable)
- **Access**: Read-only
- **Examples**: `source/skidmore_all_firms_complete.json`

**Best Practices**:
- Never modify source data
- Maintain data provenance
- Version control for schemas
- Document data sources

### 2. Raw Zone (Bronze Layer)
**Purpose**: Initial ingestion, minimal processing

**Characteristics**:
- **Format**: CSV, JSON, Text
- **Schema**: As-is from source
- **Retention**: Long-term
- **Access**: Read-only
- **Examples**: `raw/sample_dpor_results.csv`

**Best Practices**:
- Preserve original format
- Add metadata tags
- Track ingestion timestamps
- Maintain data lineage

### 3. Cleaned Zone (Silver Layer)
**Purpose**: Cleaned, validated, standardized data

**Characteristics**:
- **Format**: Parquet, CSV
- **Schema**: Enforced, validated
- **Retention**: Long-term
- **Access**: Read/Write (ETL)
- **Examples**: `cleaned/dpor_all_cleaned.csv`

**Best Practices**:
- Enforce schema validation
- Standardize formats
- Remove duplicates
- Validate data quality
- Create indexes

### 4. Analysis Zone (Gold Layer)
**Purpose**: Aggregated, enriched, analysis-ready data

**Characteristics**:
- **Format**: Parquet, JSON
- **Schema**: Optimized for queries
- **Retention**: Long-term
- **Access**: Read-optimized
- **Examples**: `analysis/dpor_validated.csv`

**Best Practices**:
- Pre-aggregate common queries
- Optimize for read performance
- Create materialized views
- Partition by query patterns

### 5. Scraped Zone
**Purpose**: External data from web scraping

**Characteristics**:
- **Format**: JSON
- **Schema**: Platform-specific
- **Retention**: Configurable
- **Access**: Read/Write
- **Examples**: `scraped/airbnb_listings_john_carlyle.json`

**Best Practices**:
- Normalize platform formats
- Add scraping metadata
- Handle rate limiting
- Validate scraped data

### 6. Vector Zone
**Purpose**: Vector embeddings for semantic search

**Characteristics**:
- **Format**: FAISS, NumPy arrays
- **Schema**: Vector dimensions
- **Retention**: Long-term
- **Access**: Read-optimized
- **Examples**: `vectors/vector_index.faiss`

**Best Practices**:
- Use efficient vector formats
- Index for similarity search
- Version embeddings
- Document embedding models

## Data Flow Patterns

### Pattern 1: Source → Cleaned → Analysis
```
Source (JSON)
    ↓ [Extract]
Raw (CSV)
    ↓ [Transform & Validate]
Cleaned (Parquet)
    ↓ [Aggregate & Enrich]
Analysis (Parquet/JSON)
    ↓ [Consume]
Reports/Dashboards
```

### Pattern 2: Scraped → Normalized → Analysis
```
Web Scraping
    ↓ [Collect]
Scraped (JSON)
    ↓ [Normalize]
Cleaned (Parquet)
    ↓ [Join with Source]
Analysis (Parquet)
```

### Pattern 3: Source → Vector → Semantic Search
```
Source (JSON/Text)
    ↓ [Extract Text]
Text Processing
    ↓ [Generate Embeddings]
Vectors (FAISS)
    ↓ [Query]
Semantic Search Results
```

## Data Types and Formats

### Structured Data
**Definition**: Data with fixed schema and tabular structure

**Formats**:
- **CSV**: Human-readable, good for small datasets
- **Parquet**: Columnar, compressed, optimal for analytics
- **SQL Tables**: Relational database format

**Use Cases**:
- Firm licenses (tabular)
- Individual licenses (tabular)
- Analysis results (tabular)

**Best Practices**:
- Use Parquet for large datasets
- Enforce schema validation
- Create indexes on key columns
- Partition by date/state

### Semi-Structured Data
**Definition**: Data with flexible schema, nested structures

**Formats**:
- **JSON**: Flexible, human-readable, good for APIs
- **JSONL**: JSON Lines, one object per line
- **XML**: Hierarchical, verbose

**Use Cases**:
- Firm data with nested metadata
- Scraped listings with varying fields
- Configuration files
- API responses

**Best Practices**:
- Use JSON Schema for validation
- Flatten nested structures for analytics
- Preserve original JSON for flexibility
- Use JSONL for streaming

### Unstructured Data
**Definition**: Data without predefined structure

**Formats**:
- **Text**: Plain text documents
- **PDF**: Portable Document Format
- **HTML**: Web pages
- **Images**: Photos, screenshots

**Use Cases**:
- Legal documents
- Web pages
- Evidence files
- Reports

**Best Practices**:
- Extract text for searchability
- Generate embeddings for semantic search
- Store metadata separately
- Use OCR for scanned documents

## Storage Strategy

### File Organization
```
data/
├── source/          # Source of truth (immutable)
├── raw/            # Initial ingestion
├── cleaned/         # Validated and standardized
├── analysis/       # Analysis-ready aggregates
├── scraped/        # External scraped data
└── vectors/        # Vector embeddings
```

### Naming Conventions
- **Files**: `{entity}_{type}_{date}.{ext}`
  - Example: `skidmore_all_firms_complete.json`
- **Partitions**: `{dimension}={value}/`
  - Example: `state=VA/`, `year=2025/`
- **Versions**: `{name}_v{version}.{ext}`
  - Example: `schema_v1.0.0.json`

### Partitioning Strategy
- **By Date**: `year=2025/month=12/day=08/`
- **By State**: `state=VA/`, `state=TX/`
- **By Entity Type**: `entity=firm/`, `entity=individual/`
- **By Status**: `status=active/`, `status=expired/`

## Data Quality Framework

### Quality Dimensions

1. **Completeness**
   - Required fields present
   - No missing critical data
   - Coverage metrics

2. **Accuracy**
   - Data matches source
   - Correct values
   - Verified against authoritative sources

3. **Consistency**
   - Uniform formats
   - Consistent naming
   - No contradictions

4. **Validity**
   - Conforms to schema
   - Meets business rules
   - Passes validation checks

5. **Timeliness**
   - Up-to-date data
   - Freshness metrics
   - Staleness detection

6. **Uniqueness**
   - No duplicates
   - Unique identifiers
   - Deduplication rules

### Quality Checks

```python
# Example quality check
def validate_firm_data(firm):
    checks = {
        'completeness': all_required_fields_present(firm),
        'validity': schema_validation(firm),
        'uniqueness': license_number_unique(firm['firm_license']),
        'accuracy': address_valid(firm['address']),
        'consistency': dates_logical(firm)
    }
    return all(checks.values())
```

## Metadata Management

### Metadata Types

1. **Technical Metadata**
   - Schema definitions
   - Data types
   - File formats
   - Storage locations

2. **Business Metadata**
   - Business definitions
   - Data owners
   - Business rules
   - Data lineage

3. **Operational Metadata**
   - Data quality metrics
   - Processing statistics
   - Error logs
   - Performance metrics

### Metadata Storage
- **Schema**: `schema.json`, `schema.sql`
- **Documentation**: `SCHEMA.md`, `DATA_ONTOLOGY.md`
- **Lineage**: Tracked in processing logs
- **Quality**: `data_quality_report.json`

## Security and Access Control

### Data Classification

1. **Public**: No restrictions
   - Schema definitions
   - Documentation

2. **Internal**: Team access
   - Analysis results
   - Processed data

3. **Confidential**: Restricted access
   - Source data
   - Personal information
   - Investigation data

### Access Control
- **Role-Based**: Admin, Analyst, Viewer
- **Data Masking**: PII redaction
- **Audit Logging**: All access logged
- **Encryption**: At rest and in transit

## Scalability Considerations

### Horizontal Scaling
- **Partitioning**: Distribute data across partitions
- **Sharding**: Split large tables
- **Distributed Processing**: Use Spark/Dask

### Vertical Scaling
- **Indexing**: Strategic indexes
- **Caching**: Frequently accessed data
- **Compression**: Reduce storage

### Performance Optimization
- **Columnar Formats**: Parquet for analytics
- **Predicate Pushdown**: Filter early
- **Projection**: Select only needed columns
- **Materialized Views**: Pre-compute aggregates

## Technology Stack

### Storage
- **File System**: Local/Network storage
- **Formats**: Parquet, JSON, CSV
- **Vector DB**: FAISS for embeddings

### Processing
- **Python**: Data processing scripts
- **Pandas**: Data manipulation
- **SQL**: Query interface
- **Spark**: Distributed processing (future)

### Validation
- **JSON Schema**: Schema validation
- **Great Expectations**: Data quality
- **Custom Validators**: Business rules

### Documentation
- **Markdown**: Documentation
- **JSON Schema**: Machine-readable schemas
- **SQL DDL**: Database schemas

## Best Practices Summary

### Data Management
✅ **Single Source of Truth**: One authoritative source per entity
✅ **Schema Enforcement**: Validate all data
✅ **Version Control**: Track schema changes
✅ **Documentation**: Keep documentation current
✅ **Lineage Tracking**: Know data origins

### Performance
✅ **Partitioning**: Partition by query patterns
✅ **Indexing**: Index frequently queried columns
✅ **Compression**: Use efficient formats
✅ **Caching**: Cache hot data
✅ **Projection**: Select only needed columns

### Quality
✅ **Validation**: Validate at ingestion
✅ **Monitoring**: Track quality metrics
✅ **Automation**: Automate quality checks
✅ **Alerting**: Alert on quality issues
✅ **Remediation**: Fix quality issues promptly

### Governance
✅ **Access Control**: Enforce access policies
✅ **Audit Logging**: Log all access
✅ **Data Classification**: Classify data sensitivity
✅ **Retention Policies**: Define retention rules
✅ **Compliance**: Meet regulatory requirements

## Migration and Evolution

### Schema Evolution
- **Backward Compatibility**: Support old schemas
- **Versioning**: Version all schemas
- **Migration Scripts**: Automated migrations
- **Testing**: Test schema changes

### Data Migration
- **Incremental**: Migrate in batches
- **Validation**: Validate migrated data
- **Rollback**: Ability to rollback
- **Monitoring**: Monitor migration progress

## References

- [Data Ontology](./DATA_ONTOLOGY.md)
- [Schema Definition](./schema.json)
- [Schema Documentation](./SCHEMA.md)
- [Quick Reference](./QUICK_REFERENCE.md)

## Maintenance

**Owner**: Data Architecture Team
**Review Cycle**: Quarterly
**Last Review**: 2025-12-08
**Next Review**: 2026-03-08
