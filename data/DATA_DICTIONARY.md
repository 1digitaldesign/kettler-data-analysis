# Data Dictionary

Complete field definitions, types, constraints, and examples for all data entities in the Kettler Data Analysis repository.

## Table of Contents

- [Firms](#firms)
- [Individual Licenses](#individual-licenses)
- [Connections](#connections)
- [Research Outputs](#research-outputs)
- [Violations](#violations)
- [Evidence](#evidence)

---

## Firms

**Table:** `firms`
**Primary Key:** `firm_license`
**Source File:** `data/cleaned/firms.json`
**Description:** Real estate firm licenses from Virginia DPOR

### Fields

| Field Name | Type | Required | Unique | Format | Description | Example |
|------------|------|----------|--------|--------|-------------|---------|
| `firm_license` | string | Yes | Yes | `^[0-9]{10}$` | 10-digit Virginia DPOR license number (PK) | `"0226025311"` |
| `firm_name` | string | Yes | No | - | Legal name of the firm | `"KETTLER MANAGEMENT INC"` |
| `license_type` | string | Yes | No | - | Type of license | `"Real Estate Firm License"` |
| `firm_type` | string | No | No | - | Legal entity type | `"Corporation"` |
| `address` | string | Yes | No | - | Business address | `"8255 GREENSBORO DR STE 200, MCLEAN, VA 22102"` |
| `state` | string | Yes | No | `^[A-Z]{2}$` | Two-letter state code | `"VA"` |
| `principal_broker` | string | Yes | No | - | Name of principal broker | `"SKIDMORE CAITLIN MARIE"` |
| `initial_cert_date` | string | No | No | `YYYY-MM-DD` | Initial certification date | `"2014-10-31"` |
| `expiration_date` | string | No | No | `YYYY-MM-DD` | License expiration date | `"2026-10-31"` |
| `individual_license` | string | No | No | `^[0-9]{10}$` | FK to `individual_licenses.license_number` | `"0225258285"` |
| `gap_years` | number | No | No | - | Years between firm license and principal broker license | `11` |

### Constraints

- `firm_license` must be unique and exactly 10 digits
- `principal_broker` cannot be null
- `address` cannot be null
- `firm_name` cannot be null

### Indexes

- `firm_name` - For name searches
- `state` - For state filtering
- `principal_broker` - For broker searches
- `address` - For address matching

### Foreign Keys

- `individual_license` → `individual_licenses.license_number` (optional, many-to-one)

---

## Individual Licenses

**Table:** `individual_licenses`
**Primary Key:** `license_number`
**Source File:** `data/cleaned/individual_licenses.json`
**Description:** Individual real estate licenses

### Fields

| Field Name | Type | Required | Unique | Format | Description | Example |
|------------|------|----------|--------|--------|-------------|---------|
| `license_number` | string | Yes | Yes | `^[0-9]{10}$` | 10-digit license number (PK) | `"0225258285"` |
| `name` | string | Yes | No | - | License holder name | `"SKIDMORE, CAITLIN MARIE"` |
| `address` | string | No | No | - | Address associated with license | `"FRISCO, TX 75034"` |
| `license_type` | string | Yes | No | - | Type of license | `"Real Estate Individual"` |
| `board` | string | No | No | - | Regulatory board | `"Real Estate Board"` |
| `state` | string | Yes | No | `^[A-Z]{2}$` | Two-letter state code | `"TX"` |
| `expiration_date` | string | No | No | `YYYY-MM-DD` | License expiration date | `"2026-10-31"` |

### Constraints

- `license_number` must be unique and exactly 10 digits
- `name` cannot be null
- `state` must be a valid 2-letter state code

### Indexes

- `name` - For name searches
- `state` - For state filtering
- `license_type` - For license type filtering

### Foreign Keys

- None (this is a root entity)

---

## Connections

**Table:** `connections`
**Primary Key:** `connection_id`
**Source File:** `research/connections/caitlin_skidmore_connections.json`
**Description:** Connections between firms and individuals

### Fields

| Field Name | Type | Required | Unique | Format | Description | Example |
|------------|------|----------|--------|--------|-------------|---------|
| `connection_id` | string | Yes | Yes | `^[a-f0-9]{32}$` | Auto-generated connection ID (PK) | `"abc123def456..."` |
| `firm_license` | string | No | No | `^[0-9]{10}$` | FK to `firms.firm_license` | `"0226025311"` |
| `license_number` | string | No | No | `^[0-9]{10}$` | FK to `individual_licenses.license_number` | `"0225258285"` |
| `connection_type` | string | Yes | No | enum | Type of connection | `"Principal Broker"` |
| `connection_detail` | string | No | No | - | Detailed description of connection | `"Listed as Principal Broker: SKIDMORE CAITLIN MARIE"` |
| `state` | string | No | No | `^[A-Z]{2}$` | State where connection exists | `"VA"` |
| `firm_name` | string | No | No | - | Firm name (denormalized) | `"KETTLER MANAGEMENT INC"` |
| `verified` | boolean | No | No | - | Whether connection has been verified | `false` |
| `analysis_date` | string | No | No | `YYYY-MM-DD` | Date connection was identified | `"2025-12-07"` |

### Connection Types (enum)

- `"Principal Broker"` - Individual is listed as principal broker
- `"Same Address"` - Firms share the same address
- `"Same Address as Known Firm"` - Address matches a known firm
- `"Known Firm Match"` - Direct firm match
- `"Professional Association"` - Professional relationship
- `"Corporate Relationship"` - Corporate connection

### Constraints

- `connection_id` must be unique
- `connection_type` cannot be null
- At least one of `firm_license` or `license_number` must be present

### Indexes

- `firm_license` - For firm-based queries
- `license_number` - For license-based queries
- `connection_type` - For type filtering
- `state` - For state filtering

### Foreign Keys

- `firm_license` → `firms.firm_license` (optional, many-to-one)
- `license_number` → `individual_licenses.license_number` (optional, many-to-one)

---

## Research Outputs

**Table:** `research_outputs`
**Primary Key:** `research_id`
**Source File:** `research/` (multiple files)
**Description:** Research analysis outputs and findings

### Fields

| Field Name | Type | Required | Unique | Format | Description | Example |
|------------|------|----------|--------|--------|-------------|---------|
| `research_id` | string | Yes | Yes | `^[a-f0-9]{32}$` | Auto-generated research ID (PK) | `"def456ghi789..."` |
| `file_path` | string | Yes | Yes | - | Relative path to research file | `"research/connections/caitlin_skidmore_connections.json"` |
| `category` | string | Yes | No | enum | Research category | `"connections"` |
| `firm_license` | string | No | No | `^[0-9]{10}$` | FK to `firms.firm_license` (if firm-specific) | `"0226025311"` |
| `license_number` | string | No | No | `^[0-9]{10}$` | FK to `individual_licenses.license_number` (if license-specific) | `"0225258285"` |
| `analysis_date` | string | No | No | `YYYY-MM-DD` | Date analysis was performed | `"2025-12-07"` |
| `findings_summary` | string | No | No | - | Brief summary of findings | `"Found 38 firms connected to Caitlin Skidmore"` |
| `status` | string | No | No | enum | Research status | `"complete"` |
| `metadata` | object | No | No | - | Additional metadata from research file | `{}` |

### Categories (enum)

- `"connections"` - Connection analyses
- `"violations"` - Violation findings
- `"anomalies"` - Anomaly reports
- `"evidence"` - Evidence documents
- `"verification"` - Verification results
- `"timelines"` - Timeline analyses
- `"summaries"` - Summary reports
- `"search_results"` - Search results
- `"analysis"` - General analysis outputs
- `"va_dpor_complaint"` - VA DPOR complaint research

### Status Values (enum)

- `"complete"` - Research is complete
- `"in_progress"` - Research is ongoing
- `"pending"` - Research is pending
- `"verified"` - Research has been verified

### Constraints

- `research_id` must be unique
- `file_path` should be unique
- `category` cannot be null

### Indexes

- `category` - For category filtering
- `firm_license` - For firm-specific research
- `license_number` - For license-specific research
- `analysis_date` - For date-based queries
- `status` - For status filtering

### Foreign Keys

- `firm_license` → `firms.firm_license` (optional, many-to-one)
- `license_number` → `individual_licenses.license_number` (optional, many-to-one)

---

## Violations

**Table:** `violations`
**Primary Key:** `violation_id`
**Source File:** `research/violations/` (multiple files)
**Description:** Regulatory violations identified

### Fields

| Field Name | Type | Required | Unique | Format | Description | Example |
|------------|------|----------|--------|--------|-------------|---------|
| `violation_id` | string | Yes | Yes | `^[a-f0-9]{32}$` | Auto-generated violation ID (PK) | `"ghi789jkl012..."` |
| `violation_type` | string | Yes | No | enum | Type of violation | `"Principal Broker Gap"` |
| `firm_license` | string | No | No | `^[0-9]{10}$` | FK to `firms.firm_license` | `"0226025311"` |
| `license_number` | string | No | No | `^[0-9]{10}$` | FK to `individual_licenses.license_number` | `"0225258285"` |
| `severity` | string | No | No | enum | Violation severity | `"High"` |
| `description` | string | Yes | No | - | Detailed description of violation | `"Firm licensed 10.5 years before principal broker"` |
| `evidence_files` | array[string] | No | No | - | List of evidence file paths | `["research/va_dpor_complaint/principal_broker_gap_analysis.json"]` |
| `state` | string | No | No | `^[A-Z]{2}$` | State where violation occurred | `"VA"` |
| `identified_date` | string | No | No | `YYYY-MM-DD` | Date violation was identified | `"2025-12-07"` |

### Violation Types (enum)

- `"Principal Broker Gap"` - Firm licensed before principal broker
- `"Geographic Violation"` - Geographic impossibility
- `"Supervision Impossibility"` - Cannot supervise from location
- `"Unlicensed Practice"` - Practice without license
- `"Timeline Impossibility"` - Timeline conflicts
- `"Regulatory Violation"` - General regulatory violation
- `"50-Mile Rule Violation"` - Violation of 50-mile supervision rule

### Severity Values (enum)

- `"High"` - High severity violation
- `"Medium"` - Medium severity violation
- `"Low"` - Low severity violation

### Constraints

- `violation_id` must be unique
- `violation_type` cannot be null
- `description` cannot be null
- At least one of `firm_license` or `license_number` should be present

### Indexes

- `violation_type` - For type filtering
- `firm_license` - For firm-based queries
- `license_number` - For license-based queries
- `severity` - For severity filtering
- `state` - For state filtering

### Foreign Keys

- `firm_license` → `firms.firm_license` (optional, many-to-one)
- `license_number` → `individual_licenses.license_number` (optional, many-to-one)

---

## Evidence

**Table:** `evidence`
**Primary Key:** `evidence_id`
**Source File:** `evidence/` (multiple files)
**Description:** Evidence documents and extracted data

### Fields

| Field Name | Type | Required | Unique | Format | Description | Example |
|------------|------|----------|--------|--------|-------------|---------|
| `evidence_id` | string | Yes | Yes | `^[a-f0-9]{32}$` | Auto-generated evidence ID (PK) | `"jkl012mno345..."` |
| `file_path` | string | Yes | No | - | Path to evidence file | `"evidence/pdfs/lease_termination.pdf"` |
| `evidence_type` | string | Yes | No | enum | Type of evidence | `"PDF"` |
| `violation_id` | string | No | No | `^[a-f0-9]{32}$` | FK to `violations.violation_id` | `"ghi789jkl012..."` |
| `extracted_data` | object | No | No | - | Extracted entities and data from evidence | `{"entities": [], "dates": []}` |
| `extraction_date` | string | No | No | `YYYY-MM-DD` | Date evidence was extracted | `"2025-12-07"` |
| `source` | string | No | No | - | Source of evidence | `"Lease termination document"` |

### Evidence Types (enum)

- `"PDF"` - PDF document
- `"Excel"` - Excel spreadsheet
- `"Email"` - Email correspondence
- `"Legal Document"` - Legal document
- `"LinkedIn Profile"` - LinkedIn profile
- `"Web Page"` - Web page
- `"Correspondence"` - General correspondence

### Constraints

- `evidence_id` must be unique
- `file_path` cannot be null
- `evidence_type` cannot be null

### Indexes

- `evidence_type` - For type filtering
- `violation_id` - For violation-based queries
- `extraction_date` - For date-based queries

### Foreign Keys

- `violation_id` → `violations.violation_id` (optional, many-to-one)

---

## Data Types Reference

### String Types

- **License Number**: Exactly 10 digits (`^[0-9]{10}$`)
- **State Code**: Two uppercase letters (`^[A-Z]{2}$`)
- **Date**: ISO 8601 format (`YYYY-MM-DD`)
- **ID**: 32-character hexadecimal (`^[a-f0-9]{32}$`)

### Enum Types

- **Connection Types**: See [Connections](#connections) section
- **Research Categories**: See [Research Outputs](#research-outputs) section
- **Violation Types**: See [Violations](#violations) section
- **Evidence Types**: See [Evidence](#evidence) section
- **Severity Levels**: High, Medium, Low
- **Status Values**: complete, in_progress, pending, verified

### Array Types

- **Evidence Files**: Array of file path strings
- **Extracted Data**: Object containing arrays of entities, dates, etc.

### Object Types

- **Metadata**: Flexible object structure for additional data
- **Extracted Data**: Structured object with entity arrays and properties

---

## Entity-Relationship Diagram

```mermaid
erDiagram
    FIRMS ||--o{ CONNECTIONS : "has"
    INDIVIDUAL_LICENSES ||--o{ CONNECTIONS : "has"
    FIRMS ||--o| INDIVIDUAL_LICENSES : "principal_broker"
    FIRMS ||--o{ RESEARCH_OUTPUTS : "analyzed_in"
    INDIVIDUAL_LICENSES ||--o{ RESEARCH_OUTPUTS : "analyzed_in"
    FIRMS ||--o{ VIOLATIONS : "violates"
    INDIVIDUAL_LICENSES ||--o{ VIOLATIONS : "violates"
    VIOLATIONS ||--o{ EVIDENCE : "supported_by"

    FIRMS {
        string firm_license PK
        string firm_name
        string address
        string state
        string principal_broker
        string individual_license FK
        date initial_cert_date
        date expiration_date
    }

    INDIVIDUAL_LICENSES {
        string license_number PK
        string name
        string address
        string state
        string license_type
        date expiration_date
    }

    CONNECTIONS {
        string connection_id PK
        string firm_license FK
        string license_number FK
        string connection_type
        string connection_detail
        string state
        boolean verified
    }

    RESEARCH_OUTPUTS {
        string research_id PK
        string file_path
        string category
        string firm_license FK
        string license_number FK
        date analysis_date
        string status
    }

    VIOLATIONS {
        string violation_id PK
        string violation_type
        string firm_license FK
        string license_number FK
        string severity
        string description
        array evidence_files
    }

    EVIDENCE {
        string evidence_id PK
        string file_path
        string evidence_type
        string violation_id FK
        object extracted_data
        date extraction_date
    }
```

## Related Documentation

- [Schema Definition](./schema.json) - Complete JSON schema
- [Data Ontology](./ONTOLOGY.md) - Conceptual relationships
- [Data Ancestry](./ANCESTRY.md) - Data lineage and transformations
- [Repository Structure](../docs/REPOSITORY_STRUCTURE.md) - File organization
