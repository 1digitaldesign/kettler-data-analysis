#!/usr/bin/env Rscript
# Data Quality Validation Script
# Validates license data, flags duplicates, and creates quality reports

library(dplyr)
library(stringr)
library(data.table)

# Configuration
DATA_DIR <- "data"
CLEANED_DIR <- file.path(DATA_DIR, "cleaned")
ANALYSIS_DIR <- file.path(DATA_DIR, "analysis")
dir.create(ANALYSIS_DIR, showWarnings = FALSE, recursive = TRUE)

# Validate license number formats
validate_license_numbers <- function(df) {
  if (nrow(df) == 0) {
    return(df)
  }

  # If license_number column doesn't exist, return original dataframe with validation flags set to NA
  if (!"license_number" %in% names(df)) {
    df$license_valid <- NA
    df$license_format_issue <- "License number column not found"
    return(df)
  }

  df$license_valid <- TRUE
  df$license_format_issue <- ""

  for (i in 1:nrow(df)) {
    license <- df$license_number[i]

    if (is.na(license) || license == "") {
      df$license_valid[i] <- FALSE
      df$license_format_issue[i] <- "Missing license number"
      next
    }

    license <- str_trim(license)

    # Check for common valid formats
    # Most license numbers are alphanumeric, 6-15 characters
    if (nchar(license) < 6 || nchar(license) > 15) {
      df$license_valid[i] <- FALSE
      df$license_format_issue[i] <- paste("Invalid length:", nchar(license))
    }

    # Check for invalid characters (should be alphanumeric, dashes, spaces)
    if (!str_detect(license, "^[A-Za-z0-9\\s\\-]+$")) {
      df$license_valid[i] <- FALSE
      df$license_format_issue[i] <- "Contains invalid characters"
    }
  }

  return(df)
}

# Flag potential duplicates
flag_duplicates <- function(df) {
  if (nrow(df) == 0) {
    return(df)
  }

  df$is_duplicate <- FALSE
  df$duplicate_group <- NA_integer_
  df$duplicate_reason <- ""

  # Check for required columns and handle missing ones gracefully
  has_license <- "license_number" %in% names(df)
  has_name <- "name" %in% names(df)
  has_address <- "address" %in% names(df)
  has_state <- "state" %in% names(df)

  # Create matching keys with fallbacks for missing columns
  license_part <- if (has_license) toupper(str_remove_all(df$license_number, "[^A-Za-z0-9]")) else rep("", nrow(df))
  name_part <- if (has_name) toupper(str_remove_all(df$name, "[^A-Za-z0-9]")) else rep("", nrow(df))
  address_part <- if (has_address) toupper(str_remove_all(df$address, "[^A-Za-z0-9]")) else rep("", nrow(df))
  state_part <- if (has_state) toupper(str_remove_all(df$state, "[^A-Za-z0-9]")) else rep("", nrow(df))

  df$match_key1 <- paste(
    license_part,
    name_part,
    state_part,
    sep = "|"
  )

  df$match_key2 <- paste(
    name_part,
    address_part,
    state_part,
    sep = "|"
  )

  # Find duplicates by license number + name + state
  dup_groups1 <- df %>%
    group_by(match_key1) %>%
    mutate(group_size = n()) %>%
    filter(group_size > 1) %>%
    ungroup()

  if (nrow(dup_groups1) > 0) {
    dup_groups1 <- dup_groups1 %>%
      group_by(match_key1) %>%
      mutate(duplicate_group = cur_group_id()) %>%
      ungroup()

    df$is_duplicate[df$match_key1 %in% dup_groups1$match_key1] <- TRUE
    df$duplicate_group[df$match_key1 %in% dup_groups1$match_key1] <-
      dup_groups1$duplicate_group[match(df$match_key1[df$match_key1 %in% dup_groups1$match_key1],
                                         dup_groups1$match_key1)]
    df$duplicate_reason[df$match_key1 %in% dup_groups1$match_key1] <- "Same license number, name, and state"
  }

  # Find duplicates by name + address + state (different license numbers)
  dup_groups2 <- df %>%
    filter(!is_duplicate) %>%
    group_by(match_key2) %>%
    mutate(group_size = n()) %>%
    filter(group_size > 1) %>%
    ungroup()

  if (nrow(dup_groups2) > 0) {
    # Get max duplicate_group, defaulting to 0 if all are NA (prevents -Inf)
    max_dup_group <- max(df$duplicate_group, 0L, na.rm = TRUE)
    if (is.infinite(max_dup_group) || is.na(max_dup_group)) {
      max_dup_group <- 0L
    }

    dup_groups2 <- dup_groups2 %>%
      group_by(match_key2) %>%
      mutate(duplicate_group = max_dup_group + cur_group_id()) %>%
      ungroup()

    df$is_duplicate[df$match_key2 %in% dup_groups2$match_key2] <- TRUE
    df$duplicate_group[df$match_key2 %in% dup_groups2$match_key2] <-
      dup_groups2$duplicate_group[match(df$match_key2[df$match_key2 %in% dup_groups2$match_key2],
                                         dup_groups2$match_key2)]
    df$duplicate_reason[df$match_key2 %in% dup_groups2$match_key2] <- "Same name, address, and state (different license)"
  }

  # Remove temporary columns
  df <- df %>% select(-match_key1, -match_key2)

  return(df)
}

