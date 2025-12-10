#!/usr/bin/env Rscript
# Consolidate License Findings - Simplified Version
#
# This script consolidates all license search findings from JSON files
# and generates comprehensive summary reports.

library(jsonlite)
library(dplyr)

# Set working directory to repo root
if (dir.exists("research")) {
  # Already in repo root
} else if (dir.exists("../research")) {
  setwd("..")
} else if (dir.exists("../../research")) {
  setwd("../..")
}

# Output directory
output_dir <- file.path("research", "license_searches", "consolidated")
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# Initialize results list
all_findings <- list()

# Process New Jersey findings
cat("Processing New Jersey findings...\n")
nj_files <- list.files("research/license_searches/new_jersey", pattern = "*_finding.json", full.names = TRUE)
for (file in nj_files) {
  data <- fromJSON(file)
  if (!is.null(data$findings)) {
    finding_key <- names(data$findings)[1]
    if (!is.null(finding_key)) {
      finding <- data$findings[[finding_key]]
      employee_name <- if (!is.null(finding$full_name)) finding$full_name else gsub("nj_|_finding.json", "", basename(file))
      employee_name <- gsub("_", " ", employee_name)
      employee_name <- stringr::str_to_title(employee_name)

      all_findings[[length(all_findings) + 1]] <- list(
        employee = employee_name,
        state = "New Jersey",
        licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
        license_number = NA,
        license_type = NA,
        status = if (!is.null(finding$results_found) && finding$results_found > 0) "Found" else "Not Found",
        search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
        notes = if (!is.null(finding$note)) finding$note else NA
      )
    }
  }
}

# Process New York findings
cat("Processing New York findings...\n")
ny_files <- list.files("research/license_searches/new_york", pattern = "*_finding.json", full.names = TRUE)
for (file in ny_files) {
  data <- fromJSON(file)
  if (!is.null(data$findings)) {
    finding_key <- names(data$findings)[1]
    if (!is.null(finding_key)) {
      finding <- data$findings[[finding_key]]
      employee_name <- if (!is.null(finding$full_name)) finding$full_name else gsub("ny_|_finding.json", "", basename(file))
      employee_name <- gsub("_", " ", employee_name)
      employee_name <- stringr::str_to_title(employee_name)

      all_findings[[length(all_findings) + 1]] <- list(
        employee = employee_name,
        state = "New York",
        licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
        license_number = NA,
        license_type = NA,
        status = if (!is.null(finding$results_found) && finding$results_found > 0) "Found" else "Not Found",
        search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
        notes = if (!is.null(finding$note)) finding$note else NA
      )
    }
  }
}

# Process DC findings
cat("Processing DC findings...\n")
# First process the original dc_skidmore_licenses_found.json
dc_file <- "research/license_searches/dc/dc_skidmore_licenses_found.json"
if (file.exists(dc_file)) {
  data <- fromJSON(dc_file)
  if (!is.null(data$caitlin_skidmore)) {
    emp_data <- data$caitlin_skidmore
    license_number <- NA
    license_type <- NA

    tryCatch({
      if (!is.null(emp_data$licenses)) {
        if (is.data.frame(emp_data$licenses) && nrow(emp_data$licenses) > 0) {
          license_number <- emp_data$licenses$license_number[1]
          license_type <- emp_data$licenses$license_type[1]
        } else if (is.list(emp_data$licenses) && length(emp_data$licenses) > 0) {
          first_license <- emp_data$licenses[[1]]
          if (is.list(first_license)) {
            license_number <- first_license$license_number
            license_type <- first_license$license_type
          }
        }
      }
    }, error = function(e) {
      # If error, just use NA values
      license_number <<- NA
      license_type <<- NA
    })

    all_findings[[length(all_findings) + 1]] <- list(
      employee = "Caitlin Skidmore",
      state = "DC",
      licensed = TRUE,
      license_number = license_number,
      license_type = license_type,
      status = "Active",
      search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
      notes = if (!is.null(emp_data$note)) emp_data$note else NA
    )
  }

  # Check for Robert Kettler and Edward Hyland
  if (!is.null(data$robert_kettler) && !is.null(data$robert_kettler$results_found) && data$robert_kettler$results_found == 0) {
    all_findings[[length(all_findings) + 1]] <- list(
      employee = "Robert Kettler",
      state = "DC",
      licensed = FALSE,
      license_number = NA,
      license_type = NA,
      status = "Not Found",
      search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
      notes = if (!is.null(data$robert_kettler$note)) data$robert_kettler$note else NA
    )
  }

  if (!is.null(data$edward_hyland) && !is.null(data$edward_hyland$results_found) && data$edward_hyland$results_found == 0) {
    all_findings[[length(all_findings) + 1]] <- list(
      employee = "Edward Hyland",
      state = "DC",
      licensed = FALSE,
      license_number = NA,
      license_type = NA,
      status = "Not Found",
      search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
      notes = if (!is.null(data$edward_hyland$note)) data$edward_hyland$note else NA
    )
  }
}

