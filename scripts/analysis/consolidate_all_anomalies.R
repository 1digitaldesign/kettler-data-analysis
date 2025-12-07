#!/usr/bin/env Rscript
# Consolidate all anomalies from various sources into single dataset
# Merge new anomalies with existing anomaly reports

library(jsonlite)
library(dplyr)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "all_anomalies_consolidated.json")

consolidate_all_anomalies <- function() {
  cat("=== Consolidating All Anomalies ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load all anomaly sources
  anomaly_sources <- list()

  # Load new anomalies
  new_file <- file.path(RESEARCH_DIR, "new_anomalies_found.json")
  if (file.exists(new_file)) {
    anomaly_sources$new_anomalies <- fromJSON(new_file)
    cat("Loaded new anomalies\n")
  }

  # Load additional anomalies
  additional_file <- file.path(RESEARCH_DIR, "additional_anomalies.json")
  if (file.exists(additional_file)) {
    anomaly_sources$additional_anomalies <- fromJSON(additional_file)
    cat("Loaded additional anomalies\n")
  }

  # Load nexus patterns (contains anomalies)
  nexus_file <- file.path(RESEARCH_DIR, "nexus_patterns_analysis.json")
  if (file.exists(nexus_file)) {
    anomaly_sources$nexus_patterns <- fromJSON(nexus_file)
    cat("Loaded nexus patterns\n")
  }

  # Load timeline analysis (contains anomalies)
  timeline_file <- file.path(RESEARCH_DIR, "timeline_analysis.json")
  if (file.exists(timeline_file)) {
    anomaly_sources$timeline_analysis <- fromJSON(timeline_file)
    cat("Loaded timeline analysis\n")
  }

  # Consolidate
  consolidated <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      consolidation_date = as.character(Sys.Date()),
      sources_consolidated = names(anomaly_sources)
    ),
    all_anomalies = anomaly_sources,
    summary = list(
      total_sources = length(anomaly_sources),
      note = "All anomalies consolidated from multiple analysis sources"
    )
  )

  # Save
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(consolidated, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved consolidated anomalies to:", OUTPUT_FILE, "\n")

  return(consolidated)
}

if (!interactive()) consolidate_all_anomalies()
