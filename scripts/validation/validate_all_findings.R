#!/usr/bin/env Rscript
# Comprehensive validation of all license search findings

library(jsonlite)
library(dplyr)

cat("=== Comprehensive Findings Validation ===\n\n")

# Expected data
CORE_15_EMPLOYEES <- c(
  "Robert Kettler", "Cindy Fisher", "Luke Davis", "Pat Cassada", "Sean Curtin",
  "Robert Grealy", "Todd Bowen", "Amy Groff", "Edward Hyland", "Djene Moyer",
  "Henry Ramos", "Caitlin Skidmore", "Kristina Thoummarath", "Christina Chang",
  "Jeffrey Williams"
)

LARIAT_BROKERS <- c("Leah Douthit", "Liddy Bisanz", "Thomas Bisanz")

ALL_EMPLOYEES <- c(CORE_15_EMPLOYEES, LARIAT_BROKERS)

OPERATIONAL_STATES <- c(
  "Virginia", "DC", "Maryland", "Pennsylvania", "North Carolina",
  "South Carolina", "Georgia", "Florida", "Arizona", "New Mexico", "Utah"
)

ADDITIONAL_STATES <- c("New Jersey", "New York", "Connecticut")

ALL_STATES <- c(OPERATIONAL_STATES, ADDITIONAL_STATES)

# Load consolidated findings
findings_file <- "research/license_searches/consolidated/all_findings.csv"
if (!file.exists(findings_file)) {
  stop(sprintf("Findings file not found: %s", findings_file))
}

df <- read.csv(findings_file, stringsAsFactors = FALSE)
cat(sprintf("Loaded %d findings from CSV\n\n", nrow(df)))

# Validation checks
errors <- list()
warnings <- list()
info <- list()

# 1. Check for duplicates
cat("=== 1. Checking for Duplicates ===\n")
duplicates <- df %>%
  group_by(employee, state) %>%
  summarise(count = n(), .groups = 'drop') %>%
  filter(count > 1)

if (nrow(duplicates) > 0) {
  errors[[length(errors) + 1]] <- list(
    check = "Duplicates",
    message = sprintf("Found %d duplicate (employee, state) pairs", nrow(duplicates)),
    details = duplicates
  )
  cat(sprintf("❌ ERROR: Found %d duplicates\n", nrow(duplicates)))
  print(duplicates)
} else {
  cat("✅ No duplicates found\n")
}
cat("\n")

# 2. Check expected employees
cat("=== 2. Checking Expected Employees ===\n")
found_employees <- unique(df$employee)
missing_employees <- setdiff(ALL_EMPLOYEES, found_employees)
extra_employees <- setdiff(found_employees, ALL_EMPLOYEES)

if (length(missing_employees) > 0) {
  errors[[length(errors) + 1]] <- list(
    check = "Missing Employees",
    message = sprintf("Missing %d expected employees", length(missing_employees)),
    details = missing_employees
  )
  cat(sprintf("❌ ERROR: Missing employees: %s\n", paste(missing_employees, collapse = ", ")))
} else {
  cat("✅ All expected employees found\n")
}

if (length(extra_employees) > 0) {
  warnings[[length(warnings) + 1]] <- list(
    check = "Extra Employees",
    message = sprintf("Found %d unexpected employees", length(extra_employees)),
    details = extra_employees
  )
  cat(sprintf("⚠️  WARNING: Extra employees: %s\n", paste(extra_employees, collapse = ", ")))
}
cat("\n")

# 3. Check expected states
cat("=== 3. Checking Expected States ===\n")
found_states <- unique(df$state)
missing_states <- setdiff(ALL_STATES, found_states)
extra_states <- setdiff(found_states, ALL_STATES)

if (length(missing_states) > 0) {
  errors[[length(errors) + 1]] <- list(
    check = "Missing States",
    message = sprintf("Missing %d expected states", length(missing_states)),
    details = missing_states
  )
  cat(sprintf("❌ ERROR: Missing states: %s\n", paste(missing_states, collapse = ", ")))
} else {
  cat("✅ All expected states found\n")
}

