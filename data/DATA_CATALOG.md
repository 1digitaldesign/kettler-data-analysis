# Data Catalog

![Catalog](https://img.shields.io/badge/catalog-complete-brightgreen)
![Assets](https://img.shields.io/badge/data%20assets-15%2B-blue)
![Governance](https://img.shields.io/badge/governance-active-orange)

Comprehensive data catalog providing discoverability, documentation, and governance for all data assets.

## About This Catalog

This data catalog follows industry best practices for data asset management, providing:

- **Data Discovery**: Find data assets quickly by category, type, or purpose
- **Metadata Management**: Comprehensive metadata for each data asset
- **Data Lineage**: Track data from source to consumption
- **Data Quality**: Quality metrics and validation status
- **Access & Governance**: Ownership, access controls, and compliance information

> 📘 This catalog complements:
> - [Data Dictionary](./DATA_DICTIONARY.md) - Technical field definitions
> - [Data Ontology](./ONTOLOGY.md) - Conceptual model and relationships
> - [Data Ancestry](./ANCESTRY.md) - Data lineage and transformations
> - [Schema](./schema.json) - JSON Schema definitions

---

## Catalog Structure

### Data Assets by Category

<details>
<summary><b>📊 Source Data</b> (Authoritative, Original Sources)</summary>

| Asset Name | Type | Format | Records | Owner | Last Updated | Quality Score |
|------------|------|--------|---------|-------|--------------|---------------|
| `skidmore_all_firms_complete.json` | Firms | JSON Array | 38 | Data Team | 2025-12-10 | ✅ 95% |
| `skidmore_firms_database.csv` | Firms | CSV | 38 | Data Team | 2025-12-10 | ✅ 95% |
| `skidmore_individual_licenses.json` | Licenses | JSON Array | 40+ | Data Team | 2025-12-10 | ✅ 92% |
| `skidmore_individual_licenses.csv` | Licenses | CSV | 40+ | Data Team | 2025-12-10 | ✅ 92% |

**Location:** `data/source/`

**Description:** Original, authoritative data from Virginia DPOR and multi-state searches.

**Lineage:** External sources → Raw data collection → Source data

**Access:** Read-only for analysis scripts

</details>

<details>
<summary><b>🔧 Processed Data</b> (Cleaned, Normalized, Validated)</summary>

| Asset Name | Type | Format | Records | Owner | Last Updated | Quality Score |
|------------|------|--------|---------|-------|--------------|---------------|
| `firms.json` | Firms | JSON Array | 38 | Data Team | 2025-12-10 | ✅ 98% |
| `individual_licenses.json` | Licenses | JSON Array | 40+ | Data Team | 2025-12-10 | ✅ 97% |
| `dpor_all_cleaned.csv` | Combined | CSV | Variable | Data Team | 2025-12-10 | ✅ 96% |

**Location:** `data/cleaned/`

**Description:** Cleaned, normalized, and validated data ready for analysis.

**Lineage:** Source data → Data cleaning pipeline → Processed data

**Transformations:**
- Name standardization
- Address normalization
- Date parsing and validation
- Deduplication
- Schema validation

**Access:** Read-only for analysis scripts

</details>

<details>
<summary><b>🔗 Connection Data</b> (Relationships Between Entities)</summary>

| Asset Name | Type | Format | Records | Owner | Last Updated | Quality Score |
|------------|------|--------|---------|-------|--------------|---------------|
| `caitlin_skidmore_connections.json` | Connections | JSON Object | Variable | Research Team | 2025-12-10 | ✅ 94% |
| `dpor_skidmore_connections.csv` | Connections | CSV | Variable | Research Team | 2025-12-10 | ✅ 94% |
| `connection_matrix.json` | Matrix | JSON Object | N/A | Research Team | 2025-12-10 | ✅ 90% |
| `nexus_patterns_analysis.json` | Patterns | JSON Object | N/A | Research Team | 2025-12-10 | ✅ 88% |

**Location:** `research/connections/`

**Description:** Identified connections between firms, individuals, and entities.

**Connection Types:**
- Principal Broker relationships
- Same Address connections
- Known Firm matches
- Professional associations

**Lineage:** Processed data → Connection analysis → Connection data

**Access:** Read-only for research and analysis

</details>

<details>
<summary><b>⚠️ Violations & Anomalies</b> (Regulatory Compliance Issues)</summary>

| Asset Name | Type | Format | Records | Owner | Last Updated | Quality Score |
|------------|------|--------|---------|-------|--------------|---------------|
| `all_violations_consolidated.json` | Violations | JSON Array | Variable | Research Team | 2025-12-10 | ✅ 96% |
| `all_anomalies_consolidated.json` | Anomalies | JSON Array | Variable | Research Team | 2025-12-10 | ✅ 93% |
| `fraud_indicators.json` | Indicators | JSON Object | N/A | Research Team | 2025-12-10 | ✅ 91% |

**Location:** `research/violations/`, `research/anomalies/`

**Description:** Identified regulatory violations and data anomalies.

**Violation Types:**
- Principal Broker Gap violations
- Geographic violations
- Supervision impossibilities
- Unlicensed practice
- Timeline impossibilities

**Lineage:** Processed data + Connection data → Analysis → Violations/Anomalies

**Access:** Research team only

</details>

<details>
<summary><b>📄 Evidence</b> (Supporting Documents and Extracted Data)</summary>

| Asset Name | Type | Format | Records | Owner | Last Updated | Quality Score |
|------------|------|--------|---------|-------|--------------|---------------|
| `pdf_evidence_extracted.json` | PDF Evidence | JSON Array | Variable | Research Team | 2025-12-10 | ✅ 85% |
| `excel_evidence_extracted.json` | Excel Evidence | JSON Array | Variable | Research Team | 2025-12-10 | ✅ 87% |
| `all_evidence_summary.json` | Summary | JSON Object | N/A | Research Team | 2025-12-10 | ✅ 90% |

**Location:** `research/evidence/`, `evidence/`

**Description:** Extracted data from PDFs, Excel files, and other documents.

**Evidence Types:**
- PDF documents
- Excel spreadsheets
- Legal documents
- Correspondence

**Lineage:** External documents → Extraction pipeline → Evidence data

**Access:** Research team only

</details>

<details>
<summary><b>📈 Research Outputs</b> (Analysis Results and Reports)</summary>

| Asset Name | Type | Format | Records | Owner | Last Updated | Quality Score |
|------------|------|--------|---------|-------|--------------|---------------|
| `timeline_analysis.json` | Timeline | JSON Object | N/A | Research Team | 2025-12-10 | ✅ 92% |
| `shared_resources_analysis.json` | Resources | JSON Object | N/A | Research Team | 2025-12-10 | ✅ 89% |
| `filing_recommendations.json` | Recommendations | JSON Object | N/A | Research Team | 2025-12-10 | ✅ 95% |
| VA DPOR Complaint Files | Complaint | JSON/MD | Multiple | Research Team | 2025-12-10 | ✅ 98% |

**Location:** `research/`, `research/va_dpor_complaint/`

**Description:** Research analysis outputs, summaries, and complaint filings.

**Output Types:**
- Analysis reports
- Summary statistics
- Filing recommendations
- Complaint packages

**Lineage:** All data sources → Analysis pipeline → Research outputs

**Access:** Research team and authorized stakeholders

</details>

---

## Data Asset Metadata

### Metadata Standards

All data assets include standardized metadata following JSON Schema and industry best practices:

- **Identification**: Name, type, format, location
- **Ownership**: Owner, steward, last updated
- **Quality**: Quality score, validation status, issues
- **Lineage**: Source, transformations, dependencies
- **Access**: Access controls, compliance requirements
- **Usage**: Usage statistics, related assets

### Metadata Schema

See [metadata.json](./metadata.json) for the complete metadata schema definition.

---

## Data Discovery

### Search by Category

- **Source Data**: Original, authoritative data
- **Processed Data**: Cleaned and validated data
- **Connection Data**: Relationship mappings
- **Violations**: Regulatory compliance issues
- **Evidence**: Supporting documents
- **Research Outputs**: Analysis results

### Search by Type

- **JSON**: Structured data files
- **CSV**: Tabular data files
- **Markdown**: Documentation and reports
- **PDF**: Evidence documents
- **Excel**: Spreadsheet data

### Search by Purpose

- **Analysis**: Data for analysis and research
- **Compliance**: Regulatory compliance data
- **Evidence**: Supporting documentation
- **Reporting**: Reports and summaries

---

## Data Quality

### Quality Metrics

- **Completeness**: Percentage of required fields populated
- **Accuracy**: Validation against schema and business rules
- **Consistency**: Consistency across related data assets
- **Timeliness**: Data freshness and update frequency
- **Validity**: Adherence to schema and format requirements

### Quality Scores

Quality scores are calculated based on:
- Schema validation results
- Data completeness checks
- Cross-reference validation
- Business rule compliance

**Score Legend:**
- ✅ 95-100%: Excellent quality
- ✅ 90-94%: Good quality
- ⚠️ 85-89%: Acceptable quality
- ⚠️ <85%: Needs improvement

---

## Data Governance

### Ownership

- **Data Team**: Source and processed data
- **Research Team**: Research outputs, violations, evidence
- **Compliance Team**: Violations and compliance data

### Access Controls

- **Public**: Documentation and public reports
- **Internal**: Analysis scripts and research outputs
- **Restricted**: Sensitive evidence and violation data

### Compliance

- **Data Privacy**: PII handling and protection
- **Regulatory**: Compliance with regulatory requirements
- **Retention**: Data retention policies
- **Audit**: Audit trail and logging

---

## Data Lineage

### Lineage Tracking

All data assets include lineage information tracking:
- **Source**: Original data source
- **Transformations**: Processing steps applied
- **Dependencies**: Dependent data assets
- **Consumers**: Systems and processes using the data

See [Data Ancestry](./ANCESTRY.md) for detailed lineage documentation.

---

## Usage Guidelines

### Finding Data

1. **By Category**: Use the category sections above
2. **By Schema**: Check [Data Dictionary](./DATA_DICTIONARY.md) for field definitions
3. **By Relationships**: See [Data Ontology](./ONTOLOGY.md) for entity relationships
4. **By Lineage**: Review [Data Ancestry](./ANCESTRY.md) for data flow

### Using Data

1. **Check Quality Score**: Verify data quality before use
2. **Review Schema**: Understand data structure and constraints
3. **Check Lineage**: Understand data origin and transformations
4. **Validate**: Use schema validation before processing

### Contributing Data

1. **Follow Schema**: Ensure data adheres to schema.json
2. **Add Metadata**: Include complete metadata
3. **Document Lineage**: Document source and transformations
4. **Validate**: Run validation before committing

---

## Related Documentation

### Data documentation
- [Data Dictionary](./DATA_DICTIONARY.md) - Technical field definitions
- [Data Ontology](./ONTOLOGY.md) - Conceptual model and relationships
- [Data Ancestry](./ANCESTRY.md) - Data lineage and transformations
- [Data Governance](./GOVERNANCE.md) - Governance framework and policies
- [Schema](./schema.json) - JSON Schema definitions
- [Metadata Schema](./metadata.json) - Metadata structure definition
- [Data README](./README.md) - Data directory guide

### System documentation
- [Documentation Index](../docs/INDEX.md) - Complete documentation index
- [System Architecture](../docs/SYSTEM_ARCHITECTURE.md) - System architecture overview
- [System Analyst Guide](../docs/SYSTEM_ANALYST_GUIDE.md) - System analyst guide
- [Repository Structure](../docs/REPOSITORY_STRUCTURE.md) - Repository organization

---

## Maintenance

### Regular Updates

- **Weekly**: Quality score updates
- **Monthly**: Metadata reviews
- **Quarterly**: Catalog structure reviews
- **As Needed**: New asset additions

### Review Process

1. Data stewards review assigned assets
2. Quality metrics updated
3. Metadata refreshed
4. Documentation updated

---

**Last Updated:** 2025-12-10
**Catalog Version:** 1.0.0
**Maintained By:** Data Governance Team
