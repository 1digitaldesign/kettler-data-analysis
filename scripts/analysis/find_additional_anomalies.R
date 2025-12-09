#!/usr/bin/env Rscript
# Find additional anomalies beyond initial analysis
# Look for patterns, inconsistencies, and hidden connections

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

DATA_DIR <- file.path(PROJECT_ROOT, "data")
RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "additional_anomalies.json")

# Load firms data
load_firms <- function() {
  firms_file <- file.path(DATA_DIR, "source", "skidmore_all_firms_complete.csv")
  if (!file.exists(firms_file)) {
    stop("Firms file not found: ", firms_file)
  }
  return(read.csv(firms_file, stringsAsFactors = FALSE))
}

# Find additional anomalies
find_anomalies <- function(firms) {
  cat("\n=== Finding Additional Anomalies ===\n")

  anomalies <- list()

  # Anomaly: License number patterns
  license_prefixes <- character(0)  # Initialize before conditional block
  if ("License.Number" %in% names(firms) && nrow(firms) > 0) {
    license_numbers <- firms$License.Number
    license_numbers <- license_numbers[!is.na(license_numbers) & license_numbers != ""]
    if (length(license_numbers) > 0) {
      license_prefixes <- substr(license_numbers, 1, 3)
      prefix_counts <- table(license_prefixes)
    } else {
      prefix_counts <- table(character(0))
    }
  } else {
    prefix_counts <- table(character(0))
  }

  # Check if licenses are sequential or clustered
  anomalies$license_patterns <- list(
    unique_prefixes = length(unique(license_prefixes)),
    prefix_distribution = as.list(prefix_counts),
    anomaly_type = "license_number_clustering",
    explanation = "License numbers may reveal registration patterns or timing"
  )

  # Anomaly: Firm type distribution
  firm_types <- table(firms$Firm.Type)
  llc_val <- if ("LLC" %in% names(firm_types)) firm_types["LLC"] else 0
  corp_val <- if ("Corporation" %in% names(firm_types)) firm_types["Corporation"] else 0
  anomalies$firm_type_distribution <- list(
    types = as.list(firm_types),
    llc_count = ifelse(is.na(llc_val), 0, as.numeric(llc_val)),
    corporation_count = ifelse(is.na(corp_val), 0, as.numeric(corp_val)),
    anomaly_type = "entity_type_pattern",
    explanation = "Mix of LLCs and Corporations may indicate different purposes"
  )

  # Anomaly: Expiration date clustering
  expiration_years <- character(0)  # Initialize before conditional block
  if ("Expiration.Date" %in% names(firms) && nrow(firms) > 0) {
    expiration_dates <- firms$Expiration.Date
    expiration_dates <- expiration_dates[!is.na(expiration_dates) & expiration_dates != ""]
    if (length(expiration_dates) > 0) {
      expiration_years <- substr(expiration_dates, 1, 4)
      year_counts <- table(expiration_years)
    } else {
      year_counts <- table(character(0))
    }
  } else {
    year_counts <- table(character(0))
  }

  anomalies$expiration_clustering <- list(
    unique_years = length(unique(expiration_years)),
    year_distribution = as.list(year_counts),
    anomaly_type = "coordinated_renewal",
    explanation = "Clustered expiration dates may indicate coordinated management"
  )

  # Anomaly: State distribution analysis
  states <- character(0)  # Initialize before conditional block
  if ("Address" %in% names(firms) && nrow(firms) > 0) {
    states <- str_extract(firms$Address, ",\\s*([A-Z]{2})\\s*\\d")
    states <- str_extract(states, "[A-Z]{2}")
    states <- states[!is.na(states)]
    if (length(states) > 0) {
      state_counts <- table(states)
    } else {
      state_counts <- table(character(0))
    }
  } else {
    state_counts <- table(character(0))
  }

  anomalies$state_distribution <- list(
    state_count = length(unique(states)),
    states = as.list(state_counts),
    anomaly_type = "geographic_pattern",
    explanation = "State distribution may reveal operational strategy"
  )

  # Anomaly: Address variations for same location
  # Check Frisco address variations
  frisco_firms <- firms[grepl("5729.*LEBANON|LEBANON.*5729", firms$Address, ignore.case = TRUE) &
                        grepl("FRISCO.*TX.*75034", firms$Address, ignore.case = TRUE), ]

  if (nrow(frisco_firms) > 0) {
    address_variations <- unique(frisco_firms$Address)
    anomalies$frisco_address_variations <- list(
      variation_count = length(address_variations),
      variations = address_variations,
      anomaly_type = "address_inconsistency",
      explanation = "Same location with different address formats may indicate data manipulation"
    )
  }

  # Anomaly: Missing or suspicious data
  missing_initial_dates <- sum(firms$Initial.Cert.Date == "DATA MISSING" | is.na(firms$Initial.Cert.Date))
  missing_gaps <- sum(is.na(firms$Gap.Years) | firms$Gap.Years == "UNKNOWN")

  anomalies$data_quality_issues <- list(
    missing_initial_dates = missing_initial_dates,
    missing_gaps = missing_gaps,
    anomaly_type = "data_obfuscation",
    explanation = "Missing data may hide timeline inconsistencies"
  )

  return(anomalies)
}

