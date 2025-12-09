#!/usr/bin/env Rscript
# Scrape state bar associations for Edward Hyland and Sean Curtin
# UPL check for Hyland, General Counsel verification for Curtin

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
OUTPUT_FILE <- file.path(RESEARCH_VERIFICATION_DIR, "bar_association_verification_all.json")

# State bar association URLs (framework)
STATE_BAR_URLS <- list(
  VA = "https://www.vsb.org/site/members/member_lookup",
  TX = "https://www.texasbar.com/AM/Template.cfm?Section=Find_A_Lawyer",
  NC = "https://www.ncbar.gov/for-the-public/find-a-lawyer/",
  MD = "https://www.mdcourts.gov/attygrievance/attorneysearch",
  DC = "https://www.dcbar.org/bar-services/member-directory"
)

# Search bar association (framework)
search_bar_association <- function(name, state_code, url) {
  return(list(
    name = name,
    state = state_code,
    status = "framework",
    admitted = NA,
    bar_number = NA,
    admission_date = NA,
    note = "Framework - requires manual implementation per state"
  ))
}

# Main scraping function
scrape_all_bar_associations <- function() {
  cat("=== Bar Association Verification ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  targets <- list(
    hyland = list(name = "Edward Hyland", purpose = "UPL check"),
    curtin = list(name = "Sean Curtin", purpose = "General Counsel verification")
  )

  results <- list(
    metadata = list(date = as.character(Sys.Date()), status = "framework"),
    searches = list()
  )

  for (target_name in names(targets)) {
    target <- targets[[target_name]]
    cat("Searching for:", target$name, "\n")

    target_results <- list(
      individual = target$name,
      purpose = target$purpose,
      states = list()
    )

    for (state_code in names(STATE_BAR_URLS)) {
      url <- STATE_BAR_URLS[[state_code]]
      state_result <- search_bar_association(target$name, state_code, url)
      target_results$states[[state_code]] <- state_result
    }

    results$searches[[target_name]] <- target_results
  }

  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved results to:", OUTPUT_FILE, "\n")

  return(results)
}

if (!interactive()) scrape_all_bar_associations()