# Process individual DC finding files
dc_files <- list.files("research/license_searches/dc", pattern = "dc_.*_finding.json", full.names = TRUE)
cat(sprintf("Found %d DC individual finding files\n", length(dc_files)))
for (file in dc_files) {
  # Skip if already processed (dc_skidmore_licenses_found.json)
  if (basename(file) == "dc_skidmore_licenses_found.json") next

  data <- fromJSON(file)
  if (!is.null(data$findings)) {
    finding_key <- names(data$findings)[1]
    if (!is.null(finding_key)) {
      finding <- data$findings[[finding_key]]
      employee_name <- if (!is.null(finding$full_name)) finding$full_name else gsub("dc_|_finding.json", "", basename(file))
      employee_name <- gsub("_", " ", employee_name)
      employee_name <- stringr::str_to_title(employee_name)

      # Skip if already processed from dc_skidmore_licenses_found.json
      if (employee_name == "Caitlin Skidmore" || employee_name == "Robert Kettler" || employee_name == "Edward Hyland") next

      all_findings[[length(all_findings) + 1]] <- list(
        employee = employee_name,
        state = "DC",
        licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
        license_number = NA,
        license_type = NA,
        status = if (!is.null(finding$results_found) && finding$results_found > 0) "Found" else "Not Found",
        search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
        notes = if (!is.null(finding$note)) finding$note else NA
      )
    }
  }
}
cat(sprintf("Processed %d DC findings\n", length(dc_files)))

# Process Maryland findings
cat("Processing Maryland findings...\n")
md_files <- list.files("research/license_searches/maryland", pattern = "*_finding.json", full.names = TRUE)
cat(sprintf("Found %d Maryland finding files\n", length(md_files)))
for (file in md_files) {
  data <- fromJSON(file)
  if (!is.null(data$findings)) {
    finding_key <- names(data$findings)[1]
    if (!is.null(finding_key)) {
      finding <- data$findings[[finding_key]]
      employee_name <- if (!is.null(finding$full_name)) finding$full_name else gsub("md_|_finding.json", "", basename(file))
      employee_name <- gsub("_", " ", employee_name)
      employee_name <- stringr::str_to_title(employee_name)

      # Normalize name variations
      if (grepl("Cynthia.*Fisher|Cindy.*Fisher", employee_name, ignore.case = TRUE)) {
        employee_name <- "Cindy Fisher"
      }
      if (grepl("Christina.*Chang", employee_name, ignore.case = TRUE)) {
        employee_name <- "Christina Chang"
      }

      # Extract license information if licensed
      license_num <- NA
      license_type_val <- NA
      if (!is.null(finding$real_estate_license) && finding$real_estate_license == TRUE) {
        license_num <- if (!is.null(finding$license_number)) finding$license_number else NA
        license_type_val <- if (!is.null(finding$license_type)) finding$license_type else NA
      }

      all_findings[[length(all_findings) + 1]] <- list(
        employee = employee_name,
        state = "Maryland",
        licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
        license_number = license_num,
        license_type = license_type_val,
        status = if (!is.null(finding$results_found) && finding$results_found > 0) {
          if (!is.null(finding$real_estate_license) && finding$real_estate_license == TRUE) "Active" else "Found"
        } else "Not Found",
        search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
        notes = if (!is.null(finding$note)) finding$note else NA
      )
    }
  }
}
cat(sprintf("Processed %d Maryland findings\n", length(md_files)))