if (length(extra_states) > 0) {
  warnings[[length(warnings) + 1]] <- list(
    check = "Extra States",
    message = sprintf("Found %d unexpected states", length(extra_states)),
    details = extra_states
  )
  cat(sprintf("⚠️  WARNING: Extra states: %s\n", paste(extra_states, collapse = ", ")))
}
cat("\n")

# 4. Check core 15 coverage in operational states
cat("=== 4. Checking Core 15 Coverage in Operational States ===\n")
coverage_check <- df %>%
  filter(employee %in% CORE_15_EMPLOYEES & state %in% OPERATIONAL_STATES) %>%
  group_by(state) %>%
  summarise(
    employees_found = n(),
    expected = length(CORE_15_EMPLOYEES),
    missing = expected - employees_found,
    .groups = 'drop'
  ) %>%
  mutate(complete = employees_found == expected)

incomplete <- coverage_check %>% filter(!complete)
if (nrow(incomplete) > 0) {
  errors[[length(errors) + 1]] <- list(
    check = "Incomplete Coverage",
    message = sprintf("%d operational states have incomplete coverage", nrow(incomplete)),
    details = incomplete
  )
  cat("❌ ERROR: Incomplete coverage:\n")
  print(incomplete)
} else {
  cat("✅ All operational states have complete core 15 coverage\n")
}
cat("\n")

# 5. Validate licensed employees
cat("=== 5. Validating Licensed Employees ===\n")
licensed_df <- df %>% filter(licensed == TRUE)
cat(sprintf("Found %d licensed entries\n", nrow(licensed_df)))

if (nrow(licensed_df) > 0) {
  cat("\nLicensed employees:\n")
  licensed_summary <- licensed_df %>%
    group_by(employee, state) %>%
    summarise(
      license_number = first(license_number),
      license_type = first(license_type),
      .groups = 'drop'
    )
  print(licensed_summary)

  # Verify known licenses
  expected_licenses <- list(
    list(employee = "Caitlin Skidmore", state = "DC", license_number = "BR40000429"),
    list(employee = "Cindy Fisher", state = "Maryland", license_number = "653897"),
    list(employee = "Christina Chang", state = "Maryland", license_number = "5011394")
  )

  for (expected in expected_licenses) {
    found <- licensed_df %>%
      filter(employee == expected$employee &
             state == expected$state &
             license_number == expected$license_number)
    if (nrow(found) == 0) {
      errors[[length(errors) + 1]] <- list(
        check = "Missing Expected License",
        message = sprintf("Expected license not found: %s in %s (%s)",
                          expected$employee, expected$state, expected$license_number)
      )
      cat(sprintf("❌ ERROR: Missing expected license: %s in %s\n",
                  expected$employee, expected$state))
    } else {
      cat(sprintf("✅ Verified: %s in %s (%s)\n",
                  expected$employee, expected$state, expected$license_number))
    }
  }
} else {
  warnings[[length(warnings) + 1]] <- list(
    check = "No Licensed Employees",
    message = "No licensed employees found in dataset"
  )
  cat("⚠️  WARNING: No licensed employees found\n")
}
cat("\n")

# 6. Check data quality
cat("=== 6. Checking Data Quality ===\n")
# Check for missing required fields
required_fields <- c("employee", "state", "licensed")
missing_fields <- sapply(required_fields, function(field) {
  sum(is.na(df[[field]]) | df[[field]] == "")
})

if (any(missing_fields > 0)) {
  errors[[length(errors) + 1]] <- list(
    check = "Missing Required Fields",
    message = "Found missing required field values",
    details = missing_fields[missing_fields > 0]
  )
  cat("❌ ERROR: Missing required fields:\n")
  print(missing_fields[missing_fields > 0])
} else {
  cat("✅ All required fields present\n")
}

# Check license numbers for licensed entries
licensed_without_number <- df %>%
  filter(licensed == TRUE & (is.na(license_number) | license_number == ""))

if (nrow(licensed_without_number) > 0) {
  warnings[[length(warnings) + 1]] <- list(
    check = "Licensed Without License Number",
    message = sprintf("%d licensed entries missing license numbers", nrow(licensed_without_number)),
    details = licensed_without_number %>% select(employee, state)
  )
  cat(sprintf("⚠️  WARNING: %d licensed entries missing license numbers\n",
              nrow(licensed_without_number)))
} else {
  cat("✅ All licensed entries have license numbers\n")
}
cat("\n")

