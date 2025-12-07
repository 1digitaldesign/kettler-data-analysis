#!/usr/bin/env Rscript
# DPOR License Search Script
# Searches Virginia DPOR and other state licensing databases for firm information

library(httr)
library(rvest)
library(dplyr)
library(jsonlite)
library(stringr)

# Firm names to search
firms <- c(
  "Bell Partners Inc",
  "Bozzuto Management Company",
  "Cortland Management LLC",
  "Gables Residential Services Inc",
  "Gateway Management Company LLC",
  "McCormack Baron Management Inc",
  "Burlington Capital Properties LLC",
  "Bainbridge Mid Atlantic Management LLC",
  "Capreit Residential Management LLC",
  "Edgewood Management Corporation"
)

# Clean firm names for search
clean_firm_name <- function(name) {
  name %>%
    str_remove_all("\\s+(Inc|LLC|Corporation|Company)$") %>%
    str_trim()
}

# Search Virginia DPOR
search_virginia_dpor <- function(firm_name) {
  base_url <- "https://www.dpor.virginia.gov/LicenseLookup"

  # Note: This is a placeholder - actual search would require form submission
  # or API access. Manual search may be needed.

  cat(sprintf("Searching Virginia DPOR for: %s\n", firm_name))

  # Return structure for results
  result <- list(
    firm_name = firm_name,
    state = "Virginia",
    search_url = base_url,
    notes = "Manual search required - DPOR website may require form submission"
  )

  return(result)
}

# Main search function
search_all_firms <- function(firms) {
  results <- list()

  for (firm in firms) {
    cat(sprintf("\n=== Searching for: %s ===\n", firm))

    # Search Virginia
    va_result <- search_virginia_dpor(firm)
    results[[length(results) + 1]] <- va_result

    # Add other states here as needed
  }

  return(results)
}

# Run searches
cat("Starting DPOR searches...\n")
search_results <- search_all_firms(firms)

# Save results
results_df <- bind_rows(search_results)
write.csv(results_df, "dpor_search_results.csv", row.names = FALSE)
cat("\nResults saved to dpor_search_results.csv\n")

# Print summary
cat("\n=== Search Summary ===\n")
print(results_df)
