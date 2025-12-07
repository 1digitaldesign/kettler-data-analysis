#!/usr/bin/env Rscript
# Auto ETL Hook
# Automatically runs ETL pipeline when data is accessed
# Integrates with existing data loading functions

library(jsonlite)

# Configuration
PROJECT_ROOT <- getwd()
if (basename(PROJECT_ROOT) != "kettler-data-analysis") {
  PROJECT_ROOT <- dirname(dirname(PROJECT_ROOT))
}

VECTOR_DIR <- file.path(PROJECT_ROOT, "data", "vectors")
LAST_RUN_FILE <- file.path(VECTOR_DIR, "last_etl_run.json")

# Check if ETL needs to run
check_etl_needed <- function(file_path) {
  # Check if file exists
  if (!file.exists(file_path)) {
    return(FALSE)
  }

  # Check if ETL has run recently (within last hour)
  if (file.exists(LAST_RUN_FILE)) {
    tryCatch({
      last_run <- fromJSON(LAST_RUN_FILE)
      last_time <- as.POSIXct(last_run$timestamp)
      time_diff <- difftime(Sys.time(), last_time, units = "hours")

      if (as.numeric(time_diff) < 1) {
        return(FALSE)  # Ran recently, skip
      }
    }, error = function(e) {
      # If error reading, run ETL
      return(TRUE)
    })
  }

  # Check if file has been processed
  processed_file <- file.path(VECTOR_DIR, "processed_files.json")
  if (file.exists(processed_file)) {
    tryCatch({
      processed <- fromJSON(processed_file)
      file_str <- normalizePath(file_path)

      if (file_str %in% processed) {
        # Check if file was modified after processing
        file_mtime <- file.info(file_path)$mtime
        # We don't track modification times, so assume it needs processing
        # if it's a new file or we're not sure
        return(TRUE)
      }
    }, error = function(e) {
      return(TRUE)
    })
  }

  return(TRUE)
}

# Run ETL for a specific file
run_etl_for_file <- function(file_path) {
  if (!check_etl_needed(file_path)) {
    return(invisible(NULL))
  }

  cat("Running ETL for:", file_path, "\n")

  # Call Python ETL pipeline
  python_cmd <- if (system("which python3 > /dev/null 2>&1", ignore.stdout = TRUE, ignore.stderr = TRUE) == 0) {
    "python3"
  } else {
    "python"
  }

  etl_script <- file.path(PROJECT_ROOT, "scripts", "etl", "etl_pipeline.py")

  # Run incremental ETL
  system_result <- system(
    paste(python_cmd, etl_script, "--file", shQuote(file_path)),
    intern = TRUE,
    ignore.stdout = TRUE,
    ignore.stderr = TRUE
  )

  # Update last run time
  last_run <- list(
    timestamp = as.character(Sys.time()),
    file = file_path
  )
  write_json(last_run, LAST_RUN_FILE)
}

# Wrapper for read.csv that triggers ETL
read_csv_with_etl <- function(file, ...) {
  run_etl_for_file(file)
  return(read.csv(file, ...))
}

# Wrapper for fromJSON that triggers ETL
from_json_with_etl <- function(file, ...) {
  run_etl_for_file(file)
  return(fromJSON(file, ...))
}

# Hook into existing load functions
hook_data_loading <- function() {
  # This function can be called to set up hooks
  # For now, we'll use explicit wrappers
  cat("Data loading hooks available. Use read_csv_with_etl() or from_json_with_etl()\n")
}

# Auto-run ETL on startup if needed
auto_run_etl <- function(force = FALSE) {
  if (force) {
    cat("Running full ETL pipeline...\n")
    python_cmd <- if (system("which python3 > /dev/null 2>&1", ignore.stdout = TRUE, ignore.stderr = TRUE) == 0) {
      "python3"
    } else {
      "python"
    }

    etl_script <- file.path(PROJECT_ROOT, "scripts", "etl", "etl_pipeline.py")
    system(paste(python_cmd, etl_script))

    # Update last run time
    last_run <- list(
      timestamp = as.character(Sys.time()),
      type = "full"
    )
    write_json(last_run, LAST_RUN_FILE)
  } else {
    # Check if ETL needs to run
    last_run_file <- LAST_RUN_FILE
    if (!file.exists(last_run_file)) {
      cat("ETL has never run. Running initial ETL pipeline...\n")
      auto_run_etl(force = TRUE)
    }
  }
}

# Export functions
if (!interactive()) {
  # If run as script, check if ETL needs to run
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) > 0 && args[1] == "auto") {
    auto_run_etl(force = FALSE)
  } else if (length(args) > 0 && args[1] == "force") {
    auto_run_etl(force = TRUE)
  }
}
