#!/usr/bin/env Rscript
# Find new anomalies in existing dataset and add to current data
# Analyze all available data sources for patterns, inconsistencies, and violations

library(jsonlite)
library(dplyr)
library(stringr)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_ANOMALIES_DIR, "new_anomalies_found.json")

# Load all available data sources
load_all_data_sources <- function() {
  data_sources <- list()

  # Load individuals
  individuals_file <- file.path(RESEARCH_DIR, "all_individuals_identified.json")
  if (file.exists(individuals_file)) {
    data_sources$individuals <- fromJSON(individuals_file)
  }

  # Load license audit
  audit_file <- file.path(RESEARCH_DIR, "management_chain_license_audit.json")
  if (file.exists(audit_file)) {
    data_sources$license_audit <- fromJSON(audit_file)
  }

  # Load DPOR verification
  dpor_file <- file.path(RESEARCH_DIR, "dpor_license_verification_all.json")
  if (file.exists(dpor_file)) {
    data_sources$dpor_verification <- fromJSON(dpor_file)
  }

  # Load bar association verification
  bar_file <- file.path(RESEARCH_DIR, "bar_association_verification_all.json")
  if (file.exists(bar_file)) {
    data_sources$bar_verification <- fromJSON(bar_file)
  }

  # Load property management verification
  pm_file <- file.path(RESEARCH_DIR, "property_management_license_verification.json")
  if (file.exists(pm_file)) {
    data_sources$property_management <- fromJSON(pm_file)
  }

  # Load violations compiled
  violations_file <- file.path(RESEARCH_DIR, "all_violations_compiled.json")
  if (file.exists(violations_file)) {
    data_sources$violations <- fromJSON(violations_file)
  }

  return(data_sources)
}

# Find email domain anomalies
find_email_anomalies <- function(data_sources) {
  anomalies <- list()

  if (!is.null(data_sources$individuals)) {
    individuals <- data_sources$individuals$individuals_identified

    # Extract emails
    emails <- c()
    for (ind in names(individuals)) {
      if (!is.null(individuals[[ind]]$email)) {
        emails <- c(emails, individuals[[ind]]$email)
      }
    }

    # Check for domain patterns
    if (length(emails) > 0) {
      domains <- str_extract(emails, "@(.+)")
      domains <- str_remove(domains, "^@")
      domains <- domains[!is.na(domains)]

      if (length(domains) > 0) {
        domain_table <- table(domains)

        # Anomaly: Multiple domains for same organization
        if (length(unique(domains)) > 1) {
          anomalies$email_domains <- list(
            type = "multiple_email_domains",
            description = "Multiple email domains found for Kettler organization",
            domains = unique(domains),
            count = length(unique(domains)),
            severity = "medium"
          )
        }

        # Anomaly: Non-standard domain
        standard_domains <- c("kettler.com", "kettlermanagement.com")
        non_standard <- setdiff(domains, standard_domains)
        if (length(non_standard) > 0) {
          anomalies$non_standard_domains <- list(
            type = "non_standard_email_domains",
            description = "Non-standard email domains found",
            domains = non_standard,
            severity = "medium"
          )
        }
      }
    }
  }

  return(anomalies)
}

# Find role-title inconsistencies
find_role_anomalies <- function(data_sources) {
  anomalies <- list()

  if (!is.null(data_sources$individuals)) {
    individuals <- data_sources$individuals$individuals_identified

    roles <- c()
    for (ind in names(individuals)) {
      if (!is.null(individuals[[ind]]$role)) {
        roles <- c(roles, individuals[[ind]]$role)
      }
    }

    # Check for role inconsistencies
    management_roles <- roles[grepl("Manager|Director|VP|SVP|President|CEO|CFO|CIO|Counsel", roles, ignore.case = TRUE)]

    if (length(management_roles) > 0) {
      # Anomaly: High number of management roles
      if (length(management_roles) > 5) {
        anomalies$excessive_management <- list(
          type = "excessive_management_layers",
          description = "High number of management roles identified",
          count = length(management_roles),
          roles = management_roles,
          severity = "low"
        )
      }
    }
  }

  return(anomalies)
}

# Find license verification gaps
find_license_gaps <- function(data_sources) {
  anomalies <- list()

  if (!is.null(data_sources$license_audit)) {
    audits <- data_sources$license_audit$audits

    if (!is.null(audits) && length(audits) > 0) {
      # Check for NEEDS_VERIFICATION status
      needs_verification <- audits[audits$status == "NEEDS_VERIFICATION", ]

      if (nrow(needs_verification) > 0) {
        anomalies$verification_gaps <- list(
          type = "license_verification_gaps",
          description = "Individuals requiring license verification",
          count = nrow(needs_verification),
          individuals = needs_verification$name,
          severity = "high"
        )
      }

      # Check for NO_REQUIREMENTS_DEFINED
      no_requirements <- audits[audits$status == "NO_REQUIREMENTS_DEFINED", ]

      if (nrow(no_requirements) > 0) {
        anomalies$missing_requirements <- list(
          type = "missing_license_requirements",
          description = "Roles without defined license requirements",
          count = nrow(no_requirements),
          roles = unique(no_requirements$role),
          severity = "medium"
        )
      }
    }
  }

  return(anomalies)
}

