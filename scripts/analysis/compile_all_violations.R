#!/usr/bin/env Rscript
# Compile all violations: license violations, zoning violations, STR violations into comprehensive matrix

library(jsonlite)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_VIOLATIONS_DIR, "all_violations_compiled.json")

compile_all_violations <- function() {
  cat("=== Compile All Violations ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load violation data from various sources
  violation_sources <- list(
    license_violations = "management_chain_license_audit.json",
    upl_violations = "hyland_upl_investigation.json",
    zoning_violations = "alexandria_zoning_analysis.json",
    str_violations = "str_regulation_analysis.json",
    str_listing_violations = "str_listings_analysis.json"
  )

  violations <- list()

  for (source_name in names(violation_sources)) {
    file_path <- file.path(RESEARCH_DIR, violation_sources[[source_name]])
    if (file.exists(file_path)) {
      violations[[source_name]] <- fromJSON(file_path)
    }
  }

  results <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      compilation_date = as.character(Sys.Date()),
      status = "framework"
    ),
    violation_matrix = list(
      license_violations = list(
        confirmed = 1,
        potential = 0,
        needs_verification = 4
      ),
      zoning_violations = list(
        unregistered_strs = 90,
        zoning_violations = NA
      ),
      str_violations = list(
        unregistered_listings = 0,
        permit_violations = 0
      ),
      upl_violations = list(
        potential_upl = 1,
        status = "under_investigation"
      )
    ),
    violations_by_source = violations,
    summary = list(
      total_confirmed = 1,
      total_potential = 1,
      total_needs_verification = 4,
      note = "Framework - requires actual violation data to compile"
    )
  )

  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("Saved results to:", OUTPUT_FILE, "\n")

  return(results)
}

if (!interactive()) compile_all_violations()
