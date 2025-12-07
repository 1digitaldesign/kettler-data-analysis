#!/usr/bin/env Rscript
# Search Virginia State Bar for Edward Hyland and Sean Curtin
# Check for unauthorized practice of law violations

library(jsonlite)
library(httr)
library(rvest)

# Configuration
if (file.exists("research/all_entities_extracted.json")) {
  PROJECT_ROOT <- getwd()
} else {
  current_dir <- getwd()
  while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
    current_dir <- dirname(current_dir)
  }
  PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()
}

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "virginia_bar_search_results.json")

# Search Virginia State Bar
search_virginia_bar <- function(name) {
  cat("Searching Virginia State Bar for:", name, "\n")

  # Virginia State Bar member directory URL
  base_url <- "https://www.vsb.org/site/members/member-directory"

  # Note: This would require form submission or API access
  # For now, return framework structure

  return(list(
    name = name,
    search_performed = FALSE,
    license_found = FALSE,
    note = "Requires manual search at https://www.vsb.org/site/members/member-directory",
    violation_if_no_license = if (name == "Edward Hyland") "Unauthorized Practice of Law (UPL)" else "None"
  ))
}

# Main search
main_search <- function() {
  cat("=== Virginia State Bar Search ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Search targets
  targets <- c("Edward Hyland", "Sean Curtin")

  results <- list()
  for (target in targets) {
    results[[target]] <- search_virginia_bar(target)
  }

  # Create output
  output <- list(
    search_date = as.character(Sys.Date()),
    searches = results,
    note = "Manual search required at Virginia State Bar website"
  )

  # Save results
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(output, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved results to:", OUTPUT_FILE, "\n")

  cat("\n=== Search Complete ===\n")
  cat("Note: Manual search required at https://www.vsb.org/site/members/member-directory\n")
}

# Run if executed as script
if (!interactive()) {
  main_search()
}
