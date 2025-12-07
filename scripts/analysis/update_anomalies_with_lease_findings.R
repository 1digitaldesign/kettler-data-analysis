#!/usr/bin/env Rscript
# Update anomaly dataset with lease agreement findings
# Merge lease abnormalities with existing anomalies

library(jsonlite)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "all_anomalies_updated.json")

update_anomalies_with_lease <- function() {
  cat("=== Updating Anomalies with Lease Findings ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load existing anomalies
  consolidated_file <- file.path(RESEARCH_DIR, "all_anomalies_consolidated.json")
  lease_abnormalities_file <- file.path(RESEARCH_DIR, "lease_abnormalities_detailed.json")

  all_anomalies <- list()

  if (file.exists(consolidated_file)) {
    all_anomalies$existing <- fromJSON(consolidated_file)
    cat("Loaded existing anomalies\n")
  }

  if (file.exists(lease_abnormalities_file)) {
    all_anomalies$lease_findings <- fromJSON(lease_abnormalities_file)
    cat("Loaded lease abnormalities\n")
  }

  # Add new entity: Azure Carlyle LP
  new_entities <- list(
    azure_carlyle_lp = list(
      entity_name = "Azure Carlyle LP",
      entity_type = "Limited Partnership",
      role = "Property Owner",
      property = "800 John Carlyle Street",
      connection_to_kettler = "Kettler Management listed as manager",
      investigation_status = "needs_verification",
      search_frameworks_created = TRUE
    )
  )

  # Compile updated anomalies
  updated <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      update_type = "lease_findings_integration",
      sources = c("existing_anomalies", "lease_abnormalities", "new_entities")
    ),
    anomalies = all_anomalies,
    new_entities_identified = new_entities,
    summary = list(
      total_anomaly_sources = length(all_anomalies),
      new_entities = length(new_entities),
      note = "Anomalies updated with lease agreement findings"
    )
  )

  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(updated, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved updated anomalies to:", OUTPUT_FILE, "\n")

  return(updated)
}

if (!interactive()) update_anomalies_with_lease()
