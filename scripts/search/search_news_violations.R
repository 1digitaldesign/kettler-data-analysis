#!/usr/bin/env Rscript
# Search news databases for violations and complaints
# Framework for searching news sources

library(jsonlite)

# Configuration
if (file.exists("research/evidence/all_entities_extracted.json")) {
  PROJECT_ROOT <- getwd()
} else {
  current_dir <- getwd()
  while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
    current_dir <- dirname(current_dir)
  }
  PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()
}

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "news_violations_search.json")

# Search terms
get_search_terms <- function() {
  terms <- list(
    kettler = c(
      "Kettler Management violation",
      "Kettler Management complaint",
      "Kettler Management discrimination",
      "Kettler Management fraud",
      "Kettler Management unlicensed",
      "Kettler Management lawsuit",
      "Kettler Management settlement",
      "Kettler Management BBB",
      "Kettler Management tenant",
      "Kettler Management eviction"
    ),
    hyland = c(
      "Edward Hyland",
      "Edward Hyland Kettler",
      "Edward Hyland unlicensed"
    ),
    properties = c(
      "800 Carlyle violation",
      "800 Carlyle complaint",
      "Sinclaire Seminary violation"
    ),
    general = c(
      "Alexandria property management violation",
      "McLean property management complaint",
      "Virginia property management fraud"
    )
  )
  return(terms)
}

# News sources to search
get_news_sources <- function() {
  sources <- list(
    local = c(
      "Washington Post",
      "Washington City Paper",
      "Alexandria Times",
      "Northern Virginia Magazine",
      "Virginia Business"
    ),
    regional = c(
      "Richmond Times-Dispatch",
      "Virginia Pilot",
      "Roanoke Times"
    ),
    national = c(
      "New York Times",
      "Wall Street Journal",
      "USA Today"
    ),
    trade = c(
      "Multi-Housing News",
      "National Real Estate Investor",
      "Property Management Insider"
    )
  )
  return(sources)
}

# Main search function
main_search <- function() {
  cat("=== News Violations Search ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Get search terms
  terms <- get_search_terms()

  # Get news sources
  sources <- get_news_sources()

  # Create results structure
  results <- list(
    search_date = as.character(Sys.Date()),
    search_terms = terms,
    news_sources = sources,
    searches_performed = 0,
    violations_found = list(),
    note = "Framework for news database searches. Actual implementation requires API access or web scraping."
  )

  # Save results
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved results to:", OUTPUT_FILE, "\n")

  cat("\n=== Search Complete ===\n")
  cat("Note: This is a framework. Implement actual news searches.\n")
}

# Run if executed as script
if (!interactive()) {
  main_search()
}
