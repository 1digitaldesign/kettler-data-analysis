#!/usr/bin/env Rscript
# Chat Data Hook
# Automatically runs ETL when data is accessed in a chat session
# This should be sourced at the beginning of any analysis script

# Configuration
PROJECT_ROOT <- getwd()
if (basename(PROJECT_ROOT) != "kettler-data-analysis") {
  PROJECT_ROOT <- dirname(dirname(PROJECT_ROOT))
}

# Source auto ETL hook
source(file.path(PROJECT_ROOT, "scripts", "etl", "auto_etl_hook.R"))

# Override common data loading functions to trigger ETL
if (!exists("original_read.csv")) {
  original_read.csv <- read.csv
  original_fromJSON <- fromJSON

  # Enhanced read.csv
  read.csv <- function(file, ...) {
    if (is.character(file) && file.exists(file)) {
      run_etl_for_file(file)
    }
    return(original_read.csv(file, ...))
  }

  # Enhanced fromJSON
  fromJSON <- function(txt, ...) {
    # If txt is a file path, trigger ETL
    if (is.character(txt) && length(txt) == 1 && file.exists(txt)) {
      run_etl_for_file(txt)
    }
    return(original_fromJSON(txt, ...))
  }

  cat("Chat data hook activated. ETL will run automatically when data is loaded.\n")
}

# Run initial ETL check
auto_run_etl(force = FALSE)
