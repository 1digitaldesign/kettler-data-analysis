#!/usr/bin/env Rscript
# Research Path Utilities
# Helper functions for accessing research files in organized structure

# Load main paths first
if (!exists("RESEARCH_DIR")) {
  source(file.path(dirname(dirname(dirname(getwd()))), "scripts", "utils", "paths.R"))
}

# Research file path helpers
get_research_file <- function(category, filename) {
  category_dir <- switch(category,
    "connections" = RESEARCH_CONNECTIONS_DIR,
    "violations" = RESEARCH_VIOLATIONS_DIR,
    "anomalies" = RESEARCH_ANOMALIES_DIR,
    "evidence" = RESEARCH_EVIDENCE_DIR,
    "verification" = RESEARCH_VERIFICATION_DIR,
    "timelines" = RESEARCH_TIMELINES_DIR,
    "summaries" = RESEARCH_SUMMARIES_DIR,
    "search_results" = RESEARCH_SEARCH_RESULTS_DIR,
    RESEARCH_DIR  # Default fallback
  )

  file_path <- file.path(category_dir, filename)

  # Fallback: try old location
  if (!file.exists(file_path)) {
    old_path <- file.path(RESEARCH_DIR, filename)
    if (file.exists(old_path)) {
      return(old_path)
    }
  }

  return(file_path)
}

# Common research file shortcuts
get_entities_file <- function() {
  get_research_file("evidence", "all_entities_extracted.json")
}

get_evidence_summary_file <- function() {
  get_research_file("evidence", "all_evidence_summary.json")
}

get_connections_file <- function() {
  get_research_file("connections", "caitlin_skidmore_connections.json")
}

get_violations_file <- function() {
  get_research_file("violations", "all_violations_compiled.json")
}

get_anomalies_file <- function() {
  get_research_file("anomalies", "all_anomalies_consolidated.json")
}

get_verification_file <- function(type = "hyland") {
  filename <- switch(type,
    "hyland" = "hyland_verification.json",
    "kettler" = "kettler_verification.json",
    "skidmore" = "skidmore_firms_validation.json",
    paste0(type, "_verification.json")
  )
  get_research_file("verification", filename)
}
