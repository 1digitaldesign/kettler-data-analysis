# Data Quick Reference Guide

**Last Updated:** 2025-12-08

## 📊 Primary Data Files

### 1. Firms Data (Main Dataset)
**File:** `source/skidmore_all_firms_complete.json`
**Primary Key:** `firm_license`
**Records:** 38 firms

**Key Fields:**
- `firm_license` (PK): 10-digit license number
- `firm_name`: Legal name
- `address`: Business address
- `state`: Two-letter state code
- `principal_broker`: "SKIDMORE CAITLIN MARIE"

**Status:** ✅ 100% complete

### 2. Individual Licenses
**File:** `source/skidmore_individual_licenses.json`
**Primary Key:** `license_number`
**Records:** 40+ licenses

**Key Fields:**
- `license_number` (PK): 10-digit license number
- `name`: "SKIDMORE, CAITLIN MARIE"
- `address`: License address

## 🔑 Primary Keys

| Table | Primary Key | Format | Example |
|-------|-------------|--------|---------|
| **firms** | `firm_license` | 10 digits | `0226025311` |
| **individual_licenses** | `license_number` | 10 digits | `0225258285` |

## 🔗 Foreign Keys

| From Table | From Column | To Table | To Column | Type |
|------------|-------------|----------|-----------|------|
| `firms` | `individual_license` | `individual_licenses` | `license_number` | Optional |

## 📋 Common Queries

### Get all firms
```python
import json
with open('data/source/skidmore_all_firms_complete.json') as f:
    data = json.load(f)
    firms = data['companies']
```

### Find firm by license number
```python
firm = next((f for f in firms if f['firm_license'] == '0226025311'), None)
```

### Get firms by state
```python
tx_firms = [f for f in firms if f['state'] == 'TX']
```

### Count firms by state
```python
from collections import Counter
state_counts = Counter(f['state'] for f in firms)
```

## ✅ Data Validation

Run schema validation:
```bash
cd data
python3 validate_schema.py
```

## 📚 Full Documentation

- **Schema:** [`SCHEMA.md`](./SCHEMA.md)
- **JSON Schema:** [`schema.json`](./schema.json)
- **SQL DDL:** [`schema.sql`](./schema.sql)
