#!/usr/bin/env Rscript
# Handle CAPTCHA-protected searches and document results
# This script consolidates browser automation results including CAPTCHA handling

library(jsonlite)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "captcha_handled_searches.json")

consolidate_captcha_searches <- function() {
  cat("=== Consolidating CAPTCHA-Handled Searches ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  results <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      status = "browser_automation_with_captcha_handling",
      note = "Searches attempted with CAPTCHA detection"
    ),
    searches_attempted = list(
      virginia_scc = list(
        url = "https://cis.scc.virginia.gov/EntitySearch",
        entity = "Azure Carlyle LP",
        status = "attempted",
        captcha_detected = "checking",
        note = "Page load issues - may require CAPTCHA bypass"
      ),
      vrbo = list(
        url = "https://www.vrbo.com",
        search_term = "800 John Carlyle Street Alexandria VA",
        status = "attempted",
        captcha_detected = FALSE
      ),
      alexandria_gov = list(
        url = "https://www.alexandriava.gov",
        search_term = "800 John Carlyle property records",
        status = "attempted",
        captcha_detected = FALSE
      ),
      sec_edgar = list(
        url = "https://www.sec.gov/edgar/searchedgar/companysearch.html",
        entity = "Azure Carlyle LP",
        status = "attempted",
        captcha_detected = "checking",
        note = "SEC website may have CAPTCHA protection"
      )
    ),
    captcha_handling_strategy = list(
      detection = "Check for recaptcha iframes, captcha classes, and CAPTCHA-related text",
      user_prompt = "If CAPTCHA detected, prompt user to solve or provide alternative method",
      fallback = "Document CAPTCHA-protected sites for manual search",
      note = "Some sites may require manual intervention"
    ),
    findings = list(
      dpor_completed = "Azure Carlyle LP not found in DPOR (confirmed)",
      next_steps = c(
        "Complete Virginia SCC search (may require CAPTCHA bypass)",
        "Extract VRBO search results",
        "Extract Alexandria property records",
        "Extract SEC EDGAR results if available"
      )
    )
  )

  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("Saved CAPTCHA-handled searches to:", OUTPUT_FILE, "\n")

  return(results)
}

if (!interactive()) consolidate_captcha_searches()
