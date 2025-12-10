#!/usr/bin/env Rscript
# Search for Lariat Realty Advisors connections among affiliated companies

library(jsonlite)

# Load affiliated companies
companies_file <- "research/lariat_affiliated_companies.json"
companies_data <- fromJSON(companies_file)
companies_list <- companies_data$affiliated_companies

cat("=== Lariat Affiliated Companies Investigation ===\n\n")
cat(sprintf("Total companies: %d\n\n", length(companies_list)))

# Create output directory
output_dir <- "research/lariat_company_investigations"
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# Process each company
investigations <- list()

for (i in seq_along(companies_list)) {
  company <- companies_list[[i]]
  company_name <- company$name

  cat(sprintf("%d/%d: %s\n", i, length(companies_list), company_name))

  # Create investigation record
  investigation <- list(
    company_name = company_name,
    search_date = as.character(Sys.Date()),
    search_method = "web_search_and_browser_automation",
    findings = list(
      lariat_connection = "pending_browser_search",
      website_url = "pending",
      state_licenses = "pending",
      shared_addresses = "pending",
      shared_contacts = "pending",
      notes = company$note %||% ""
    )
  )

  # Save investigation file
  safe_name <- tolower(gsub("[^a-z0-9]", "_", company_name))
  safe_name <- gsub("_{2,}", "_", safe_name)
  safe_name <- gsub("^_|_$", "", safe_name)

  output_file <- file.path(output_dir, paste0(safe_name, "_investigation.json"))

  tryCatch({
    write_json(investigation, output_file, pretty = TRUE, auto_unbox = TRUE)
    cat(sprintf("  ✓ Created: %s\n", basename(output_file)))
    investigations[[company_name]] <- investigation
  }, error = function(e) {
    cat(sprintf("  ✗ Error creating file: %s\n", e$message))
  })
}

# Save summary
summary_file <- file.path(output_dir, "investigation_summary.json")
summary <- list(
  metadata = list(
    date = as.character(Sys.Date()),
    total_companies = length(companies_list),
    investigation_status = "framework_created"
  ),
  companies = companies_list,
  investigations_created = length(investigations)
)

tryCatch({
  write_json(summary, summary_file, pretty = TRUE, auto_unbox = TRUE)
  cat(sprintf("\n✓ Summary saved to: %s\n", summary_file))
}, error = function(e) {
  cat(sprintf("\n✗ Error saving summary: %s\n", e$message))
})

cat(sprintf("\n=== Framework Created ===\n"))
cat(sprintf("Investigation files created: %d\n", length(investigations)))
cat("\nNext step: Use browser automation to search each company\n")
