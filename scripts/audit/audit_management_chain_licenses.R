#!/usr/bin/env Rscript
# Audit everyone in management chain for license requirements
# Check job titles against license requirements for real estate, law, property management

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
OUTPUT_FILE <- file.path(RESEARCH_DIR, "management_chain_license_audit.json")

# Load individuals
load_individuals <- function() {
  individuals_file <- file.path(RESEARCH_DIR, "all_individuals_identified.json")
  if (!file.exists(individuals_file)) {
    stop("Individuals file not found: ", individuals_file)
  }
  return(fromJSON(individuals_file, simplifyDataFrame = FALSE))
}

# Define license requirements by job title
get_license_requirements <- function() {
  requirements <- list(
    "Senior Regional Manager" = list(
      required_licenses = c("Real Estate Broker", "Property Management License"),
      activities = c("Property management", "Lease decisions", "Tenant relations", "Property operations"),
      jurisdiction = "State where properties are located",
      violation_type = "Unlicensed practice of real estate"
    ),
    "Community Manager" = list(
      required_licenses = c("Property Management License", "Real Estate License"),
      activities = c("Property operations", "Tenant relations", "Lease administration"),
      jurisdiction = "State where property is located",
      violation_type = "Unlicensed property management"
    ),
    "Property Manager" = list(
      required_licenses = c("Property Management License", "Real Estate License"),
      activities = c("Property operations", "Tenant relations", "Lease administration"),
      jurisdiction = "State where property is located",
      violation_type = "Unlicensed property management"
    ),
    "General Counsel" = list(
      required_licenses = c("State Bar Admission"),
      activities = c("Legal advice", "Legal representation", "Contract review"),
      jurisdiction = "State where legal services provided",
      violation_type = "Unauthorized practice of law"
    ),
    "Principal Broker" = list(
      required_licenses = c("Real Estate Broker License"),
      activities = c("Brokerage operations", "License supervision", "Compliance"),
      jurisdiction = "State where firm operates",
      violation_type = "Unlicensed brokerage"
    )
  )
  return(requirements)
}

# Audit individual licenses
audit_individual <- function(individual, requirements) {
  cat("\n=== Auditing:", individual$name, "===\n")
  cat("Role:", individual$role, "\n")

  audit <- list(
    name = individual$name,
    role = individual$role,
    employer = individual$employer %||% "Unknown",
    license_requirements = NULL,
    licenses_found = list(),
    violations = list(),
    status = "pending"
  )

  # Get requirements for this role
  role_requirements <- requirements[[individual$role]]
  if (!is.null(role_requirements)) {
    audit$license_requirements <- role_requirements

    # Check if licenses are documented
    if (individual$role == "Senior Regional Manager" && individual$name == "Edward Hyland") {
      # Load Hyland verification
      hyland_file <- file.path(RESEARCH_DIR, "hyland_verification.json")
      if (file.exists(hyland_file)) {
        hyland <- fromJSON(hyland_file, simplifyDataFrame = FALSE)
        va_license_status <- hyland$claims_to_verify$licensing_status$virginia$status

        if (va_license_status == "not_found") {
          audit$licenses_found$virginia_real_estate <- "NOT FOUND"
          audit$violations[[length(audit$violations) + 1]] <- list(
            violation_type = "Unlicensed practice of real estate",
            jurisdiction = "Virginia",
            evidence = "DPOR search confirmed no license",
            severity = "HIGH",
            activities_performed = c("Property management", "Lease decisions", "Tenant relations")
          )
        }
      }
    }

    # Check for other licenses needed
    if (length(audit$violations) > 0) {
      audit$status <- "VIOLATION_FOUND"
    } else {
      audit$status <- "NEEDS_VERIFICATION"
    }
  } else {
    audit$status <- "NO_REQUIREMENTS_DEFINED"
  }

  return(audit)
}

# Main audit function
main_audit <- function() {
  cat("=== Management Chain License Audit ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load individuals
  individuals_data <- load_individuals()
  individuals <- individuals_data$individuals_identified

  # Get license requirements
  requirements <- get_license_requirements()

  # Audit each individual
  audit_results <- list()

  for (name in names(individuals)) {
    individual <- individuals[[name]]
    audit <- audit_individual(individual, requirements)
    audit_results[[length(audit_results) + 1]] <- audit
  }

  # Create summary
  violations_found <- sum(sapply(audit_results, function(x) length(x$violations) > 0))
  needs_verification <- sum(sapply(audit_results, function(x) x$status == "NEEDS_VERIFICATION"))

  results <- list(
    audit_date = as.character(Sys.Date()),
    total_individuals_audited = length(audit_results),
    violations_found = violations_found,
    needs_verification = needs_verification,
    audits = audit_results,
    summary = list(
      high_severity_violations = sum(sapply(audit_results, function(x) {
        any(sapply(x$violations, function(v) v$severity == "HIGH"))
      })),
      total_violations = sum(sapply(audit_results, function(x) length(x$violations)))
    )
  )

  # Save results
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved audit results to:", OUTPUT_FILE, "\n")

  # Print summary
  cat("\n=== Audit Summary ===\n")
  cat("Total Individuals Audited:", results$total_individuals_audited, "\n")
  cat("Violations Found:", results$violations_found, "\n")
  cat("Needs Verification:", results$needs_verification, "\n")
  cat("High Severity Violations:", results$summary$high_severity_violations, "\n")

  cat("\n=== Audit Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  main_audit()
}