# Process Connecticut findings
cat("Processing Connecticut findings...\n")
ct_files <- list.files("research/license_searches/connecticut", pattern = "*_finding.json", full.names = TRUE)
cat(sprintf("Found %d Connecticut finding files\n", length(ct_files)))
for (file in ct_files) {
  data <- fromJSON(file)
  if (!is.null(data$findings)) {
    finding_key <- names(data$findings)[1]
    if (!is.null(finding_key)) {
      finding <- data$findings[[finding_key]]
      employee_name <- if (!is.null(finding$full_name)) finding$full_name else gsub("ct_|_finding.json", "", basename(file))
      employee_name <- gsub("_", " ", employee_name)
      employee_name <- stringr::str_to_title(employee_name)

      all_findings[[length(all_findings) + 1]] <- list(
        employee = employee_name,
        state = "Connecticut",
        licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
        license_number = NA,
        license_type = NA,
        status = if (!is.null(finding$results_found) && finding$results_found > 0) "Found" else "Not Found",
        search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
        notes = if (!is.null(finding$note)) finding$note else NA
      )
    }
  }
}
cat(sprintf("Processed %d Connecticut findings\n", length(ct_files)))

# Process Virginia findings
cat("Processing Virginia findings...\n")
va_files <- list.files("research/license_searches/virginia", pattern = "va_.*_finding.json", full.names = TRUE)
cat(sprintf("Found %d Virginia finding files\n", length(va_files)))
for (file in va_files) {
  data <- fromJSON(file)
  if (!is.null(data$findings)) {
    finding_key <- names(data$findings)[1]
    if (!is.null(finding_key)) {
      finding <- data$findings[[finding_key]]
      employee_name <- if (!is.null(finding$full_name)) finding$full_name else gsub("va_|_finding.json", "", basename(file))
      employee_name <- gsub("_", " ", employee_name)
      employee_name <- stringr::str_to_title(employee_name)

      all_findings[[length(all_findings) + 1]] <- list(
        employee = employee_name,
        state = "Virginia",
        licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
        license_number = NA,
        license_type = NA,
        status = if (!is.null(finding$results_found) && finding$results_found > 0) "Found" else "Not Found",
        search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
        notes = if (!is.null(finding$note)) finding$note else NA
      )
    }
  }
}
cat(sprintf("Processed %d Virginia findings\n", length(va_files)))

# Process Pennsylvania findings
cat("Processing Pennsylvania findings...\n")
pa_files <- list.files("research/license_searches/pennsylvania", pattern = "pa_.*_finding.json", full.names = TRUE)
cat(sprintf("Found %d Pennsylvania finding files\n", length(pa_files)))
for (file in pa_files) {
  data <- fromJSON(file)
  if (!is.null(data$findings)) {
    finding_key <- names(data$findings)[1]
    if (!is.null(finding_key)) {
      finding <- data$findings[[finding_key]]
      employee_name <- if (!is.null(finding$full_name)) finding$full_name else gsub("pa_|_finding.json", "", basename(file))
      employee_name <- gsub("_", " ", employee_name)
      employee_name <- stringr::str_to_title(employee_name)

      all_findings[[length(all_findings) + 1]] <- list(
        employee = employee_name,
        state = "Pennsylvania",
        licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
        license_number = NA,
        license_type = NA,
        status = if (!is.null(finding$results_found) && finding$results_found > 0) "Found" else "Not Found",
        search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
        notes = if (!is.null(finding$note)) finding$note else NA
      )
    }
  }
}
cat(sprintf("Processed %d Pennsylvania findings\n", length(pa_files)))

