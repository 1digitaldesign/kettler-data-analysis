#!/usr/bin/env Rscript
# Check Alexandria zoning database and STR permit requirements for 800 John Carlyle

library(jsonlite)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "alexandria_zoning_analysis.json")

# Alexandria zoning URLs
ALEXANDRIA_ZONING_URLS <- list(
  zoning_database = "https://www.alexandriava.gov/planning/info/default.aspx?id=106430",
  str_permit_database = "https://www.alexandriava.gov/planning/info/default.aspx?id=106430",
  property_search = "https://www.alexandriava.gov/planning/info/default.aspx?id=106430"
)

PROPERTY_ADDRESS <- "800 John Carlyle Street, Alexandria, VA 22314"

check_alexandria_zoning <- function() {
  cat("=== Alexandria Zoning Analysis ===\n")
  cat("Date:", Sys.Date(), "\n\n")
  cat("Property:", PROPERTY_ADDRESS, "\n\n")

  results <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      property = PROPERTY_ADDRESS,
      status = "framework"
    ),
    zoning_check = list(
      zoning_classification = NA,
      str_permitted = NA,
      str_permits_found = list(),
      violations = list(),
      note = "Framework - requires manual search of Alexandria zoning database"
    ),
    urls = ALEXANDRIA_ZONING_URLS
  )

  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("Saved results to:", OUTPUT_FILE, "\n")

  return(results)
}

if (!interactive()) check_alexandria_zoning()
