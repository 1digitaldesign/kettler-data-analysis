#!/usr/bin/env Rscript
# Search for Lariat Realty Advisors connections among affiliated companies

library(jsonlite)
library(dplyr)

# Load affiliated companies
companies_file <- "research/lariat_affiliated_companies.json"
if (!file.exists(companies_file)) {
  stop(sprintf("Companies file not found: %s", companies_file))
}

companies_data <- fromJSON(companies_file)
companies <- companies_data$affiliated_companies

cat("=== Searching Lariat Connections for Affiliated Companies ===\n\n")
cat(sprintf("Total companies to investigate: %d\n\n", length(companies)))

# Create output directory
output_dir <- "research/lariat_company_investigations"
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# Search results storage
search_results <- list()

for (i in seq_along(companies)) {
  company <- companies[[i]]
  company_name <- if (is.list(company) && "name" %in% names(company)) {
    company$name
  } else if (is.character(company)) {
    company
  } else {
    as.character(company)
  }

  cat(sprintf("Processing %d/%d: %s\n", i, length(companies), company_name))

  # Create investigation record
  investigation <- list(
    company_name = company_name,
    search_date = Sys.Date(),
    search_method = "web_search_and_browser_automation",
    findings = list()
  )

  # Note: Actual web searches would be done via browser automation
  # This creates the framework for investigation
  investigation$findings$lariat_connection <- "pending_browser_search"
  investigation$findings$website_url <- "pending"
  investigation$findings$state_licenses <- "pending"
  investigation$findings$shared_addresses <- "pending"
  investigation$findings$shared_contacts <- "pending"

  # Save investigation file
  safe_name <- tolower(gsub("[^a-z0-9]", "_", company_name))
  safe_name <- gsub("_{2,}", "_", safe_name)
  safe_name <- gsub("^_|_$", "", safe_name)

  output_file <- file.path(output_dir, paste0(safe_name, "_investigation.json"))
  write_json(investigation, output_file, pretty = TRUE, auto_unbox = TRUE)

  search_results[[company_name]] <- investigation

  cat(sprintf("  Created investigation file: %s\n", basename(output_file)))
}

# Save summary
summary_file <- file.path(output_dir, "investigation_summary.json")
summary <- list(
  metadata = list(
    date = Sys.Date(),
    total_companies = length(companies),
    investigation_status = "framework_created"
  ),
  companies = companies,
  search_results = search_results
)

write_json(summary, summary_file, pretty = TRUE, auto_unbox = TRUE)

cat(sprintf("\n=== Framework Created ===\n"))
cat(sprintf("Investigation files created: %d\n", length(companies)))
cat(sprintf("Summary saved to: %s\n", summary_file))
cat("\nNext step: Use browser automation to search each company\n")
