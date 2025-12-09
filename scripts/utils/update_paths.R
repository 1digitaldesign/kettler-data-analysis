#!/usr/bin/env Rscript
# Path Update Utility
# Updates file paths in scripts to use new organized structure

# This script helps identify and update file paths that need to be changed
# Run this to see what needs updating, then update manually or with sed

cat("=== Path Update Utility ===\n")
cat("This script identifies files that reference old paths\n\n")

# Common path mappings
path_mappings <- list(
  # Research files
  "research/evidence/all_entities_extracted.json" = "research/evidence/all_entities_extracted.json",
  "research/evidence/all_evidence_summary.json" = "research/evidence/all_evidence_summary.json",
  "research/pdf_evidence_extracted.json" = "research/evidence/pdf_evidence_extracted.json",
  "research/pdf_evidence_summary.csv" = "research/evidence/pdf_evidence_summary.csv",
  "research/excel_evidence_extracted.json" = "research/evidence/excel_evidence_extracted.json",
  "research/excel_evidence_summary.csv" = "research/evidence/excel_evidence_summary.csv",
  "research/connections/caitlin_skidmore_connections.json" = "research/connections/caitlin_skidmore_connections.json",
  "research/hyland_skidmore_connections.json" = "research/connections/hyland_skidmore_connections.json",
  "research/connection_matrix.json" = "research/connections/connection_matrix.json",
  "research/real_nexus_analysis.json" = "research/connections/real_nexus_analysis.json",
  "research/nexus_patterns_analysis.json" = "research/connections/nexus_patterns_analysis.json",
  "research/all_violations_compiled.json" = "research/violations/all_violations_compiled.json",
  "research/hyland_upl_investigation.json" = "research/violations/hyland_upl_investigation.json",
  "research/upl_evidence_extracted.json" = "research/violations/upl_evidence_extracted.json",
  "research/all_anomalies_consolidated.json" = "research/anomalies/all_anomalies_consolidated.json",
  "research/all_anomalies_updated.json" = "research/anomalies/all_anomalies_updated.json",
  "research/additional_anomalies.json" = "research/anomalies/additional_anomalies.json",
  "research/fraud_indicators.json" = "research/anomalies/fraud_indicators.json",
  "research/verification/hyland_verification.json" = "research/verification/hyland_verification.json",
  "research/verification/kettler_verification.json" = "research/verification/kettler_verification.json",
  "research/skidmore_firms_validation.json" = "research/verification/skidmore_firms_validation.json",
  "research/timeline_analysis.json" = "research/timelines/timeline_analysis.json",
  "research/filing_recommendations.json" = "research/summaries/filing_recommendations.json",

  # Config files
  "config/state_dpor_registry.csv" = "config/state_dpor_registry.csv",

  # Script references
  "search_multi_state_dpor.R" = "bin/search_states.R",
  "analyze_skidmore_connections.R" = "bin/analyze_connections.R",
  "validate_data_quality.R" = "bin/validate_data.R",
  "generate_outputs.R" = "bin/generate_reports.R",
  "clean_dpor_data.py" = "bin/clean_data.py"
)

cat("Path mappings to apply:\n")
for (old_path in names(path_mappings)) {
  cat(sprintf("  %s -> %s\n", old_path, path_mappings[[old_path]]))
}

cat("\nNote: Update scripts manually or use sed/perl to apply these changes\n")
