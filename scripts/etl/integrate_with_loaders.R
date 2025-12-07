#!/usr/bin/env Rscript
# Integration with Existing Data Loaders
# Wraps existing data loading functions to automatically trigger ETL

source(file.path(dirname(dirname(dirname(getwd()))), "scripts", "etl", "auto_etl_hook.R"))

# Enhanced load functions that trigger ETL
load_skidmore_data_with_etl <- function() {
  # Run ETL check before loading
  auto_run_etl(force = FALSE)

  # Load data using original function
  source("analyze_skidmore_connections.R")
  return(load_skidmore_data())
}

load_all_evidence_with_etl <- function() {
  # Run ETL check before loading
  auto_run_etl(force = FALSE)

  # Load evidence using original function
  source("scripts/analysis/analyze_all_evidence.R")
  return(load_all_evidence())
}

load_all_data_with_etl <- function() {
  # Run ETL check before loading
  auto_run_etl(force = FALSE)

  # Load data using original function
  source("organize_evidence.R")
  return(load_all_data())
}

# Export functions
cat("ETL-integrated loaders available:\n")
cat("  - load_skidmore_data_with_etl()\n")
cat("  - load_all_evidence_with_etl()\n")
cat("  - load_all_data_with_etl()\n")