# Process North Carolina findings
cat("Processing North Carolina findings...\n")
nc_files <- list.files("research/license_searches/north_carolina", pattern = "nc_.*_finding.json", full.names = TRUE)
cat(sprintf("Found %d North Carolina finding files\n", length(nc_files)))
for (file in nc_files) {
  data <- fromJSON(file)
  if (!is.null(data$findings)) {
    finding_key <- names(data$findings)[1]
    if (!is.null(finding_key)) {
      finding <- data$findings[[finding_key]]
      employee_name <- if (!is.null(finding$full_name)) finding$full_name else gsub("nc_|_finding.json", "", basename(file))
      employee_name <- gsub("_", " ", employee_name)
      employee_name <- stringr::str_to_title(employee_name)

      all_findings[[length(all_findings) + 1]] <- list(
        employee = employee_name,
        state = "North Carolina",
        licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
        license_number = NA,
        license_type = NA,
        status = if (!is.null(finding$results_found) && finding$results_found > 0) "Found" else "Not Found",
        search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
        notes = if (!is.null(finding$note)) finding$note else NA
      )
    }
  }
}
cat(sprintf("Processed %d North Carolina findings\n", length(nc_files)))

# Process South Carolina findings
cat("Processing South Carolina findings...\n")
sc_files <- list.files("research/license_searches/south_carolina", pattern = "sc_.*_finding.json", full.names = TRUE)
cat(sprintf("Found %d South Carolina finding files\n", length(sc_files)))
for (file in sc_files) {
  data <- fromJSON(file)
  if (!is.null(data$findings)) {
    finding_key <- names(data$findings)[1]
    if (!is.null(finding_key)) {
      finding <- data$findings[[finding_key]]
      employee_name <- if (!is.null(finding$full_name)) finding$full_name else gsub("sc_|_finding.json", "", basename(file))
      employee_name <- gsub("_", " ", employee_name)
      employee_name <- stringr::str_to_title(employee_name)

      all_findings[[length(all_findings) + 1]] <- list(
        employee = employee_name,
        state = "South Carolina",
        licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
        license_number = NA,
        license_type = NA,
        status = if (!is.null(finding$results_found) && finding$results_found > 0) "Found" else "Not Found",
        search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
        notes = if (!is.null(finding$note)) finding$note else NA
      )
    }
  }
}
cat(sprintf("Processed %d South Carolina findings\n", length(sc_files)))

# Process Georgia findings
cat("Processing Georgia findings...\n")
ga_files <- list.files("research/license_searches/georgia", pattern = "ga_.*_finding.json", full.names = TRUE)
cat(sprintf("Found %d Georgia finding files\n", length(ga_files)))
for (file in ga_files) {
  data <- fromJSON(file)
  if (!is.null(data$findings)) {
    finding_key <- names(data$findings)[1]
    if (!is.null(finding_key)) {
      finding <- data$findings[[finding_key]]
      employee_name <- if (!is.null(finding$full_name)) finding$full_name else gsub("ga_|_finding.json", "", basename(file))
      employee_name <- gsub("_", " ", employee_name)
      employee_name <- stringr::str_to_title(employee_name)

      all_findings[[length(all_findings) + 1]] <- list(
        employee = employee_name,
        state = "Georgia",
        licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
        license_number = NA,
        license_type = NA,
        status = if (!is.null(finding$results_found) && finding$results_found > 0) "Found" else "Not Found",
        search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
        notes = if (!is.null(finding$note)) finding$note else NA
      )
    }
  }
}
cat(sprintf("Processed %d Georgia findings\n", length(ga_files)))

# Process Florida findings
cat("Processing Florida findings...\n")
fl_files <- list.files("research/license_searches/florida", pattern = "fl_.*_finding.json", full.names = TRUE)
cat(sprintf("Found %d Florida finding files\n", length(fl_files)))
for (file in fl_files) {
  data <- fromJSON(file)
  if (!is.null(data$findings)) {
    finding_key <- names(data$findings)[1]
    if (!is.null(finding_key)) {
      finding <- data$findings[[finding_key]]
      employee_name <- if (!is.null(finding$full_name)) finding$full_name else gsub("fl_|_finding.json", "", basename(file))
      employee_name <- gsub("_", " ", employee_name)
      employee_name <- stringr::str_to_title(employee_name)

      all_findings[[length(all_findings) + 1]] <- list(
        employee = employee_name,
        state = "Florida",
        licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
        license_number = NA,
        license_type = NA,
        status = if (!is.null(finding$results_found) && finding$results_found > 0) "Found" else "Not Found",
        search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
        notes = if (!is.null(finding$note)) finding$note else NA
      )
    }
  }
}
cat(sprintf("Processed %d Florida findings\n", length(fl_files)))

