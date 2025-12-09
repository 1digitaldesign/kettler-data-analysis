#!/usr/bin/env Rscript
# Search for Edward Hyland licenses across all 50 states
# Uses state_dpor_registry.csv to search each state's DPOR database

library(httr)
library(rvest)
library(dplyr)
library(jsonlite)
library(stringr)

# Configuration
if (file.exists("config/state_dpor_registry.csv")) {
  PROJECT_ROOT <- getwd()
} else if (file.exists("../state_dpor_registry.csv")) {
  PROJECT_ROOT <- normalizePath("..")
} else {
  current_dir <- getwd()
  while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
    current_dir <- dirname(current_dir)
  }
  PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()
}

REGISTRY_FILE <- file.path(PROJECT_ROOT, "config/state_dpor_registry.csv")
OUTPUT_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(OUTPUT_DIR, "hyland_license_search_all_states.json")

# Load state registry
load_state_registry <- function() {
  if (!file.exists(REGISTRY_FILE)) {
    stop("State registry file not found: ", REGISTRY_FILE)
  }
  return(read.csv(REGISTRY_FILE, stringsAsFactors = FALSE))
}

# Search terms for Edward Hyland
SEARCH_TERMS <- c("Edward Hyland", "Ed Hyland", "E. Hyland", "Edward J. Hyland")

# Generic search function (simplified - actual implementation would need state-specific logic)
search_state_dpor <- function(state_code, state_name, search_url, search_term) {
  cat("  Searching", state_name, "for:", search_term, "\n")

  # Note: This is a placeholder. Actual implementation would need to:
  # 1. Handle different search types (form_based vs query_based)
  # 2. Parse each state's specific form structure
  # 3. Handle authentication/captchas if needed
  # 4. Parse results appropriately

  # For now, return "not_found" as most states would require manual verification
  # In a production system, this would call state-specific search functions

  return(list(
    state = state_code,
    state_name = state_name,
    search_term = search_term,
    status = "not_searched",
    note = "Automated search not implemented - requires manual verification or state-specific implementation"
  ))
}

# Main search function
main_search <- function() {
  cat("=== Edward Hyland Multi-State License Search ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load state registry
  registry <- load_state_registry()
  cat("Loaded", nrow(registry), "states\n\n")

  if (nrow(registry) == 0) {
    cat("ERROR: State registry is empty\n")
    return(list(
      search_date = as.character(Sys.Date()),
      search_terms = SEARCH_TERMS,
      states_searched = list(),
      summary = list(
        total_states = 0,
        states_searched = 0,
        licenses_found = 0,
        no_license_found = 0,
        not_searched = 0,
        error = "Registry is empty"
      )
    ))
  }

  # Initialize results
  results <- list(
    search_date = as.character(Sys.Date()),
    search_terms = SEARCH_TERMS,
    states_searched = list(),
    summary = list(
      total_states = nrow(registry),
      states_searched = 0,
      licenses_found = 0,
      no_license_found = 0,
      not_searched = 0
    )
  )

  # Search each state
  for (i in 1:nrow(registry)) {
    state_code <- registry$state_code[i]
    state_name <- registry$state[i]
    search_url <- registry$license_lookup_url[i]

    cat("State", i, "of", nrow(registry), ":", state_name, "\n")

    state_results <- list()

    # Search with each search term
    for (term in SEARCH_TERMS) {
      result <- search_state_dpor(state_code, state_name, search_url, term)
      state_results[[length(state_results) + 1]] <- result
    }

    # Determine overall status for state
    statuses <- sapply(state_results, function(x) x$status)
    if (any(statuses == "found")) {
      results$summary$licenses_found <- results$summary$licenses_found + 1
      overall_status <- "found"
    } else if (all(statuses == "not_found")) {
      results$summary$no_license_found <- results$summary$no_license_found + 1
      overall_status <- "not_found"
    } else {
      results$summary$not_searched <- results$summary$not_searched + 1
      overall_status <- "not_searched"
    }

    results$states_searched[[state_code]] <- list(
      state_code = state_code,
      state_name = state_name,
      search_url = search_url,
      overall_status = overall_status,
      searches = state_results
    )

    results$summary$states_searched <- results$summary$states_searched + 1

    # Rate limiting
    Sys.sleep(0.5)
  }

  # Save results
  dir.create(OUTPUT_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved results to:", OUTPUT_FILE, "\n")

  # Print summary
  cat("\n=== Search Summary ===\n")
  cat("Total States:", results$summary$total_states, "\n")
  cat("States Searched:", results$summary$states_searched, "\n")
  cat("Licenses Found:", results$summary$licenses_found, "\n")
  cat("No License Found:", results$summary$no_license_found, "\n")
  cat("Not Searched:", results$summary$not_searched, "\n")

  cat("\n=== Search Complete ===\n")
  cat("\nNOTE: This script provides a framework for multi-state searching.\n")
  cat("Actual implementation requires state-specific search logic for each DPOR website.\n")
  cat("For now, manual verification is recommended for definitive results.\n")
}

# Run if executed as script
if (!interactive()) {
  main_search()
}
