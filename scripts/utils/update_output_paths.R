#!/usr/bin/env Rscript
# Update OUTPUT_FILE paths in all scripts
# Maps output files to appropriate research subdirectories

# Output file mappings
output_mappings <- list(
  # Connections
  "connection_matrix.json" = "RESEARCH_CONNECTIONS_DIR",
  "nexus_patterns_analysis.json" = "RESEARCH_CONNECTIONS_DIR",
  "real_nexus_analysis.json" = "RESEARCH_CONNECTIONS_DIR",
  "shared_resources_analysis.json" = "RESEARCH_CONNECTIONS_DIR",
  "hyland_skidmore_connections.json" = "RESEARCH_CONNECTIONS_DIR",
  "azure_carlyle_search.json" = "RESEARCH_CONNECTIONS_DIR",
  "azure_carlyle_findings.json" = "RESEARCH_CONNECTIONS_DIR",
  
  # Violations
  "all_violations_compiled.json" = "RESEARCH_VIOLATIONS_DIR",
  "hyland_upl_investigation.json" = "RESEARCH_VIOLATIONS_DIR",
  "upl_evidence_extracted.json" = "RESEARCH_VIOLATIONS_DIR",
  "news_violations_search.json" = "RESEARCH_VIOLATIONS_DIR",
  
  # Anomalies
  "all_anomalies_consolidated.json" = "RESEARCH_ANOMALIES_DIR",
  "all_anomalies_updated.json" = "RESEARCH_ANOMALIES_DIR",
  "additional_anomalies.json" = "RESEARCH_ANOMALIES_DIR",
  "fraud_indicators.json" = "RESEARCH_ANOMALIES_DIR",
  "new_anomalies_found.json" = "RESEARCH_ANOMALIES_DIR",
  
  # Evidence
  "all_evidence_summary.json" = "RESEARCH_EVIDENCE_DIR",
  "all_entities_extracted.json" = "RESEARCH_EVIDENCE_DIR",
  "all_individuals_identified.json" = "RESEARCH_EVIDENCE_DIR",
  "pdf_evidence_extracted.json" = "RESEARCH_EVIDENCE_DIR",
  "pdf_evidence_summary.csv" = "RESEARCH_EVIDENCE_DIR",
  "excel_evidence_extracted.json" = "RESEARCH_EVIDENCE_DIR",
  "excel_evidence_summary.csv" = "RESEARCH_EVIDENCE_DIR",
  "email_domain_analysis.json" = "RESEARCH_EVIDENCE_DIR",
  "str_listings_analysis.json" = "RESEARCH_EVIDENCE_DIR",
  "str_regulation_analysis.json" = "RESEARCH_EVIDENCE_DIR",
  "alexandria_zoning_analysis.json" = "RESEARCH_EVIDENCE_DIR",
  
  # Verification
  "hyland_verification.json" = "RESEARCH_VERIFICATION_DIR",
  "kettler_verification.json" = "RESEARCH_VERIFICATION_DIR",
  "skidmore_firms_validation.json" = "RESEARCH_VERIFICATION_DIR",
  "business_license_verification.json" = "RESEARCH_VERIFICATION_DIR",
  "property_management_license_verification.json" = "RESEARCH_VERIFICATION_DIR",
  "bar_association_verification_all.json" = "RESEARCH_VERIFICATION_DIR",
  "dpor_license_verification_all.json" = "RESEARCH_VERIFICATION_DIR",
  "management_chain_license_audit.json" = "RESEARCH_VERIFICATION_DIR",
  
  # Timelines
  "timeline_analysis.json" = "RESEARCH_TIMELINES_DIR",
  "lease_evidence_cross_reference.json" = "RESEARCH_TIMELINES_DIR",
  "lease_abnormalities_detailed.json" = "RESEARCH_TIMELINES_DIR",
  "lease_agreement_analysis.json" = "RESEARCH_TIMELINES_DIR",
  
  # Summaries
  "filing_recommendations.json" = "RESEARCH_SUMMARIES_DIR",
  "FINAL_COMPREHENSIVE_AUDIT_REPORT.md" = "RESEARCH_SUMMARIES_DIR",
  
  # Search results
  "captcha_handled_searches.json" = "RESEARCH_SEARCH_RESULTS_DIR",
  "kettler_employees_all_states_license_search.json" = "RESEARCH_SEARCH_RESULTS_DIR",
  "kettler_employees_license_search_comprehensive.json" = "RESEARCH_SEARCH_RESULTS_DIR",
  "kettler_employees_license_search_results.json" = "RESEARCH_SEARCH_RESULTS_DIR"
)

cat("Output file mappings:\n")
for (filename in names(output_mappings)) {
  cat(sprintf("  %s -> %s\n", filename, output_mappings[[filename]]))
}

cat("\nUse this mapping to update OUTPUT_FILE definitions in scripts\n")