# Process Arizona findings
cat("Processing Arizona findings...\n")
az_files <- list.files("research/license_searches/arizona", pattern = "az_.*_finding.json", full.names = TRUE)
cat(sprintf("Found %d Arizona finding files\n", length(az_files)))
for (file in az_files) {
  data <- fromJSON(file)
  if (!is.null(data$findings)) {
    finding_key <- names(data$findings)[1]
    if (!is.null(finding_key)) {
      finding <- data$findings[[finding_key]]
      employee_name <- if (!is.null(finding$full_name)) finding$full_name else gsub("az_|_finding.json", "", basename(file))
      employee_name <- gsub("_", " ", employee_name)
      employee_name <- stringr::str_to_title(employee_name)

      all_findings[[length(all_findings) + 1]] <- list(
        employee = employee_name,
        state = "Arizona",
        licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
        license_number = NA,
        license_type = NA,
        status = if (!is.null(finding$results_found) && finding$results_found > 0) "Found" else "Not Found",
        search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
        notes = if (!is.null(finding$note)) finding$note else NA
      )
    }
  }
}
cat(sprintf("Processed %d Arizona findings\n", length(az_files)))

# Process New Mexico findings
cat("Processing New Mexico findings...\n")
nm_files <- list.files("research/license_searches/new_mexico", pattern = "nm_.*_finding.json", full.names = TRUE)
cat(sprintf("Found %d New Mexico finding files\n", length(nm_files)))
for (file in nm_files) {
  data <- fromJSON(file)
  if (!is.null(data$findings)) {
    finding_key <- names(data$findings)[1]
    if (!is.null(finding_key)) {
      finding <- data$findings[[finding_key]]
      employee_name <- if (!is.null(finding$full_name)) finding$full_name else gsub("nm_|_finding.json", "", basename(file))
      employee_name <- gsub("_", " ", employee_name)
      employee_name <- stringr::str_to_title(employee_name)

      all_findings[[length(all_findings) + 1]] <- list(
        employee = employee_name,
        state = "New Mexico",
        licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
        license_number = NA,
        license_type = NA,
        status = if (!is.null(finding$results_found) && finding$results_found > 0) "Found" else "Not Found",
        search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
        notes = if (!is.null(finding$note)) finding$note else NA
      )
    }
  }
}
cat(sprintf("Processed %d New Mexico findings\n", length(nm_files)))

# Process Utah findings
cat("Processing Utah findings...\n")
ut_files <- list.files("research/license_searches/utah", pattern = "ut_.*_finding.json", full.names = TRUE)
cat(sprintf("Found %d Utah finding files\n", length(ut_files)))
for (file in ut_files) {
  data <- fromJSON(file)
  if (!is.null(data$findings)) {
    finding_key <- names(data$findings)[1]
    if (!is.null(finding_key)) {
      finding <- data$findings[[finding_key]]
      employee_name <- if (!is.null(finding$full_name)) finding$full_name else gsub("ut_|_finding.json", "", basename(file))
      employee_name <- gsub("_", " ", employee_name)
      employee_name <- stringr::str_to_title(employee_name)

      all_findings[[length(all_findings) + 1]] <- list(
        employee = employee_name,
        state = "Utah",
        licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
        license_number = NA,
        license_type = NA,
        status = if (!is.null(finding$results_found) && finding$results_found > 0) "Found" else "Not Found",
        search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
        notes = if (!is.null(finding$note)) finding$note else NA
      )
    }
  }
}
cat(sprintf("Processed %d Utah findings\n", length(ut_files)))

