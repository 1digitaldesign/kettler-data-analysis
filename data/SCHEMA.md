# Database Schema Documentation

**Last Updated:** 2025-12-08
**Version:** 1.0.0

## Overview

This document describes the complete database schema for the Kettler Data Analysis project. All datasets are normalized with clearly defined primary keys (PK) and foreign keys (FK).

## Entity Relationship Diagram

```
┌─────────────────────┐
│  individual_licenses│
│  PK: license_number │
└──────────┬──────────┘
           │
           │ (optional FK)
           │
┌──────────▼──────────┐
│      firms          │
│  PK: firm_license  │
│  FK: individual_   │
│      license        │
└──────────┬──────────┘
           │
           │ (FK)
           │
┌──────────▼──────────┐
│ firm_connections    │
│ PK: connection_id   │
│ FK: firm_license_1  │
│ FK: firm_license_2  │
└─────────────────────┘

┌─────────────────────┐
│    str_listings     │
│  PK: listing_id     │
│  (independent)      │
└─────────────────────┘

┌─────────────────────┐
│ analysis_results    │
│ PK: analysis_id     │
│  (independent)      │
└─────────────────────┘
```

## Tables

### 1. `firms` (Primary Table)

**File:** `cleaned/firms.json` (cleaned and deduplicated)
**Description:** Real estate firms associated with Caitlin Skidmore as principal broker

**Primary Key:** `firm_license` (10-digit Virginia DPOR license number)

| Column | Type | Required | Description | Constraints |
|--------|------|----------|-------------|-------------|
| `firm_license` | STRING(10) | ✅ | **PK:** 10-digit license number | Pattern: `^[0-9]{10}$`, UNIQUE |
| `firm_name` | STRING | ✅ | Legal name of the firm | |
| `individual_license` | STRING(10) \| NULL | ❌ | **FK:** References `individual_licenses.license_number` | Pattern: `^[0-9]{10}$` |
| `license_type` | STRING | ✅ | Type of license | Enum: `["Real Estate Firm License"]` |
| `firm_type` | STRING | ✅ | Legal entity type | Enum: `["Corporation", "LLC - Limited Liability Company", "Solely owned LLC", "LLC", "Limited Partnership", "LP"]` |
| `address` | STRING | ✅ | Business address | NOT NULL |
| `dba_name` | STRING \| NULL | ❌ | Doing Business As name | |
| `initial_cert_date` | DATE \| NULL | ❌ | Initial certification date (YYYY-MM-DD) | Format: `YYYY-MM-DD` |
| `expiration_date` | DATE | ✅ | License expiration date (YYYY-MM-DD) | Format: `YYYY-MM-DD`, > initial_cert_date |
| `principal_broker` | STRING | ✅ | Principal broker name | Must be `"SKIDMORE CAITLIN MARIE"` |
| `gap_years` | DECIMAL \| NULL | ❌ | Years between firm license and Skidmore's license | Negative if firm licensed after Skidmore |
| `state` | STRING(2) | ✅ | Two-letter state code | Pattern: `^[A-Z]{2}$` |
| `notes` | STRING | ❌ | Additional notes | |
| `needs_verification` | BOOLEAN | ✅ | Whether data needs verification | Default: `false` |
| `verification_date` | DATE \| NULL | ❌ | Date when data was verified | Format: `YYYY-MM-DD` |

**Indexes:**
- `firm_name` (non-unique)
- `state` (non-unique)
- `principal_broker` (non-unique)
- `address` (non-unique)

**Foreign Keys:**
- `individual_license` → `individual_licenses.license_number` (optional, many-to-one)

**Constraints:**
- `principal_broker` must equal `"SKIDMORE CAITLIN MARIE"`
- `expiration_date` must be after `initial_cert_date` (if both are not null)

---

### 2. `individual_licenses`

**File:** `cleaned/individual_licenses.json` (cleaned and deduplicated)
**Description:** Individual real estate licenses for Caitlin Skidmore across multiple states

**Primary Key:** `license_number` (10-digit license number)

| Column | Type | Required | Description | Constraints |
|--------|------|----------|-------------|-------------|
| `license_number` | STRING(10) | ✅ | **PK:** 10-digit license number | Pattern: `^[0-9]{10}$`, UNIQUE |
| `name` | STRING | ✅ | License holder name | Must be `"SKIDMORE, CAITLIN MARIE"` |
| `address` | STRING | ✅ | Address associated with license | |
| `license_type` | STRING | ✅ | Type of license | Enum: `["Real Estate Individual"]` |
| `board` | STRING | ✅ | Licensing board | Enum: `["Real Estate Board"]` |
| `state` | STRING(2) | ❌ | Two-letter state code | Pattern: `^[A-Z]{2}$` (computed) |

**Indexes:**
- `name` (non-unique)
- `address` (non-unique)

**Constraints:**
- `name` must equal `"SKIDMORE, CAITLIN MARIE"`

---

### 3. `str_listings`

**File:** `scraped/*.json` (multiple files)
**Description:** Short-term rental listings scraped from various platforms

**Primary Key:** `listing_id` (unique identifier)

