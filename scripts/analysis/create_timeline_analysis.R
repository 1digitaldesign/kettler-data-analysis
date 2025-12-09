#!/usr/bin/env Rscript
# Create master timeline combining all dates
# Identify anomalies, detect patterns, analyze causation

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
EVIDENCE_DIR <- file.path(PROJECT_ROOT, "evidence")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "timeline_analysis.json")

# Load all dates from all sources
load_all_dates <- function() {
  timeline <- list()

  # Load firms data
  firms_file <- file.path(DATA_DIR, "source", "skidmore_all_firms_complete.csv")
  if (file.exists(firms_file)) {
    firms <- read.csv(firms_file, stringsAsFactors = FALSE)

    # Parse firm license dates
    if (nrow(firms) > 0) {
      for (i in 1:nrow(firms)) {
      if (firms$Initial.Cert.Date[i] != "DATA MISSING" &&
          !is.na(firms$Initial.Cert.Date[i]) &&
          firms$Initial.Cert.Date[i] != "") {
        parsed_date <- tryCatch({
          as.Date(firms$Initial.Cert.Date[i], format = "%Y-%m-%d")
        }, error = function(e) NA)

        if (!is.na(parsed_date)) {
          timeline[[length(timeline) + 1]] <- list(
            date = as.character(parsed_date),
            event_type = "firm_license_issued",
            entity = firms$Firm.Name[i],
            details = paste("License Number:", firms$License.Number[i])
          )
        }
      }
    }
    }
  }

  # Skidmore license date
  timeline[[length(timeline) + 1]] <- list(
    date = "2025-05-30",
    event_type = "skidmore_licensed",
    entity = "Caitlin Skidmore",
    details = "Individual real estate license issued"
  )

  # Hyland employment start
  timeline[[length(timeline) + 1]] <- list(
    date = "2022-09-01",
    event_type = "hyland_employment_start",
    entity = "Edward Hyland",
    details = "Started at Kettler Management as Senior Regional Manager"
  )

  # Load evidence dates
  entities_file <- file.path(RESEARCH_DIR, "all_entities_extracted.json")
  if (file.exists(entities_file)) {
    entities <- fromJSON(entities_file, simplifyDataFrame = FALSE)

    # Parse dates from evidence
    if (!is.null(entities$dates) && length(entities$dates) > 0) {
      for (date_str in entities$dates) {
      # Try to parse various date formats
      parsed_date <- tryCatch({
        as.Date(date_str, format = "%B %d, %Y")
      }, error = function(e) {
        tryCatch({
          as.Date(date_str, format = "%m/%d/%Y")
        }, error = function(e) NA)
      })

      if (!is.na(parsed_date)) {
        timeline[[length(timeline) + 1]] <- list(
          date = as.character(parsed_date),
          event_type = "evidence_date",
          entity = "Evidence",
          details = date_str
        )
      }
    }
    }
  }

  return(timeline)
}

# Identify timeline anomalies
identify_anomalies <- function(timeline, firms) {
  cat("\n=== Identifying Timeline Anomalies ===\n")

  anomalies <- list()

  # Convert timeline to data frame for easier analysis
  if (length(timeline) == 0) {
    return(data.frame(date = as.Date(character(0)), event_type = character(0), entity = character(0)))
  }
  timeline_df <- data.frame(
    date = sapply(timeline, function(x) ifelse(is.null(x$date), NA, x$date)),
    event_type = sapply(timeline, function(x) ifelse(is.null(x$event_type), NA, x$event_type)),
    entity = sapply(timeline, function(x) ifelse(is.null(x$entity), NA, x$entity)),
    stringsAsFactors = FALSE
  )
  timeline_df <- timeline_df[!is.na(timeline_df$date), ]
  if (nrow(timeline_df) > 0) {
    timeline_df$date <- as.Date(timeline_df$date)
    timeline_df <- timeline_df[order(timeline_df$date), ]
  }

  # Anomaly 1: Firms licensed before principal broker
  skidmore_date <- as.Date("2025-05-30")
  firm_dates <- timeline_df[timeline_df$event_type == "firm_license_issued", ]
  firms_before <- firm_dates[firm_dates$date < skidmore_date, ]

  anomalies$firms_before_broker <- list(
    count = nrow(firms_before),
    firms = firms_before$entity,
    anomaly = "Firms cannot have principal broker who wasn't licensed when firm was established"
  )

  # Anomaly 2: Firms licensed after Skidmore but listed as principal broker
  firms_after <- firm_dates[firm_dates$date > skidmore_date, ]

  anomalies$firms_after_broker <- list(
    count = nrow(firms_after),
    firms = firms_after$entity,
    anomaly = "Firms licensed after Skidmore but she's listed as principal broker from start"
  )

  # Anomaly 3: Hyland started at Kettler before many firms were licensed
  hyland_date <- as.Date("2022-09-01")
  firms_after_hyland <- firm_dates[firm_dates$date > hyland_date, ]

  anomalies$firms_after_hyland_start <- list(
    count = nrow(firms_after_hyland),
    firms = firms_after_hyland$entity,
    anomaly = "Firms licensed after Hyland started at Kettler - suggests operational connection"
  )

  return(anomalies)
}

