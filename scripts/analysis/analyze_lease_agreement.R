#!/usr/bin/env Rscript
# Analyze lease renewal agreement for abnormalities, violations, and anomalies

library(jsonlite)
library(stringr)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

EVIDENCE_DIR <- file.path(PROJECT_ROOT, "evidence")
RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_TIMELINES_DIR, "lease_agreement_analysis.json")

# Load lease agreement
load_lease_agreement <- function() {
  lease_file <- file.path(EVIDENCE_DIR, "LeaseRenewalAgreement_6102025.txt")
  if (!file.exists(lease_file)) {
    stop("Lease agreement file not found: ", lease_file)
  }

  content <- readLines(lease_file, warn = FALSE)
  return(list(
    file = lease_file,
    content = content,
    line_count = length(content),
    full_text = paste(content, collapse = "\n")
  ))
}

# Find key terms and clauses
find_key_terms <- function(lease_data) {
  text <- tolower(lease_data$full_text)

  key_terms <- list(
    # License-related terms
    license_terms = c("license", "licensed", "broker", "real estate", "property management"),

    # Violation-related terms
    violation_terms = c("violation", "breach", "default", "non-compliance", "illegal"),

    # STR-related terms
    str_terms = c("short term", "short-term", "airbnb", "vrbo", "transient", "sublet", "sublease"),

    # ADA/FHA terms
    ada_terms = c("reasonable accommodation", "disability", "ada", "fair housing", "fha"),

    # Financial terms
    financial_terms = c("rent", "deposit", "fee", "charge", "penalty", "late fee"),

    # Legal terms
    legal_terms = c("attorney", "legal", "counsel", "lawyer", "unauthorized practice")
  )

  found_terms <- list()
  for (category in names(key_terms)) {
    terms <- key_terms[[category]]
    matches <- c()
    for (term in terms) {
      if (grepl(term, text, ignore.case = TRUE)) {
        matches <- c(matches, term)
        # Find context around matches
        pattern <- paste0("(.{0,100}", term, ".{0,100})")
        contexts <- str_extract_all(text, pattern)[[1]]
        if (length(contexts) > 0) {
          matches <- c(matches, paste0("CONTEXT: ", contexts[1]))
        }
      }
    }
    if (length(matches) > 0) {
      found_terms[[category]] <- unique(matches)
    }
  }

  return(found_terms)
}

# Find abnormalities
find_abnormalities <- function(lease_data) {
  abnormalities <- list()

  if (is.null(lease_data) || is.null(lease_data$full_text) ||
      is.na(lease_data$full_text) || lease_data$full_text == "") {
    abnormalities$error <- "No lease text available for analysis"
    return(abnormalities)
  }

  text <- lease_data$full_text

  # Check for missing required clauses
  required_clauses <- c(
    "landlord", "tenant", "premises", "rent", "term", "lease",
    "possession", "use", "maintenance", "default", "termination"
  )

  missing_clauses <- c()
  for (clause in required_clauses) {
    if (!grepl(clause, text, ignore.case = TRUE)) {
      missing_clauses <- c(missing_clauses, clause)
    }
  }

  if (length(missing_clauses) > 0) {
    abnormalities$missing_clauses <- list(
      type = "missing_required_clauses",
      description = "Standard lease clauses appear to be missing",
      missing = missing_clauses,
      severity = "medium"
    )
  }

  # Check for unusual language
  unusual_patterns <- c(
    "unauthorized practice",
    "without license",
    "illegal operation",
    "violation of",
    "non-compliant"
  )

  unusual_found <- c()
  for (pattern in unusual_patterns) {
    if (grepl(pattern, text, ignore.case = TRUE)) {
      unusual_found <- c(unusual_found, pattern)
    }
  }

  if (length(unusual_found) > 0) {
    abnormalities$unusual_language <- list(
      type = "unusual_legal_language",
      description = "Unusual language found in lease agreement",
      patterns = unusual_found,
      severity = "high"
    )
  }

  # Check for STR restrictions or permissions
  str_mentions <- grepl("short.?term|airbnb|vrbo|transient|sublet|sublease", text, ignore.case = TRUE)
  if (str_mentions) {
    abnormalities$str_mentions <- list(
      type = "str_related_content",
      description = "Short-term rental related content found",
      found = TRUE,
      severity = "medium"
    )
  }

  # Check for accommodation language
  accommodation_mentions <- grepl("reasonable accommodation|disability|ada|fair housing", text, ignore.case = TRUE)
  if (accommodation_mentions) {
    abnormalities$accommodation_mentions <- list(
      type = "accommodation_related_content",
      description = "Reasonable accommodation or disability-related content found",
      found = TRUE,
      severity = "high"
    )
  }

  # Check for license references
  license_mentions <- grepl("license|licensed|broker|real estate license", text, ignore.case = TRUE)
  if (license_mentions) {
    abnormalities$license_mentions <- list(
      type = "license_related_content",
      description = "License-related content found in lease",
      found = TRUE,
      severity = "high"
    )
  }

  # Extract dates
  date_pattern <- "\\d{1,2}[/-]\\d{1,2}[/-]\\d{2,4}"
  dates <- str_extract_all(text, regex(date_pattern, ignore_case = TRUE))[[1]]
  if (length(dates) > 0) {
    abnormalities$dates_found <- list(
      type = "date_extraction",
      dates = unique(dates),
      count = length(unique(dates))
    )
  }

  # Extract names/entities
  name_pattern <- "([A-Z][a-z]+\\s+[A-Z][a-z]+|[A-Z]+\\s+[A-Z]+)"
  names <- str_extract_all(text, regex(name_pattern, ignore_case = FALSE))[[1]]
  names <- unique(names[!grepl("(THE|AND|FOR|WITH|FROM|THIS|THAT|LEASE|RENTAL|AGREEMENT)", names, ignore.case = TRUE)])
  if (length(names) > 0) {
    abnormalities$entities_found <- list(
      type = "entity_extraction",
      entities = names[1:min(20, length(names))],  # Limit to first 20
      count = length(names)
    )
  }

  return(abnormalities)
}

