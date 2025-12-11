# ML-Enhanced Violation Analysis Report

Generated: 2025-12-11 01:48:09

## Executive Summary

- **Total Violations**: 20
- **High-Risk Entities**: 0
- **Violation Clusters**: 1
- **Anomalies Detected**: 2
- **Risk Level**: HIGH
- **ML Risk Score Range**: 0.500 - 0.500 (mean: 0.500)

## Key Findings

### Violations by Type

- **tax_forfeitures**: 2 violations
- **forfeited_entities**: 3 violations
- **filing_violations**: 4 violations
- **address_violations**: 11 violations
- **management_violations**: 0 violations

### ML Analysis Results

- **Clusters (K-Means)**: 5
- **Anomalies Detected**: 2
- **Network Communities**: 10

### Visualizations

- **Error**: `matplotlib not available`

### High-Risk Entities


## Recommendations

1. **[HIGH]** Investigate tax forfeiture events for potential tax evasion
   - 20 violations identified

2. **[HIGH]** Review ML-detected anomalies for unusual tax structures
   - 2 anomalies detected by Isolation Forest and LOF

3. **[MEDIUM]** Examine DBSCAN outliers for potential shell companies
   - 14 outliers detected