| Column | Type | Required | Description | Constraints |
|--------|------|----------|-------------|-------------|
| `listing_id` | STRING | ✅ | **PK:** Unique identifier | UNIQUE |
| `platform` | STRING | ✅ | Platform where listing was found | Enum: `["Airbnb", "VRBO", "Front Website", "Other"]` |
| `property_address` | STRING | ✅ | Address of the property | |
| `property_name` | STRING \| NULL | ❌ | Name/title of the listing | |
| `scraped_date` | DATE | ✅ | Date when listing was scraped | Format: `YYYY-MM-DD` |
| `metadata` | OBJECT | ❌ | Additional metadata from scraping | |

**Indexes:**
- `platform` (non-unique)
- `property_address` (non-unique)
- `scraped_date` (non-unique)

**Composite Key:** `(platform, property_address, scraped_date)` for deduplication

---

### 4. `firm_connections`

**File:** `analysis/dpor_skidmore_connections.csv`
**Description:** Connections and relationships between firms

**Primary Key:** `connection_id` (unique identifier)

| Column | Type | Required | Description | Constraints |
|--------|------|----------|-------------|-------------|
| `connection_id` | STRING | ✅ | **PK:** Unique identifier | UNIQUE |
| `firm_license_1` | STRING(10) | ✅ | **FK:** First firm | Pattern: `^[0-9]{10}$` |
| `firm_license_2` | STRING(10) | ✅ | **FK:** Second firm | Pattern: `^[0-9]{10}$` |
| `connection_type` | STRING | ✅ | Type of connection | Enum: `["same_address", "same_principal_broker", "same_license_date", "other"]` |
| `connection_strength` | DECIMAL(0-1) | ❌ | Strength of connection | Range: 0-1 |

**Indexes:**
- `firm_license_1` (non-unique)
- `firm_license_2` (non-unique)
- `connection_type` (non-unique)

**Foreign Keys:**
- `firm_license_1` → `firms.firm_license` (many-to-one)
- `firm_license_2` → `firms.firm_license` (many-to-one)

**Composite Key:** `(firm_license_1, firm_license_2)` for uniqueness

---

### 5. `analysis_results`

**File:** `analysis/*.json` (multiple files)
**Description:** Analysis outputs and quality reports

**Primary Key:** `analysis_id` (unique identifier)

| Column | Type | Required | Description | Constraints |
|--------|------|----------|-------------|-------------|
| `analysis_id` | STRING | ✅ | **PK:** Unique identifier | UNIQUE |
| `analysis_type` | STRING | ✅ | Type of analysis | Enum: `["data_quality", "connection_analysis", "validation", "summary"]` |
| `analysis_date` | DATE | ✅ | Date when analysis was run | Format: `YYYY-MM-DD` |
| `results` | OBJECT | ✅ | Analysis results | Structure varies by type |

**Indexes:**
- `analysis_type` (non-unique)
- `analysis_date` (non-unique)

---

## Relationships

### Foreign Key Relationships

1. **firms → individual_licenses** (optional)
   - `firms.individual_license` → `individual_licenses.license_number`
   - Relationship: Many-to-One (optional)
   - Description: A firm may reference an individual license

2. **firm_connections → firms** (two relationships)
   - `firm_connections.firm_license_1` → `firms.firm_license`
   - `firm_connections.firm_license_2` → `firms.firm_license`
   - Relationship: Many-to-One (required)
   - Description: Connections reference firms

## Data Quality Rules

### Firms Table
- `firm_license` must be exactly 10 digits
- `address` cannot be null
- `expiration_date` must be a valid date
- `expiration_date` must be after `initial_cert_date` (if both are not null)
- `principal_broker` must equal `"SKIDMORE CAITLIN MARIE"`

### Individual Licenses Table
- `license_number` must be exactly 10 digits
- `name` must equal `"SKIDMORE, CAITLIN MARIE"`

### Firm Connections Table
- `firm_license_1` and `firm_license_2` must reference valid firms
- `firm_license_1` ≠ `firm_license_2` (no self-connections)

## File Mappings

| Table | File(s) | Format |
|-------|---------|--------|
| `firms` | `source/skidmore_all_firms_complete.json` | JSON |
| `individual_licenses` | `source/skidmore_individual_licenses.json`<br>`source/skidmore_individual_licenses.csv` | JSON, CSV |
| `str_listings` | `scraped/airbnb_listings_john_carlyle.json`<br>`scraped/vrbo_listings_john_carlyle.json`<br>`scraped/front_website_listings.json`<br>`scraped/additional_str_listings.json` | JSON |
| `firm_connections` | `analysis/dpor_skidmore_connections.csv` | CSV |
| `analysis_results` | `analysis/data_quality_report.json`<br>`analysis/analysis_summary.json` | JSON |

## Usage Examples

### Query Firms by State
```sql
SELECT firm_name, firm_license, address, expiration_date
FROM firms
WHERE state = 'TX'
ORDER BY initial_cert_date;
```

### Find Firms with Same Address
```sql
SELECT f1.firm_name, f2.firm_name, f1.address
FROM firms f1
JOIN firms f2 ON f1.address = f2.address
WHERE f1.firm_license < f2.firm_license;
```

### Get Firm Connections
```sql
SELECT
    f1.firm_name AS firm_1,
    f2.firm_name AS firm_2,
    fc.connection_type,
    fc.connection_strength
FROM firm_connections fc
JOIN firms f1 ON fc.firm_license_1 = f1.firm_license
JOIN firms f2 ON fc.firm_license_2 = f2.firm_license;
```

## Schema Version History

- **v1.0.0** (2025-12-08): Initial schema definition with PKs/FKs
