#!/usr/bin/env Rscript
# Verify business licenses for STR operations and Kettler Management in Alexandria

library(jsonlite)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "business_license_verification.json")

BUSINESS_LICENSE_URL <- "https://www.alexandriava.gov/business/info/default.aspx?id=106430"
ENTITIES_TO_CHECK <- c("Kettler Management Inc", "Kettler Management", "800 Carlyle LLC")

verify_business_licenses <- function() {
  cat("=== Business License Verification ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  results <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      jurisdiction = "Alexandria, VA",
      status = "framework"
    ),
    entities_checked = ENTITIES_TO_CHECK,
    verifications = list(),
    str_operator_licenses = list(
      note = "Framework - requires manual search of Alexandria business license database"
    )
  )

  for (entity in ENTITIES_TO_CHECK) {
    results$verifications[[entity]] <- list(
      entity = entity,
      license_found = NA,
      license_number = NA,
      expiration_date = NA,
      status = "framework"
    )
  }

  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("Saved results to:", OUTPUT_FILE, "\n")

  return(results)
}

if (!interactive()) verify_business_licenses()