# Analyze license number sequences
analyze_license_sequences <- function(firms) {
  cat("\n=== Analyzing License Sequences ===\n")

  analysis <- list()

  # Extract numeric parts
  license_nums <- as.numeric(gsub("[^0-9]", "", firms$License.Number))
  license_nums <- license_nums[!is.na(license_nums)]

  # Check for sequential patterns
  if (length(license_nums) < 2) {
    analysis$license_analysis <- list(
      total_licenses = length(license_nums),
      min_license = if (length(license_nums) > 0) min(license_nums) else NA,
      max_license = if (length(license_nums) > 0) max(license_nums) else NA,
      average_gap = NA,
      large_gaps = 0,
      pattern_type = "insufficient_data",
      explanation = "Need at least 2 licenses to analyze patterns"
    )
  } else {
    if (length(license_nums) > 0) {
      sorted_licenses <- sort(license_nums)
      gaps <- diff(sorted_licenses)
      avg_gap <- if (length(gaps) > 0) mean(gaps, na.rm = TRUE) else NA
    } else {
      gaps <- numeric(0)
      avg_gap <- NA
    }

    analysis$license_analysis <- list(
      total_licenses = length(license_nums),
      min_license = if (length(license_nums) > 0) min(license_nums) else NA,
      max_license = if (length(license_nums) > 0) max(license_nums) else NA,
      average_gap = avg_gap,
      large_gaps = if (length(gaps) > 0) sum(gaps > 1000, na.rm = TRUE) else 0,
      pattern_type = if (!is.na(avg_gap) && avg_gap < 100) "sequential" else "scattered",
      explanation = "Sequential licenses may indicate coordinated registration"
    )
  }

  return(analysis)
}

# Find connections through addresses
find_address_connections <- function(firms) {
  cat("\n=== Finding Address Connections ===\n")

  connections <- list()

  # Normalize addresses
  normalize_addr <- function(addr) {
    addr <- toupper(addr)
    addr <- str_replace_all(addr, "[#]", "STE")
    addr <- str_replace_all(addr, "\\bSTREET\\b", "ST")
    addr <- str_replace_all(addr, "\\bDRIVE\\b", "DR")
    addr <- str_replace_all(addr, "\\bROAD\\b", "RD")
    addr <- str_replace_all(addr, "[[:punct:]]", " ")
    addr <- str_replace_all(addr, "\\s+", " ")
    return(str_trim(addr))
  }

  if ("Address" %in% names(firms) && nrow(firms) > 0) {
    firms$Address.Normalized <- sapply(firms$Address, normalize_addr)

    # Find all shared addresses
    address_counts <- table(firms$Address.Normalized)
    shared <- address_counts[address_counts > 1]
  } else {
    address_counts <- table(character(0))
    shared <- address_counts[address_counts > 1]
  }

  connections$shared_addresses <- list()
  if (length(shared) > 0) {
    for (addr in names(shared)) {
      firms_at_addr <- firms[firms$Address.Normalized == addr, ]
      connections$shared_addresses[[length(connections$shared_addresses) + 1]] <- list(
        address = addr,
        firm_count = as.numeric(shared[addr]),
        firms = firms_at_addr$Firm.Name,
        license_numbers = firms_at_addr$License.Number
      )
    }
  }

  return(connections)
}

# Main analysis
main_analysis <- function() {
  cat("=== Additional Anomalies Analysis ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load firms
  firms <- load_firms()

  # Find anomalies
  anomalies <- find_anomalies(firms)

  # Analyze license sequences
  license_analysis <- analyze_license_sequences(firms)

  # Find address connections
  address_connections <- find_address_connections(firms)

  # Create results
  results <- list(
    analysis_date = as.character(Sys.Date()),
    anomalies = anomalies,
    license_analysis = license_analysis,
    address_connections = address_connections,
    summary = list(
      license_prefixes = length(anomalies$license_patterns$unique_prefixes),
      firm_types = length(anomalies$firm_type_distribution$types),
      expiration_years = anomalies$expiration_clustering$unique_years,
      states_involved = anomalies$state_distribution$state_count,
      shared_address_clusters = length(address_connections$shared_addresses)
    )
  )

  # Save results
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved results to:", OUTPUT_FILE, "\n")

  # Print summary
  cat("\n=== Anomalies Summary ===\n")
  cat("License Prefixes:", results$summary$license_prefixes, "\n")
  cat("Firm Types:", results$summary$firm_types, "\n")
  cat("Expiration Years:", results$summary$expiration_years, "\n")
  cat("States Involved:", results$summary$states_involved, "\n")
  cat("Address Clusters:", results$summary$shared_address_clusters, "\n")

  cat("\n=== Analysis Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  main_analysis()
}