# Process New Jersey findings (for Thomas Bisanz and others)
cat("Processing New Jersey findings...\n")
nj_files <- list.files("research/license_searches/new_jersey", pattern = "nj_.*_finding.json", full.names = TRUE)
cat(sprintf("Found %d New Jersey finding files\n", length(nj_files)))
for (file in nj_files) {
  data <- fromJSON(file)
  if (!is.null(data$findings)) {
    finding_key <- names(data$findings)[1]
    if (!is.null(finding_key)) {
      finding <- data$findings[[finding_key]]
      employee_name <- if (!is.null(finding$full_name)) finding$full_name else gsub("nj_|_finding.json", "", basename(file))
      employee_name <- gsub("_", " ", employee_name)
      employee_name <- stringr::str_to_title(employee_name)

      all_findings[[length(all_findings) + 1]] <- list(
        employee = employee_name,
        state = "New Jersey",
        licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
        license_number = NA,
        license_type = NA,
        status = if (!is.null(finding$results_found) && finding$results_found > 0) "Found" else "Not Found",
        search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
        notes = if (!is.null(finding$note)) finding$note else NA
      )
    }
  }
}
cat(sprintf("Processed %d New Jersey findings\n", length(nj_files)))

# Process New York findings (for Thomas Bisanz and others)
cat("Processing New York findings...\n")
ny_files <- list.files("research/license_searches/new_york", pattern = "ny_.*_finding.json", full.names = TRUE)
cat(sprintf("Found %d New York finding files\n", length(ny_files)))
for (file in ny_files) {
  data <- fromJSON(file)
  if (!is.null(data$findings)) {
    finding_key <- names(data$findings)[1]
    if (!is.null(finding_key)) {
      finding <- data$findings[[finding_key]]
      employee_name <- if (!is.null(finding$full_name)) finding$full_name else gsub("ny_|_finding.json", "", basename(file))
      employee_name <- gsub("_", " ", employee_name)
      employee_name <- stringr::str_to_title(employee_name)

      all_findings[[length(all_findings) + 1]] <- list(
        employee = employee_name,
        state = "New York",
        licensed = if (!is.null(finding$real_estate_license)) finding$real_estate_license else FALSE,
        license_number = NA,
        license_type = NA,
        status = if (!is.null(finding$results_found) && finding$results_found > 0) "Found" else "Not Found",
        search_date = if (!is.null(data$metadata$date)) data$metadata$date else NA,
        notes = if (!is.null(finding$note)) finding$note else NA
      )
    }
  }
}
cat(sprintf("Processed %d New York findings\n", length(ny_files)))

# Convert to dataframe
if (length(all_findings) > 0) {
  findings_df <- do.call(rbind, lapply(all_findings, function(x) {
    data.frame(
      employee = x$employee,
      state = x$state,
      licensed = x$licensed,
      license_number = ifelse(is.na(x$license_number), "", x$license_number),
      license_type = ifelse(is.na(x$license_type), "", x$license_type),
      status = x$status,
      search_date = ifelse(is.na(x$search_date), "", x$search_date),
      notes = ifelse(is.na(x$notes), "", x$notes),
      stringsAsFactors = FALSE
    )
  }))

  # Remove duplicates before saving (keep first occurrence)
  findings_df <- findings_df %>%
    distinct(employee, state, .keep_all = TRUE)

  # Save consolidated findings
  write.csv(findings_df, file.path(output_dir, "all_findings.csv"), row.names = FALSE)
  cat(sprintf("\nSaved %d findings to %s (after deduplication)\n", nrow(findings_df), file.path(output_dir, "all_findings.csv")))

  # Generate summary statistics
  cat("\n=== Summary Statistics ===\n")
  cat("\nBy State:\n")
  state_summary <- findings_df %>%
    group_by(state) %>%
    summarise(
      total = n(),
      licensed = sum(licensed),
      unlicensed = sum(!licensed),
      .groups = 'drop'
    )
  print(state_summary)

  cat("\nBy Employee:\n")
  employee_summary <- findings_df %>%
    group_by(employee) %>%
    summarise(
      total_states = n(),
      licensed_states = sum(licensed),
      unlicensed_states = sum(!licensed),
      licensed_in = paste(state[licensed], collapse = ", "),
      .groups = 'drop'
    )
  employee_summary$licensed_in <- ifelse(employee_summary$licensed_in == "", "None", employee_summary$licensed_in)
  print(employee_summary)

  # Save summaries
  write.csv(state_summary, file.path(output_dir, "summary_by_state.csv"), row.names = FALSE)
  write.csv(employee_summary, file.path(output_dir, "summary_by_employee.csv"), row.names = FALSE)

} else {
  cat("\nNo findings found to consolidate.\n")
}

cat("\n=== Consolidation Complete ===\n")
