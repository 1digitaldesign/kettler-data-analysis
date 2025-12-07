#!/usr/bin/env Rscript
# Verify property management licenses for Moyer, Ramos, and other operational staff

library(jsonlite)

# Configuration
current_dir <- getwd()
if (file.exists(file.path(current_dir, "research", "all_individuals_identified.json"))) {
  PROJECT_ROOT <- current_dir
} else {
  while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
    current_dir <- dirname(current_dir)
  }
  PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()
}

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "property_management_license_verification.json")

PROPERTY_MANAGEMENT_STATES <- c("VA", "TX", "NC", "MO", "NE", "MD")
PROPERTY_MANAGEMENT_TARGETS <- c("Djene Moyer", "Henry Ramos")

PROPERTY_MANAGEMENT_URLS <- list(
  VA = "https://www.dpor.virginia.gov/LicenseLookup",
  TX = "https://www.tdlr.texas.gov/",
  NC = "https://www.ncrec.gov/",
  MO = "https://pr.mo.gov/",
  NE = "https://nrec.ne.gov/",
  MD = "https://www.dllr.state.md.us/"
)

search_property_management_license <- function(name, state_code, url) {
  return(list(
    name = name,
    state = state_code,
    status = "framework",
    license_found = NA,
    note = "Framework - requires manual implementation per state"
  ))
}

verify_property_management_licenses <- function() {
  cat("=== Property Management License Verification ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  results <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      targets = PROPERTY_MANAGEMENT_TARGETS,
      states = PROPERTY_MANAGEMENT_STATES,
      status = "framework"
    ),
    verifications = list()
  )

  for (target_name in PROPERTY_MANAGEMENT_TARGETS) {
    cat("Verifying:", target_name, "\n")

    target_results <- list(
      individual = target_name,
      states = list()
    )

    for (state_code in PROPERTY_MANAGEMENT_STATES) {
      url <- PROPERTY_MANAGEMENT_URLS[[state_code]]
      if (!is.null(url)) {
        state_result <- search_property_management_license(target_name, state_code, url)
        target_results$states[[state_code]] <- state_result
      }
    }

    results$verifications[[target_name]] <- target_results
  }

  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved results to:", OUTPUT_FILE, "\n")

  return(results)
}

if (!interactive()) verify_property_management_licenses()
