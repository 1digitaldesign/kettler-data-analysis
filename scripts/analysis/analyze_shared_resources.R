#!/usr/bin/env Rscript
# Analyze shared resources between firms
# Email domains, phone numbers, addresses, websites, bank accounts

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
OUTPUT_FILE <- file.path(RESEARCH_DIR, "shared_resources_analysis.json")

# Normalize addresses for comparison
normalize_address <- function(addr) {
  if (is.na(addr) || addr == "") return("")
  addr <- toupper(addr)
  addr <- str_replace_all(addr, "[#]", "STE")
  addr <- str_replace_all(addr, "\\bSTREET\\b", "ST")
  addr <- str_replace_all(addr, "\\bDRIVE\\b", "DR")
  addr <- str_replace_all(addr, "\\bROAD\\b", "RD")
  addr <- str_replace_all(addr, "\\bSUITE\\b", "STE")
  addr <- str_replace_all(addr, "[[:punct:]]", " ")
  addr <- str_replace_all(addr, "\\s+", " ")
  return(str_trim(addr))
}

# Find shared addresses
find_shared_addresses <- function(firms) {
  cat("\n=== Finding Shared Addresses ===\n")

  # Normalize all addresses
  firms$Address.Normalized <- sapply(firms$Address, normalize_address)

  # Count occurrences
  if ("Address.Normalized" %in% names(firms) && nrow(firms) > 0) {
    address_counts <- table(firms$Address.Normalized)
    shared_addresses <- address_counts[address_counts > 1]
  } else {
    address_counts <- table(character(0))
    shared_addresses <- address_counts[address_counts > 1]
  }

  shared_list <- list()
  if (length(shared_addresses) > 0) {
    for (addr in names(shared_addresses)) {
      firms_at_addr <- firms[firms$Address.Normalized == addr, ]
      shared_list[[length(shared_list) + 1]] <- list(
        address = addr,
        firm_count = as.numeric(shared_addresses[addr]),
        firms = firms_at_addr$Firm.Name
      )
    }
  }

  return(shared_list)
}

# Main analysis function
main_analysis <- function() {
  cat("=== Shared Resources Analysis ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load firms
  firms_file <- file.path(DATA_DIR, "source", "skidmore_all_firms_complete.csv")
  if (!file.exists(firms_file)) {
    stop("Firms file not found: ", firms_file)
  }
  firms <- read.csv(firms_file, stringsAsFactors = FALSE)

  # Load entities
  entities_file <- file.path(RESEARCH_DIR, "all_entities_extracted.json")
  entities <- if (file.exists(entities_file)) {
    fromJSON(entities_file, simplifyDataFrame = FALSE)
  } else {
    list(emails = character(0), phone_numbers = character(0))
  }

  # Find shared addresses
  shared_addresses <- find_shared_addresses(firms)

  # Analyze email domains
  if (!is.null(entities$emails) && length(entities$emails) > 0) {
    email_domains <- unique(str_extract(entities$emails, "@([^@]+)$"))
    email_domains <- email_domains[!is.na(email_domains)]
    if (length(email_domains) > 0) {
      email_domains <- str_remove(email_domains, "^@")
    } else {
      email_domains <- character(0)
    }
  } else {
    email_domains <- character(0)
  }

  # Create results
  results <- list(
    analysis_date = as.character(Sys.Date()),
    shared_addresses = shared_addresses,
    shared_address_count = length(shared_addresses),
    email_domains_found = unique(email_domains),
    summary = list(
      firms_sharing_addresses = length(shared_addresses),
      largest_address_cluster = if (length(shared_addresses) > 0) {
        max(sapply(shared_addresses, function(x) x$firm_count))
      } else 0
    )
  )

  # Save results
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved results to:", OUTPUT_FILE, "\n")

  # Print summary
  cat("\n=== Analysis Summary ===\n")
  cat("Shared Address Clusters:", results$shared_address_count, "\n")
  cat("Largest Cluster:", results$summary$largest_address_cluster, "firms\n")

  cat("\n=== Analysis Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  main_analysis()
}
