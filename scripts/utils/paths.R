#!/usr/bin/env Rscript
# Path Utilities
# Centralized path management for the project

# Get project root directory
# This function searches upward from current directory to find project root
get_project_root <- function() {
  current_dir <- getwd()
  max_depth <- 10
  depth <- 0

  while (depth < max_depth) {
    # Check for project root indicators
    has_readme <- file.exists(file.path(current_dir, "README.md"))
    has_bin <- file.exists(file.path(current_dir, "bin"))
    has_scripts <- file.exists(file.path(current_dir, "scripts"))
    has_data <- file.exists(file.path(current_dir, "data"))

    if (has_readme && has_bin && has_scripts && has_data) {
      return(normalizePath(current_dir))
    }

    parent_dir <- dirname(current_dir)
    if (parent_dir == current_dir) {
      break  # Reached filesystem root
    }
    current_dir <- parent_dir
    depth <- depth + 1
  }

  # Fallback: return current directory
  return(normalizePath(getwd()))
}

# Set project root
PROJECT_ROOT <- get_project_root()

# Directory paths
DATA_DIR <- file.path(PROJECT_ROOT, "data")
RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
EVIDENCE_DIR <- file.path(PROJECT_ROOT, "evidence")
FILINGS_DIR <- file.path(PROJECT_ROOT, "filings")
SCRIPTS_DIR <- file.path(PROJECT_ROOT, "scripts")
BIN_DIR <- file.path(PROJECT_ROOT, "bin")
CONFIG_DIR <- file.path(PROJECT_ROOT, "config")
OUTPUTS_DIR <- file.path(PROJECT_ROOT, "outputs")

# Data subdirectories
DATA_SOURCE_DIR <- file.path(DATA_DIR, "source")
DATA_RAW_DIR <- file.path(DATA_DIR, "raw")
DATA_CLEANED_DIR <- file.path(DATA_DIR, "cleaned")
DATA_ANALYSIS_DIR <- file.path(DATA_DIR, "analysis")
DATA_SCRAPED_DIR <- file.path(DATA_DIR, "scraped")
DATA_VECTORS_DIR <- file.path(DATA_DIR, "vectors")

# Research subdirectories
RESEARCH_CONNECTIONS_DIR <- file.path(RESEARCH_DIR, "connections")
RESEARCH_VIOLATIONS_DIR <- file.path(RESEARCH_DIR, "violations")
RESEARCH_ANOMALIES_DIR <- file.path(RESEARCH_DIR, "anomalies")
RESEARCH_EVIDENCE_DIR <- file.path(RESEARCH_DIR, "evidence")
RESEARCH_VERIFICATION_DIR <- file.path(RESEARCH_DIR, "verification")
RESEARCH_TIMELINES_DIR <- file.path(RESEARCH_DIR, "timelines")
RESEARCH_SUMMARIES_DIR <- file.path(RESEARCH_DIR, "summaries")
RESEARCH_SEARCH_RESULTS_DIR <- file.path(RESEARCH_DIR, "search_results")

# Config files
STATE_REGISTRY_FILE <- file.path(CONFIG_DIR, "state_dpor_registry.csv")

# Helper function to source scripts
source_script <- function(script_path) {
  full_path <- file.path(SCRIPTS_DIR, script_path)
  if (file.exists(full_path)) {
    source(full_path)
  } else {
    stop(paste("Script not found:", full_path))
  }
}

# Helper function to source bin scripts
source_bin <- function(script_name) {
  full_path <- file.path(BIN_DIR, script_name)
  if (file.exists(full_path)) {
    source(full_path)
  } else {
    stop(paste("Bin script not found:", full_path))
  }
}