# 7. Verify file counts
cat("=== 7. Verifying File Counts ===\n")
# Count finding files
finding_files <- list.files(
  "research/license_searches",
  pattern = "*_finding.json",
  recursive = TRUE,
  full.names = FALSE
)
finding_files <- finding_files[!grepl("bar_licenses", finding_files)]

expected_files <- length(ALL_EMPLOYEES) * length(ALL_STATES)
actual_files <- length(finding_files)

cat(sprintf("Expected finding files: %d (%d employees × %d states)\n",
            expected_files, length(ALL_EMPLOYEES), length(ALL_STATES)))
cat(sprintf("Actual finding files: %d\n", actual_files))

if (actual_files != expected_files) {
  warnings[[length(warnings) + 1]] <- list(
    check = "File Count Mismatch",
    message = sprintf("Expected %d files, found %d", expected_files, actual_files),
    difference = actual_files - expected_files
  )
  cat(sprintf("⚠️  WARNING: File count mismatch (difference: %d)\n",
              actual_files - expected_files))
} else {
  cat("✅ File count matches expected\n")
}
cat("\n")

# 8. Summary statistics
cat("=== 8. Summary Statistics ===\n")
summary_stats <- df %>%
  summarise(
    total_entries = n(),
    unique_employees = n_distinct(employee),
    unique_states = n_distinct(state),
    licensed_count = sum(licensed == TRUE),
    unlicensed_count = sum(licensed == FALSE),
    licensed_percentage = round(100 * sum(licensed == TRUE) / n(), 2)
  )
print(summary_stats)
info[[length(info) + 1]] <- summary_stats
cat("\n")

# 9. Operational states violations check
cat("=== 9. Operational States Violations Check ===\n")
violations <- df %>%
  filter(state %in% OPERATIONAL_STATES & employee %in% CORE_15_EMPLOYEES) %>%
  group_by(state) %>%
  summarise(
    total = n(),
    licensed = sum(licensed == TRUE),
    unlicensed = sum(licensed == FALSE),
    coverage_rate = round(100 * sum(licensed == TRUE) / n(), 1),
    .groups = 'drop'
  ) %>%
  mutate(has_violation = licensed == 0)

violation_states <- violations %>% filter(has_violation)
cat(sprintf("States with violations: %d out of %d\n",
            nrow(violation_states), length(OPERATIONAL_STATES)))
print(violation_states %>% select(state, licensed, unlicensed, coverage_rate))
info[[length(info) + 1]] <- list(
  type = "Violations",
  violation_states = violation_states$state,
  count = nrow(violation_states)
)
cat("\n")

# Final summary
cat("=== Validation Summary ===\n")
cat(sprintf("Errors: %d\n", length(errors)))
cat(sprintf("Warnings: %d\n", length(warnings)))
cat(sprintf("Info items: %d\n", length(info)))
cat("\n")

if (length(errors) > 0) {
  cat("❌ VALIDATION FAILED - Errors found:\n")
  for (i in seq_along(errors)) {
    cat(sprintf("\nError %d: %s\n", i, errors[[i]]$message))
    if (!is.null(errors[[i]]$details)) {
      print(errors[[i]]$details)
    }
  }
} else {
  cat("✅ VALIDATION PASSED - No errors found\n")
}

if (length(warnings) > 0) {
  cat("\n⚠️  Warnings:\n")
  for (i in seq_along(warnings)) {
    cat(sprintf("\nWarning %d: %s\n", i, warnings[[i]]$message))
    if (!is.null(warnings[[i]]$details)) {
      print(warnings[[i]]$details)
    }
  }
}

# Save validation report
validation_report <- list(
  date = Sys.Date(),
  findings_file = findings_file,
  total_entries = nrow(df),
  errors = errors,
  warnings = warnings,
  info = info,
  summary_stats = summary_stats,
  violations = violations
)

report_file <- "research/license_searches/consolidated/validation_report.json"
write_json(validation_report, report_file, pretty = TRUE, auto_unbox = TRUE)
cat(sprintf("\n✅ Validation report saved to: %s\n", report_file))

cat("\n=== Validation Complete ===\n")
