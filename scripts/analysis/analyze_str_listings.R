#!/usr/bin/env Rscript
# Analyze all scraped STR listings: consolidate, identify units, count violations, match with building

library(jsonlite)
library(dplyr)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

DATA_DIR <- file.path(PROJECT_ROOT, "data", "scraped")
RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "str_listings_analysis.json")

analyze_str_listings <- function() {
  cat("=== STR Listings Analysis ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load all scraped listings
  listing_files <- c(
    "airbnb_listings_john_carlyle.json",
    "vrbo_listings_john_carlyle.json",
    "front_website_listings.json",
    "additional_str_listings.json"
  )

  all_listings <- list()

  for (file in listing_files) {
    file_path <- file.path(DATA_DIR, file)
    if (file.exists(file_path)) {
      data <- fromJSON(file_path)
      all_listings[[file]] <- data
    }
  }

  results <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      platforms_analyzed = length(all_listings),
      status = "framework"
    ),
    consolidated_listings = list(),
    unit_identification = list(
      total_listings = 0,
      unique_units = list(),
      note = "Framework - requires listing data to analyze"
    ),
    violations = list(
      unregistered_strs = 0,
      note = "Framework - requires listing data to count violations"
    ),
    building_match = list(
      matched_to_800_carlyle = 0,
      matched_to_850_carlyle = 0,
      note = "Framework - requires listing data to match"
    )
  )

  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("Saved results to:", OUTPUT_FILE, "\n")

  return(results)
}

if (!interactive()) analyze_str_listings()
