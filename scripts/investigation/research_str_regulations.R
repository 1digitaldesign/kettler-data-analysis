#!/usr/bin/env Rscript
# Research and document Alexandria STR regulations (effective Sep 1, 2025)

library(jsonlite)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "str_regulation_analysis.json")

research_str_regulations <- function() {
  cat("=== STR Regulation Research ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  results <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      jurisdiction = "Alexandria, VA",
      effective_date = "2025-09-01",
      status = "framework"
    ),
    regulations = list(
      permit_required = TRUE,
      permit_application_url = "https://www.alexandriava.gov/planning/info/default.aspx?id=106430",
      max_units_permit = NA,
      violations_estimated = 90,
      note = "Framework - requires manual research of Alexandria STR ordinance"
    ),
    violations = list(
      unregistered_strs = list(
        count = 90,
        note = "Estimated from evidence - requires verification"
      )
    )
  )

  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("Saved results to:", OUTPUT_FILE, "\n")

  return(results)
}

if (!interactive()) research_str_regulations()
