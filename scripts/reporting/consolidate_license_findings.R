#!/usr/bin/env Rscript
# Consolidate License Findings
#
# This script consolidates all license search findings from JSON files
# and generates comprehensive summary reports.

library(jsonlite)
library(dplyr)
library(stringr)

# Set working directory to repo root
# Try to find repo root by looking for research directory
if (dir.exists("research")) {
  # Already in repo root
} else if (dir.exists("../research")) {
  setwd("..")
} else if (dir.exists("../../research")) {
  setwd("../..")
} else {
  # Default to current directory
  cat("Warning: Could not find repo root, using current directory\n")
}

# Output directory
output_dir <- file.path("research", "license_searches", "consolidated")
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# Employee list
employees <- c(
  "Edward Hyland", "Robert Kettler", "Caitlin Skidmore", "Cindy Fisher",
  "Sean Curtin", "Liddy Bisanz", "Luke Davis", "Pat Cassada",
  "Amy Groff", "Robert Grealy", "Djene Moyer", "Henry Ramos",
  "Kristina Thoummarath", "Christina Chang", "Todd Bowen"
)

# States
states <- c("virginia", "dc", "new_jersey", "new_york", "maryland", "connecticut")
state_names <- c("Virginia", "DC", "New Jersey", "New York", "Maryland", "Connecticut")

# Initialize results dataframe
all_findings <- data.frame(
  employee = character(),
  state = character(),
  licensed = logical(),
  license_number = character(),
  license_type = character(),
  status = character(),
  expiration_date = character(),
  search_date = character(),
  notes = character(),
  stringsAsFactors = FALSE
)

# Function to read finding JSON
read_finding <- function(state_dir, state_abbr, employee_name) {
  # Convert employee name to filename format
  filename <- tolower(employee_name)
  filename <- gsub(" ", "_", filename)
  filepath <- file.path("research", "license_searches", state_dir, paste0(state_abbr, "_", filename, "_finding.json"))

  if (file.exists(filepath)) {
    tryCatch({
      data <- fromJSON(filepath)

      # Extract finding information based on JSON structure
      # Handle different JSON structures

      # Check for DC structure (direct employee keys)
      employee_key <- NULL
      for (key in names(data)) {
        if (grepl(tolower(employee_name), tolower(key), fixed = TRUE) ||
            grepl(tolower(strsplit(employee_name, " ")[[1]][2]), tolower(key), fixed = TRUE)) {
          employee_key <- key
          break
        }
      }

      if (!is.null(employee_key) && !is.null(data[[employee_key]])) {
        # DC structure
        emp_data <- data[[employee_key]]
        licensed <- if (!is.null(emp_data$results_found)) emp_data$results_found > 0 else FALSE
        license_number <- NA
        license_type <- NA

        if (licensed && !is.null(emp_data$licenses) && length(emp_data$licenses) > 0) {
          license_number <- if (!is.null(emp_data$licenses[[1]]$license_number)) emp_data$licenses[[1]]$license_number else NA
          license_type <- if (!is.null(emp_data$licenses[[1]]$license_type)) emp_data$licenses[[1]]$license_type else NA
        }

        return(list(
          licensed = licensed,
          license_number = license_number,
          license_type = license_type,
          status = if (licensed) "Active" else "Not Found",
          expiration_date = NA,
          search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
          notes = if (!is.null(emp_data$note)) emp_data$note else NA
        ))
      }

      # Check for New Jersey/New York structure (findings key)
      if (!is.null(data$findings)) {
        finding_key <- names(data$findings)[1]
        if (!is.null(finding_key)) {
          finding <- data$findings[[finding_key]]
          return(list(
            licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
            license_number = NA,
            license_type = NA,
            status = if (!is.null(finding$results_found) && finding$results_found > 0) "Found" else "Not Found",
            expiration_date = NA,
            search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
            notes = if (!is.null(finding$note)) finding$note else NA
          ))
        }
      }

      # Direct structure
      if (!is.null(data$licensed)) {
        return(list(
          licensed = data$licensed,
          license_number = if (!is.null(data$license_number)) data$license_number else NA,
          license_type = if (!is.null(data$license_type)) data$license_type else NA,
          status = if (!is.null(data$status)) data$status else NA,
          expiration_date = if (!is.null(data$expiration_date)) data$expiration_date else NA,
          search_date = if (!is.null(data$search_date)) data$search_date else NA,
          notes = if (!is.null(data$notes)) paste(data$notes, collapse = "; ") else NA
        ))
      }

      return(NULL)
    }, error = function(e) {
      cat(sprintf("Error reading %s: %s\n", filepath, e$message))
      return(NULL)
    })
  }
  return(NULL)
}