# Validate addresses
validate_addresses <- function(df) {
  if (nrow(df) == 0 || !"address" %in% names(df)) {
    return(df)
  }

  df$address_valid <- TRUE
  df$address_issue <- ""

  for (i in 1:nrow(df)) {
    addr <- df$address[i]

    if (is.na(addr) || addr == "") {
      df$address_valid[i] <- FALSE
      df$address_issue[i] <- "Missing address"
      next
    }

    addr <- str_trim(addr)

    # Check for minimum length
    if (nchar(addr) < 10) {
      df$address_valid[i] <- FALSE
      df$address_issue[i] <- "Address too short"
    }

    # Check for common address components
    has_street <- str_detect(addr, "(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Boulevard|Blvd|Lane|Ln)")
    has_city <- str_detect(addr, "[A-Z]{2}\\s+\\d{5}")  # State + ZIP pattern

    if (!has_street && !has_city) {
      df$address_valid[i] <- FALSE
      df$address_issue[i] <- "Missing street or city/state/zip"
    }
  }

  return(df)
}

# Validate dates
validate_dates <- function(df) {
  date_columns <- c("expiration_date", "initial_cert_date", "expiration_date_parsed", "initial_cert_date_parsed")

  for (col in date_columns) {
    if (!col %in% names(df)) next

    df[[paste0(col, "_valid")]] <- TRUE
    df[[paste0(col, "_issue")]] <- ""

    for (i in 1:nrow(df)) {
      date_val <- df[[col]][i]

      if (is.na(date_val) || date_val == "") {
        df[[paste0(col, "_valid")]][i] <- FALSE
        df[[paste0(col, "_issue")]][i] <- "Missing date"
        next
      }

      # Try to parse date
      parsed <- tryCatch({
        as.Date(date_val)
      }, error = function(e) NULL)

      if (is.null(parsed)) {
        df[[paste0(col, "_valid")]][i] <- FALSE
        df[[paste0(col, "_issue")]][i] <- "Invalid date format"
      } else {
        # Check if date is reasonable (not too far in past or future)
        if (parsed < as.Date("1900-01-01") || parsed > as.Date("2100-01-01")) {
          df[[paste0(col, "_valid")]][i] <- FALSE
          df[[paste0(col, "_issue")]][i] <- "Date out of reasonable range"
        }
      }
    }
  }

  return(df)
}

# Cross-reference addresses
cross_reference_addresses <- function(df) {
  if (nrow(df) == 0 || !"address" %in% names(df)) {
    return(df)
  }

  df$address_cluster <- NA_integer_

  # Normalize addresses for clustering
  df$address_normalized_cluster <- toupper(df$address) %>%
    str_remove_all("[[:punct:]]") %>%
    str_replace_all("\\s+", " ") %>%
    str_trim()

  # Group by normalized address
  address_groups <- df %>%
    group_by(address_normalized_cluster) %>%
    summarise(cluster_id = cur_group_id(), .groups = 'drop')

  df$address_cluster <- address_groups$cluster_id[match(df$address_normalized_cluster,
                                                        address_groups$address_normalized_cluster)]

  df <- df %>% select(-address_normalized_cluster)

  return(df)
}

