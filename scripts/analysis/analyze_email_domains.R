#!/usr/bin/env Rscript
# Extract and analyze all email domains from evidence files
# Identify domain ownership and cross-reference with firms

library(jsonlite)
library(dplyr)
library(stringr)

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
DATA_DIR <- file.path(PROJECT_ROOT, "data")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "email_domain_analysis.json")

# Extract email domains
extract_domains <- function(emails) {
  domains <- character(0)
  if (is.null(emails) || length(emails) == 0) {
    return(domains)
  }
  for (email in emails) {
    if (!is.null(email) && !is.na(email) && is.character(email) && grepl("@", email)) {
      domain <- str_extract(email, "@([^@]+)$")
      if (!is.na(domain)) {
        domain <- str_remove(domain, "^@")
        domains <- c(domains, domain)
      }
    }
  }
  return(unique(domains))
}

# Analyze email patterns
analyze_email_patterns <- function(emails) {
  patterns <- list()

  # Kettler emails
  kettler_emails <- grep("@kettler\\.com", emails, ignore.case = TRUE, value = TRUE)
  if (length(kettler_emails) > 0) {
    patterns$kettler <- list(
      count = length(kettler_emails),
      emails = unique(kettler_emails),
      patterns = list()
    )

    # Extract patterns (e.g., firstname.lastname@, property.pm@, etc.)
    for (email in kettler_emails) {
      local_part <- str_extract(email, "^[^@]+")
      if (!is.na(local_part)) {
        if (grepl("\\.", local_part)) {
          pattern <- "firstname.lastname"
        } else if (grepl("^[a-z]+$", local_part, ignore.case = TRUE)) {
          pattern <- "firstname"
        } else if (grepl("\\..*\\.", local_part)) {
          pattern <- "property.role"
        } else {
          pattern <- "other"
        }
        patterns$kettler$patterns[[length(patterns$kettler$patterns) + 1]] <- list(
          email = email,
          pattern = pattern
        )
      }
    }
  }

  return(patterns)
}

# Cross-reference with firms
cross_reference_firms <- function(domains, firms) {
  connections <- list()

  # Check kettler.com domain
  if ("kettler.com" %in% domains) {
    kettler_firm <- firms[firms$Firm.Name == "KETTLER MANAGEMENT INC", ]
    if (nrow(kettler_firm) > 0 && "License.Number" %in% names(kettler_firm)) {
      connections$kettler <- list(
        domain = "kettler.com",
        firm = "KETTLER MANAGEMENT INC",
        license_number = kettler_firm$License.Number[1],
        connection_type = "direct_match"
      )
    }
  }

  return(connections)
}

# Main analysis function
main_analysis <- function() {
  cat("=== Email Domain Analysis ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load entities
  entities_file <- file.path(RESEARCH_DIR, "all_entities_extracted.json")
  if (!file.exists(entities_file)) {
    stop("Entities file not found: ", entities_file)
  }
  entities <- fromJSON(entities_file, simplifyDataFrame = FALSE)

  # Load firms
  firms_file <- file.path(DATA_DIR, "source", "skidmore_all_firms_complete.csv")
  firms <- if (file.exists(firms_file)) {
    read.csv(firms_file, stringsAsFactors = FALSE)
  } else {
    data.frame()
  }

  # Extract domains
  cat("Extracting email domains...\n")
  domains <- extract_domains(entities$emails)
  cat("Found", length(domains), "unique domains\n")

  # Analyze patterns
  cat("Analyzing email patterns...\n")
  patterns <- analyze_email_patterns(entities$emails)

  # Cross-reference with firms
  cat("Cross-referencing with firms...\n")
  firm_connections <- cross_reference_firms(domains, firms)

  # Create results
  results <- list(
    analysis_date = as.character(Sys.Date()),
    total_emails = length(entities$emails),
    unique_domains = domains,
    domain_count = length(domains),
    email_patterns = patterns,
    firm_connections = firm_connections,
    summary = list(
      kettler_emails_found = ifelse(is.null(patterns$kettler$count), 0, patterns$kettler$count),
      domains_linked_to_firms = length(firm_connections)
    )
  )

  # Save results
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved results to:", OUTPUT_FILE, "\n")

  # Print summary
  cat("\n=== Analysis Summary ===\n")
  cat("Total Emails:", results$total_emails, "\n")
  cat("Unique Domains:", results$domain_count, "\n")
  cat("Kettler Emails Found:", results$summary$kettler_emails_found, "\n")
  cat("Domains Linked to Firms:", results$summary$domains_linked_to_firms, "\n")

  cat("\n=== Analysis Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  main_analysis()
}