# Extract key information
extract_key_info <- function(lease_data) {
  text <- lease_data$full_text

  info <- list(
    # Property address
    property_address = NA,
    # Unit number
    unit_number = NA,
    # Lease term dates
    lease_start = NA,
    lease_end = NA,
    # Rent amount
    rent_amount = NA,
    # Landlord name
    landlord_name = NA,
    # Tenant name
    tenant_name = NA,
    # Management company
    management_company = NA
  )

  # Try to extract property address (look for common patterns)
  address_patterns <- c(
    "\\d+\\s+[A-Z][a-z]+\\s+[A-Z][a-z]+\\s+(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Boulevard|Blvd|Lane|Ln|Way|Circle|Cir)",
    "800.*Carlyle|850.*Carlyle|John.*Carlyle"
  )

  for (pattern in address_patterns) {
    match <- str_extract(text, regex(pattern, ignore_case = TRUE))
    if (!is.na(match)) {
      info$property_address <- match
      break
    }
  }

  # Extract unit number
  unit_match <- str_extract(text, regex("(unit|apt|apartment|#)\\s*[0-9]+", ignore_case = TRUE))
  if (!is.na(unit_match)) {
    info$unit_number <- str_extract(unit_match, "[0-9]+")
  }

  # Extract rent amount
  rent_match <- str_extract(text, regex("\\$[0-9,]+(\\.[0-9]{2})?", ignore_case = TRUE))
  if (!is.na(rent_match)) {
    info$rent_amount <- rent_match
  }

  # Look for Kettler references
  if (grepl("kettler", text, ignore.case = TRUE)) {
    info$management_company <- "Kettler Management"
  }

  return(info)
}

# Main analysis function
analyze_lease_agreement <- function() {
  cat("=== Lease Agreement Analysis ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load lease
  cat("Loading lease agreement...\n")
  lease_data <- load_lease_agreement()
  cat("Loaded", lease_data$line_count, "lines\n\n")

  # Find key terms
  cat("Finding key terms...\n")
  key_terms <- find_key_terms(lease_data)

  # Find abnormalities
  cat("Finding abnormalities...\n")
  abnormalities <- find_abnormalities(lease_data)

  # Extract key information
  cat("Extracting key information...\n")
  key_info <- extract_key_info(lease_data)

  # Compile results
  results <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      file = lease_data$file,
      line_count = lease_data$line_count,
      analysis_type = "lease_agreement_review"
    ),
    key_information = key_info,
    key_terms_found = key_terms,
    abnormalities = abnormalities,
    summary = list(
      total_abnormalities = length(abnormalities),
      high_severity = sum(sapply(abnormalities, function(x) if(!is.null(x$severity)) x$severity == "high" else FALSE)),
      medium_severity = sum(sapply(abnormalities, function(x) if(!is.null(x$severity)) x$severity == "medium" else FALSE)),
      key_terms_categories = length(key_terms)
    )
  )

  # Save results
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved analysis to:", OUTPUT_FILE, "\n")

  # Print summary
  cat("\n=== Analysis Summary ===\n")
  cat("Total abnormalities:", results$summary$total_abnormalities, "\n")
  cat("High severity:", results$summary$high_severity, "\n")
  cat("Medium severity:", results$summary$medium_severity, "\n")
  cat("Key term categories:", results$summary$key_terms_categories, "\n")

  if (!is.na(key_info$property_address)) {
    cat("Property:", key_info$property_address, "\n")
  }
  if (!is.na(key_info$unit_number)) {
    cat("Unit:", key_info$unit_number, "\n")
  }

  return(results)
}

if (!interactive()) analyze_lease_agreement()
