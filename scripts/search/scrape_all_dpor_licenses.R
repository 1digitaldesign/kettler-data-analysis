#!/usr/bin/env Rscript
# Scrape DPOR databases across all 50 states for all individuals in management chain
# Framework for comprehensive license verification

library(jsonlite)
library(dplyr)
library(stringr)

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
OUTPUT_FILE <- file.path(RESEARCH_DIR, "dpor_license_verification_all.json")

# Load individuals to search
load_individuals <- function() {
  individuals_file <- file.path(RESEARCH_DIR, "all_individuals_identified.json")
  if (file.exists(individuals_file)) {
    data <- fromJSON(individuals_file)
    individuals <- unlist(lapply(data$individuals_identified, function(x) x$name))
    return(individuals)
  }

  # Fallback list
  return(c(
    "Edward Hyland", "Djene Moyer", "Henry Ramos", "Sean Curtin",
    "Caitlin Skidmore", "Robert C. Kettler", "Cindy Fisher",
    "Luke Davis", "Pat Cassada", "Amy Groff", "Robert Grealy"
  ))
}

# Load state registry
load_state_registry <- function() {
  registry_file <- file.path(PROJECT_ROOT, "state_dpor_registry.csv")
  if (file.exists(registry_file)) {
    return(read.csv(registry_file, stringsAsFactors = FALSE))
  }
  return(NULL)
}

# Search individual in state (framework)
search_individual_in_state <- function(individual_name, state_code, state_info) {
  return(list(
    individual = individual_name,
    state = state_code,
    status = "framework",
    licenses_found = 0,
    note = "Framework - requires manual implementation per state"
  ))
}

# Main scraping function
scrape_all_dpor_licenses <- function() {
  cat("=== DPOR License Verification - All States ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  individuals <- load_individuals()
  registry <- load_state_registry()

  if (is.null(registry)) {
    cat("ERROR: State registry not found\n")
    return(NULL)
  }

  if (nrow(registry) == 0) {
    cat("ERROR: State registry is empty\n")
    return(NULL)
  }

  cat("Loaded", length(individuals), "individuals\n")
  cat("Loaded", nrow(registry), "states\n\n")

  results <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      total_individuals = length(individuals),
      total_states = nrow(registry),
      status = "framework"
    ),
    searches = list()
  )

  # For each individual, search all states
  for (i in seq_along(individuals)) {
    individual <- individuals[i]
    cat("[", i, "/", length(individuals), "] Searching for:", individual, "\n")

    individual_results <- list(
      individual = individual,
      states = list()
    )

    # Search each state
    for (j in 1:nrow(registry)) {
      state_info <- registry[j, ]
      state_result <- search_individual_in_state(individual, state_info$state_code, state_info)
      individual_results$states[[state_info$state_code]] <- state_result
    }

    results$searches[[individual]] <- individual_results
  }

  # Save results
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved results to:", OUTPUT_FILE, "\n")

  return(results)
}

if (!interactive()) scrape_all_dpor_licenses()