# Generate data quality report
generate_quality_report <- function(df) {
  report <- list()

  report$total_records <- nrow(df)

  # License number validation
  if ("license_valid" %in% names(df)) {
    report$license_validation <- list(
      valid = sum(df$license_valid, na.rm = TRUE),
      invalid = sum(!df$license_valid, na.rm = TRUE),
      missing = sum(is.na(df$license_number) | df$license_number == "", na.rm = TRUE)
    )
  }

  # Duplicate analysis
  if ("is_duplicate" %in% names(df)) {
    report$duplicates <- list(
      total_duplicates = sum(df$is_duplicate, na.rm = TRUE),
      duplicate_groups = length(unique(df$duplicate_group[df$is_duplicate])),
      unique_records = sum(!df$is_duplicate, na.rm = TRUE)
    )
  }

  # Address validation
  if ("address_valid" %in% names(df)) {
    report$address_validation <- list(
      valid = sum(df$address_valid, na.rm = TRUE),
      invalid = sum(!df$address_valid, na.rm = TRUE),
      missing = sum(is.na(df$address) | df$address == "", na.rm = TRUE)
    )
  }

  # Date validation
  date_cols <- names(df)[str_detect(names(df), "_valid$")]
  report$date_validation <- list()
  for (col in date_cols) {
    if (str_detect(col, "date")) {
      report$date_validation[[col]] <- list(
        valid = sum(df[[col]], na.rm = TRUE),
        invalid = sum(!df[[col]], na.rm = TRUE)
      )
    }
  }

  # Completeness score
  required_fields <- c("license_number", "name", "state", "address")
  completeness_scores <- sapply(required_fields, function(field) {
    if (field %in% names(df)) {
      sum(!is.na(df[[field]]) & df[[field]] != "", na.rm = TRUE) / nrow(df) * 100
    } else {
      0
    }
  })
  report$completeness <- completeness_scores
  report$overall_completeness <- mean(completeness_scores)

  # State distribution
  if ("state" %in% names(df)) {
    report$state_distribution <- df %>%
      group_by(state) %>%
      summarise(count = n(), .groups = 'drop') %>%
      arrange(desc(count))
  }

  return(report)
}

# Main validation function
main_validation <- function() {
  cat("Starting data quality validation...\n")

  # Load cleaned data
  cleaned_file <- file.path(CLEANED_DIR, "dpor_all_cleaned.csv")

  if (!file.exists(cleaned_file)) {
    cat("Cleaned data file not found. Running cleaning script first...\n")
    return()
  }

  df <- read.csv(cleaned_file, stringsAsFactors = FALSE)
  cat("Loaded", nrow(df), "records for validation\n")

  if (nrow(df) == 0) {
    cat("No data to validate\n")
    return()
  }

  # Run validations
  cat("\nValidating license numbers...\n")
  df <- validate_license_numbers(df)

  cat("Flagging duplicates...\n")
  df <- flag_duplicates(df)

  cat("Validating addresses...\n")
  df <- validate_addresses(df)

  cat("Validating dates...\n")
  df <- validate_dates(df)

  cat("Cross-referencing addresses...\n")
  df <- cross_reference_addresses(df)

  # Generate quality report
  cat("\nGenerating quality report...\n")
  report <- generate_quality_report(df)

  # Save validated data
  validated_file <- file.path(ANALYSIS_DIR, "dpor_validated.csv")
  write.csv(df, validated_file, row.names = FALSE)
  cat("Saved validated data to:", validated_file, "\n")

  # Save quality report
  report_file <- file.path(ANALYSIS_DIR, "data_quality_report.json")
  jsonlite::write_json(report, report_file, pretty = TRUE)
  cat("Saved quality report to:", report_file, "\n")

  # Save flagged issues
  issues <- df %>%
    filter(
      (license_valid == FALSE) |
      (is_duplicate == TRUE) |
      (address_valid == FALSE)
    )

  if (nrow(issues) > 0) {
    issues_file <- file.path(ANALYSIS_DIR, "data_quality_issues.csv")
    write.csv(issues, issues_file, row.names = FALSE)
    cat("Saved", nrow(issues), "flagged issues to:", issues_file, "\n")
  }

  # Print summary
  cat("\n=== Data Quality Summary ===\n")
  cat("Total Records:", report$total_records, "\n")
  cat("Overall Completeness:", round(report$overall_completeness, 2), "%\n")

  if (!is.null(report$license_validation)) {
    cat("\nLicense Validation:\n")
    cat("  Valid:", report$license_validation$valid, "\n")
    cat("  Invalid:", report$license_validation$invalid, "\n")
    cat("  Missing:", report$license_validation$missing, "\n")
  }

  if (!is.null(report$duplicates)) {
    cat("\nDuplicates:\n")
    cat("  Total Duplicate Records:", report$duplicates$total_duplicates, "\n")
    cat("  Duplicate Groups:", report$duplicates$duplicate_groups, "\n")
    cat("  Unique Records:", report$duplicates$unique_records, "\n")
  }

  cat("\n=== Validation Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  main_validation()
}
