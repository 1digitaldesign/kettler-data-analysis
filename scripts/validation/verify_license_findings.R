#!/usr/bin/env Rscript
# Verify License Findings - Comprehensive Validation
#
# Validates that all license search data is accurate and complete

library(jsonlite)
library(dplyr)

# Set working directory
if (dir.exists("research")) {
  # Already in repo root
} else if (dir.exists("../research")) {
  setwd("..")
} else if (dir.exists("../../research")) {
  setwd("../..")
}

cat("=== License Findings Verification Report ===\n\n")

# Expected data
EXPECTED_EMPLOYEES <- c(
  "Robert Kettler", "Caitlin Skidmore", "Cindy Fisher", "Pat Cassada",
  "Luke Davis", "Sean Curtin", "Robert Grealy", "Todd Bowen",
  "Amy Groff", "Kristina Thoummarath", "Christina Chang", "Jeffrey Williams",
  "Edward Hyland", "Djene Moyer", "Henry Ramos"
)

EXPECTED_STATES <- c("Connecticut", "DC", "Maryland", "New Jersey", "New York", "Virginia")
EXPECTED_TOTAL <- length(EXPECTED_EMPLOYEES) * length(EXPECTED_STATES)  # 90

# Read consolidated CSV
csv_file <- "research/license_searches/consolidated/all_findings.csv"
if (!file.exists(csv_file)) {
  stop("CSV file not found: ", csv_file)
}

df <- read.csv(csv_file, stringsAsFactors = FALSE)
cat("1. CSV Data Loaded\n")
cat("   Total rows:", nrow(df), "(expected:", EXPECTED_TOTAL, ")\n\n")

# Verification checks
issues <- list()
warnings <- list()

# Check 1: Total count
if (nrow(df) != EXPECTED_TOTAL) {
  issues <- append(issues, paste("Total findings:", nrow(df), "but expected", EXPECTED_TOTAL))
} else {
  cat("✓ Total count correct:", nrow(df), "\n")
}

# Check 2: All states present
states_found <- unique(df$state)
missing_states <- setdiff(EXPECTED_STATES, states_found)
if (length(missing_states) > 0) {
  issues <- append(issues, paste("Missing states:", paste(missing_states, collapse = ", ")))
} else {
  cat("✓ All states present:", paste(states_found, collapse = ", "), "\n")
}

# Check 3: Employees per state (should be 15 each)
state_counts <- table(df$state)
if (any(state_counts != 15)) {
  issues <- append(issues, paste("State counts incorrect:", paste(names(state_counts[state_counts != 15]), collapse = ", ")))
} else {
  cat("✓ All states have 15 employees\n")
}

# Check 4: Licensed count (should be 1 - Caitlin Skidmore in DC)
licensed_count <- sum(df$licensed == TRUE)
if (licensed_count != 1) {
  issues <- append(issues, paste("Licensed count:", licensed_count, "but expected 1"))
} else {
  cat("✓ Licensed count correct: 1 (Caitlin Skidmore in DC)\n")
}

# Check 5: Verify Caitlin Skidmore is licensed only in DC
skidmore <- df[df$employee == "Caitlin Skidmore", ]
if (nrow(skidmore) != 6) {
  issues <- append(issues, paste("Caitlin Skidmore has", nrow(skidmore), "entries but expected 6"))
} else {
  dc_licensed <- skidmore[skidmore$state == "DC" & skidmore$licensed == TRUE, ]
  other_licensed <- skidmore[skidmore$state != "DC" & skidmore$licensed == TRUE, ]
  if (nrow(dc_licensed) != 1) {
    issues <- append(issues, "Caitlin Skidmore should be licensed in DC but isn't")
  } else if (nrow(other_licensed) > 0) {
    issues <- append(issues, paste("Caitlin Skidmore licensed in unexpected states:", paste(other_licensed$state, collapse = ", ")))
  } else {
    cat("✓ Caitlin Skidmore licensed only in DC\n")
  }
}

# Check 6: License number for Caitlin Skidmore
skidmore_dc <- df[df$employee == "Caitlin Skidmore" & df$state == "DC", ]
if (nrow(skidmore_dc) == 1 && skidmore_dc$license_number != "" && !is.na(skidmore_dc$license_number)) {
  cat("✓ Caitlin Skidmore license number:", skidmore_dc$license_number, "\n")
} else {
  warnings <- append(warnings, "Caitlin Skidmore license number missing or empty")
}

# Check 7: All other employees should be unlicensed
other_employees <- df[df$employee != "Caitlin Skidmore", ]
if (any(other_employees$licensed == TRUE)) {
  licensed_others <- other_employees[other_employees$licensed == TRUE, ]
  issues <- append(issues, paste("Unexpected licensed employees:", paste(unique(licensed_others$employee), collapse = ", ")))
} else {
  cat("✓ All other employees unlicensed\n")
}

# Check 8: Employee name consistency (Edward Hyland vs Edward D Hyland)
hyland_variants <- unique(df$employee[grepl("Hyland", df$employee)])
if (length(hyland_variants) > 1) {
  warnings <- append(warnings, paste("Edward Hyland name variants found:", paste(hyland_variants, collapse = ", ")))
  cat("⚠ Name variant:", paste(hyland_variants, collapse = ", "), "\n")
}

# Check 9: Verify finding files exist
cat("\n9. Finding Files Verification:\n")
state_dirs <- list(
  "Connecticut" = "research/license_searches/connecticut",
  "DC" = "research/license_searches/dc",
  "Maryland" = "research/license_searches/maryland",
  "New Jersey" = "research/license_searches/new_jersey",
  "New York" = "research/license_searches/new_york",
  "Virginia" = "research/license_searches/virginia"
)

for (state_name in names(state_dirs)) {
  dir_path <- state_dirs[[state_name]]
  if (dir.exists(dir_path)) {
    files <- list.files(dir_path, pattern = "*finding.json", full.names = FALSE)
    cat("   ", state_name, ":", length(files), "files")
    if (state_name == "DC" && length(files) >= 12) {
      cat(" ✓\n")
    } else if (state_name != "DC" && length(files) == 15) {
      cat(" ✓\n")
    } else {
      cat(" ⚠ (expected", ifelse(state_name == "DC", "12+", "15"), ")\n")
      warnings <- append(warnings, paste(state_name, "has", length(files), "finding files"))
    }
  } else {
    issues <- append(issues, paste("Directory missing:", dir_path))
  }
}

# Summary
cat("\n=== Verification Summary ===\n")
if (length(issues) == 0 && length(warnings) == 0) {
  cat("✓ ALL CHECKS PASSED - Data is accurate and complete\n")
} else {
  if (length(issues) > 0) {
    cat("\n✗ ISSUES FOUND:\n")
    for (issue in issues) {
      cat("  -", issue, "\n")
    }
  }
  if (length(warnings) > 0) {
    cat("\n⚠ WARNINGS:\n")
    for (warning in warnings) {
      cat("  -", warning, "\n")
    }
  }
}

cat("\n=== Statistics ===\n")
cat("Total findings:", nrow(df), "\n")
cat("Licensed:", sum(df$licensed == TRUE), "\n")
cat("Unlicensed:", sum(df$licensed == FALSE), "\n")
cat("States:", length(unique(df$state)), "\n")
cat("Employees:", length(unique(df$employee)), "\n")

cat("\nVerification complete.\n")