# Detect patterns
detect_patterns <- function(timeline, firms) {
  cat("\n=== Detecting Patterns ===\n")

  patterns <- list()

  # Pattern 1: Clustering of firm licenses around certain dates
  if (length(timeline) == 0) {
    firm_dates <- as.Date(character(0))
  } else {
    firm_dates <- sapply(timeline, function(x) {
      if (!is.null(x$event_type) && x$event_type == "firm_license_issued" && !is.null(x$date)) {
        return(x$date)
      }
      return(NA)
    })
    firm_dates <- firm_dates[!is.na(firm_dates)]
    if (length(firm_dates) > 0) {
      firm_dates <- as.Date(firm_dates)
    } else {
      firm_dates <- as.Date(character(0))
    }
  }

  # Group by year
  firm_years <- format(firm_dates, "%Y")
  year_counts <- table(firm_years)

  patterns$license_clustering <- list(
    peak_years = names(year_counts)[year_counts > 1],
    explanation = "Multiple firms licensed in same year suggests coordinated effort"
  )

  # Pattern 2: Recent licensing activity
  recent_firms <- firm_dates[firm_dates > as.Date("2024-01-01")]
  patterns$recent_activity <- list(
    count = length(recent_firms),
    dates = as.character(recent_firms),
    explanation = "Recent licensing activity may indicate scheme expansion"
  )

  return(patterns)
}

# Analyze causation
analyze_causation <- function(timeline, firms) {
  cat("\n=== Analyzing Causation ===\n")

  causation <- list()

  # Hypothesis: Kettler is the real nexus
  kettler_firm <- firms[firms$Firm.Name == "KETTLER MANAGEMENT INC", ]
  if (nrow(kettler_firm) > 0 && "Initial.Cert.Date" %in% names(kettler_firm)) {
    kettler_date <- tryCatch({
      as.Date(kettler_firm$Initial.Cert.Date[1], format = "%Y-%m-%d")
    }, error = function(e) NA)

    if (!is.na(kettler_date)) {
      # Count firms licensed after Kettler
      if (length(timeline) == 0) {
        firm_dates <- as.Date(character(0))
      } else {
        firm_dates <- sapply(timeline, function(x) {
          if (!is.null(x$event_type) && x$event_type == "firm_license_issued" && !is.null(x$date)) {
            return(x$date)
          }
          return(NA)
        })
        firm_dates <- firm_dates[!is.na(firm_dates)]
        if (length(firm_dates) > 0) {
          firm_dates <- as.Date(firm_dates)
        } else {
          firm_dates <- as.Date(character(0))
        }
      }

      firms_after_kettler <- firm_dates[firm_dates > kettler_date]

      causation$kettler_precedence <- list(
        kettler_licensed = as.character(kettler_date),
        firms_licensed_after = length(firms_after_kettler),
        hypothesis = "Kettler may have been the first, with other firms added later"
      )
    }
  }

  # Hypothesis: Hyland's employment correlates with firm licensing
  hyland_date <- as.Date("2022-09-01")
  if (length(timeline) == 0) {
    firm_dates <- as.Date(character(0))
  } else {
    firm_dates <- sapply(timeline, function(x) {
      if (!is.null(x$event_type) && x$event_type == "firm_license_issued" && !is.null(x$date)) {
        return(x$date)
      }
      return(NA)
    })
    firm_dates <- firm_dates[!is.na(firm_dates)]
    if (length(firm_dates) > 0) {
      firm_dates <- as.Date(firm_dates)
    } else {
      firm_dates <- as.Date(character(0))
    }
  }

  firms_after_hyland <- if (length(firm_dates) > 0) firm_dates[firm_dates > hyland_date] else as.Date(character(0))

  causation$hyland_correlation <- list(
    hyland_started = "2022-09-01",
    firms_licensed_after = length(firms_after_hyland),
    hypothesis = "Hyland's employment may correlate with scheme expansion"
  )

  return(causation)
}

# Main function
main_analysis <- function() {
  cat("=== Timeline Analysis ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load firms
  firms_file <- file.path(DATA_DIR, "source", "skidmore_all_firms_complete.csv")
  if (!file.exists(firms_file)) {
    stop("Firms file not found: ", firms_file)
  }
  firms <- read.csv(firms_file, stringsAsFactors = FALSE)

  # Load all dates
  timeline <- load_all_dates()
  cat("Loaded", length(timeline), "timeline events\n")

  # Identify anomalies
  anomalies <- identify_anomalies(timeline, firms)

  # Detect patterns
  patterns <- detect_patterns(timeline, firms)

  # Analyze causation
  causation <- analyze_causation(timeline, firms)

  # Create results
  results <- list(
    analysis_date = as.character(Sys.Date()),
    total_events = length(timeline),
    timeline = timeline,
    anomalies = anomalies,
    patterns = patterns,
    causation = causation,
    summary = list(
      firms_before_broker = anomalies$firms_before_broker$count,
      firms_after_broker = anomalies$firms_after_broker$count,
      firms_after_hyland = anomalies$firms_after_hyland_start$count,
      recent_activity = patterns$recent_activity$count
    )
  )

  # Save results
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved results to:", OUTPUT_FILE, "\n")

  # Print summary
  cat("\n=== Timeline Summary ===\n")
  cat("Total Events:", results$total_events, "\n")
  cat("Firms Licensed Before Broker:", results$summary$firms_before_broker, "\n")
  cat("Firms Licensed After Broker:", results$summary$firms_after_broker, "\n")
  cat("Firms Licensed After Hyland Start:", results$summary$firms_after_hyland, "\n")
  cat("Recent Activity (2024+):", results$summary$recent_activity, "\n")

  cat("\n=== Analysis Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  main_analysis()
}