# Collect findings from each state
for (i in seq_along(states)) {
  state <- states[i]
  state_name <- state_names[i]

  # Determine state directory and abbreviation
  if (state == "virginia") {
    state_dir <- "virginia"
    state_abbr <- "va"
  } else if (state == "dc") {
    state_dir <- "dc"
    state_abbr <- "dc"
  } else if (state == "new_jersey") {
    state_dir <- "new_jersey"
    state_abbr <- "nj"
  } else if (state == "new_york") {
    state_dir <- "new_york"
    state_abbr <- "ny"
  } else if (state == "maryland") {
    state_dir <- "maryland"
    state_abbr <- "md"
  } else if (state == "connecticut") {
    state_dir <- "connecticut"
    state_abbr <- "ct"
  }

  cat(sprintf("\nProcessing %s...\n", state_name))

  for (employee in employees) {
    finding <- read_finding(state_dir, state_abbr, employee)

    if (!is.null(finding)) {
      # Extract finding information
      licensed <- if (!is.null(finding$licensed)) finding$licensed else FALSE
      license_number <- if (!is.null(finding$license_number)) finding$license_number else NA
      license_type <- if (!is.null(finding$license_type)) finding$license_type else NA
      status <- if (!is.null(finding$status)) finding$status else NA
      expiration_date <- if (!is.null(finding$expiration_date)) finding$expiration_date else NA
      search_date <- if (!is.null(finding$search_date)) finding$search_date else NA
      notes <- if (!is.null(finding$notes)) paste(finding$notes, collapse = "; ") else NA

      # Add to dataframe
      all_findings <- rbind(all_findings, data.frame(
        employee = employee,
        state = state_name,
        licensed = licensed,
        license_number = ifelse(is.na(license_number), NA, as.character(license_number)),
        license_type = ifelse(is.na(license_type), NA, as.character(license_type)),
        status = ifelse(is.na(status), NA, as.character(status)),
        expiration_date = ifelse(is.na(expiration_date), NA, as.character(expiration_date)),
        search_date = ifelse(is.na(search_date), NA, as.character(search_date)),
        notes = ifelse(is.na(notes), NA, as.character(notes)),
        stringsAsFactors = FALSE
      ))

      cat(sprintf("  %s: %s\n", employee, ifelse(licensed, "LICENSED", "UNLICENSED")))
    }
  }
}

# Save consolidated findings
write.csv(all_findings, file.path(output_dir, "all_findings.csv"), row.names = FALSE)
cat(sprintf("\nSaved consolidated findings to %s\n", file.path(output_dir, "all_findings.csv")))

# Generate summary statistics
summary_stats <- list()

# By state
for (state_name in state_names) {
  state_findings <- all_findings[all_findings$state == state_name, ]
  if (nrow(state_findings) > 0) {
    summary_stats[[state_name]] <- list(
      total_searches = nrow(state_findings),
      licensed = sum(state_findings$licensed, na.rm = TRUE),
      unlicensed = sum(!state_findings$licensed, na.rm = TRUE),
      completion_rate = round((nrow(state_findings) / length(employees)) * 100, 1)
    )
  }
}

# By employee
employee_summary <- data.frame(
  employee = character(),
  total_states_searched = integer(),
  licensed_states = integer(),
  unlicensed_states = integer(),
  licensed_in = character(),
  stringsAsFactors = FALSE
)

for (employee in employees) {
  emp_findings <- all_findings[all_findings$employee == employee, ]
  if (nrow(emp_findings) > 0) {
    licensed_states <- emp_findings[emp_findings$licensed == TRUE, "state"]
    unlicensed_states <- emp_findings[emp_findings$licensed == FALSE, "state"]

    employee_summary <- rbind(employee_summary, data.frame(
      employee = employee,
      total_states_searched = nrow(emp_findings),
      licensed_states = length(licensed_states),
      unlicensed_states = length(unlicensed_states),
      licensed_in = ifelse(length(licensed_states) > 0, paste(licensed_states, collapse = ", "), "None"),
      stringsAsFactors = FALSE
    ))
  }
}

# Save summaries
write_json(summary_stats, file.path(output_dir, "summary_by_state.json"), pretty = TRUE)
write.csv(employee_summary, file.path(output_dir, "summary_by_employee.csv"), row.names = FALSE)

cat("\n=== Summary Statistics ===\n")
cat("\nBy State:\n")
for (state_name in names(summary_stats)) {
  stats <- summary_stats[[state_name]]
  cat(sprintf("%s: %d searches (%d licensed, %d unlicensed) - %.1f%% complete\n",
              state_name, stats$total_searches, stats$licensed, stats$unlicensed, stats$completion_rate))
}

cat("\nBy Employee:\n")
for (i in 1:nrow(employee_summary)) {
  emp <- employee_summary[i, ]
  cat(sprintf("%s: %d states searched, licensed in: %s\n",
              emp$employee, emp$total_states_searched, emp$licensed_in))
}

cat("\n=== Consolidation Complete ===\n")
cat(sprintf("Total findings: %d\n", nrow(all_findings)))
cat(sprintf("Files saved to: %s\n", output_dir))
