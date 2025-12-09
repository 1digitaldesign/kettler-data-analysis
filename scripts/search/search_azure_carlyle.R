#!/usr/bin/env Rscript
# Search for Azure Carlyle LP entity information
# This is the owner listed in the lease agreement

library(jsonlite)
library(stringr)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_CONNECTIONS_DIR, "azure_carlyle_search.json")

# Search targets
ENTITY_NAME <- "Azure Carlyle LP"
RELATED_ENTITIES <- c(
  "Azure Carlyle",
  "Carlyle LP",
  "800 John Carlyle",
  "850 John Carlyle"
)

search_azure_carlyle <- function() {
  cat("=== Azure Carlyle LP Search ===\n")
  cat("Date:", Sys.Date(), "\n\n")
  cat("Entity:", ENTITY_NAME, "\n\n")

  results <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      entity = ENTITY_NAME,
      status = "framework"
    ),
    search_targets = RELATED_ENTITIES,
    searches = list(
      virginia_state_corporation_commission = list(
        url = "https://cis.scc.virginia.gov/EntitySearch",
        status = "framework",
        note = "Search Virginia SCC for entity registration"
      ),
      alexandria_business_licenses = list(
        url = "https://www.alexandriava.gov/business/",
        status = "framework",
        note = "Search Alexandria business license database"
      ),
      property_records = list(
        url = "https://www.alexandriava.gov/planning/",
        status = "framework",
        note = "Search Alexandria property records for 800 John Carlyle"
      ),
      sec_filings = list(
        url = "https://www.sec.gov/edgar/searchedgar/companysearch.html",
        status = "framework",
        note = "Search SEC filings for Azure Carlyle LP"
      )
    ),
    findings = list(
      connection_to_kettler = "Kettler Management listed as manager in lease",
      property_address = "800 John Carlyle Street",
      unit_number = "533",
      note = "Framework - requires actual database searches"
    )
  )

  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("Saved search framework to:", OUTPUT_FILE, "\n")

  return(results)
}

if (!interactive()) search_azure_carlyle()