# Find state search coverage gaps
find_search_coverage_gaps <- function(data_sources) {
  anomalies <- list()

  if (!is.null(data_sources$dpor_verification)) {
    searches <- data_sources$dpor_verification$searches

    if (!is.null(searches) && length(searches) > 0) {
      # Check if all searches are frameworks
      framework_count <- 0
      total_searches <- 0

      for (individual in names(searches)) {
        states <- searches[[individual]]$states
        if (!is.null(states)) {
          for (state in names(states)) {
            total_searches <- total_searches + 1
            if (!is.null(states[[state]]$status) && states[[state]]$status == "framework") {
              framework_count <- framework_count + 1
            }
          }
        }
      }

      if (framework_count == total_searches && total_searches > 0) {
        anomalies$search_coverage <- list(
          type = "incomplete_dpor_search_coverage",
          description = "All DPOR searches are frameworks - actual searches not performed",
          total_searches = total_searches,
          framework_searches = framework_count,
          coverage_percentage = 0,
          severity = "high"
        )
      }
    }
  }

  return(anomalies)
}

# Find violation pattern anomalies
find_violation_patterns <- function(data_sources) {
  anomalies <- list()

  if (!is.null(data_sources$violations)) {
    violation_matrix <- data_sources$violations$violation_matrix

    if (!is.null(violation_matrix)) {
      # Check for high violation counts
      if (!is.null(violation_matrix$zoning_violations$unregistered_strs)) {
        str_count <- violation_matrix$zoning_violations$unregistered_strs
        if (str_count > 50) {
          anomalies$massive_str_violations <- list(
            type = "massive_str_violations",
            description = "Extremely high number of unregistered STRs",
            count = str_count,
            threshold = 50,
            severity = "critical"
          )
        }
      }

      # Check for multiple violation types
      violation_types <- 0
      if (!is.null(violation_matrix$license_violations$confirmed) && violation_matrix$license_violations$confirmed > 0) violation_types <- violation_types + 1
      if (!is.null(violation_matrix$upl_violations$potential_upl) && violation_matrix$upl_violations$potential_upl > 0) violation_types <- violation_types + 1
      if (!is.null(violation_matrix$zoning_violations$unregistered_strs) && violation_matrix$zoning_violations$unregistered_strs > 0) violation_types <- violation_types + 1

      if (violation_types >= 3) {
        anomalies$multiple_violation_types <- list(
          type = "multiple_violation_categories",
          description = "Violations found across multiple categories",
          categories = violation_types,
          severity = "high"
        )
      }
    }
  }

  return(anomalies)
}

# Main analysis function
find_new_anomalies <- function() {
  cat("=== Finding New Anomalies ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load all data sources
  cat("Loading data sources...\n")
  data_sources <- load_all_data_sources()
  cat("Loaded", length(data_sources), "data sources\n\n")

  # Find anomalies
  all_anomalies <- list()

  cat("Analyzing email patterns...\n")
  all_anomalies$email <- find_email_anomalies(data_sources)

  cat("Analyzing role patterns...\n")
  all_anomalies$roles <- find_role_anomalies(data_sources)

  cat("Analyzing license gaps...\n")
  all_anomalies$licenses <- find_license_gaps(data_sources)

  cat("Analyzing search coverage...\n")
  all_anomalies$coverage <- find_search_coverage_gaps(data_sources)

  cat("Analyzing violation patterns...\n")
  all_anomalies$violations <- find_violation_patterns(data_sources)

  # Count severities
  critical_count <- 0
  high_count <- 0
  medium_count <- 0
  low_count <- 0

  for (category in names(all_anomalies)) {
    for (anomaly_name in names(all_anomalies[[category]])) {
      anomaly <- all_anomalies[[category]][[anomaly_name]]
      if (!is.null(anomaly$severity)) {
        if (anomaly$severity == "critical") critical_count <- critical_count + 1
        else if (anomaly$severity == "high") high_count <- high_count + 1
        else if (anomaly$severity == "medium") medium_count <- medium_count + 1
        else if (anomaly$severity == "low") low_count <- low_count + 1
      }
    }
  }

  # Compile results
  results <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      analysis_type = "anomaly_detection",
      data_sources_analyzed = names(data_sources)
    ),
    anomalies_found = all_anomalies,
    summary = list(
      total_anomaly_categories = length(all_anomalies),
      total_anomalies = sum(sapply(all_anomalies, length)),
      critical_count = critical_count,
      high_count = high_count,
      medium_count = medium_count,
      low_count = low_count
    )
  )
  )

  # Save results
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved anomalies to:", OUTPUT_FILE, "\n")

  # Print summary
  cat("\n=== Anomaly Summary ===\n")
  cat("Total anomaly categories:", results$summary$total_anomaly_categories, "\n")
  cat("Total anomalies:", results$summary$total_anomalies, "\n")
  cat("Critical:", results$summary$critical_count, "\n")
  cat("High:", results$summary$high_count, "\n")
  cat("Medium:", results$summary$medium_count, "\n")
  cat("Low:", results$summary$low_count, "\n")

  return(results)
}

if (!interactive()) find_new_anomalies()
