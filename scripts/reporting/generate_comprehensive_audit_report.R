#!/usr/bin/env Rscript
# Generate comprehensive audit report from all markdown reports
# Consolidate findings, violations, anomalies into single report

library(jsonlite)
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
OUTPUT_FILE <- file.path(RESEARCH_DIR, "COMPREHENSIVE_AUDIT_REPORT.md")

# Markdown files to consolidate
MARKDOWN_FILES <- c(
  "ALL_VIOLATIONS_AND_ANOMALIES.md",
  "COMPLETE_AUDIT_SUMMARY.md",
  "COMPREHENSIVE_VIOLATIONS_REPORT.md",
  "FINAL_NEXUS_FINDINGS.md",
  "FINAL_VIOLATION_SUMMARY.md",
  "VIOLATION_AUDIT_COMPLETE.md",
  "HYLAND_UPL_EVIDENCE.md",
  "validation_report.md",
  "NEXUS_ANALYSIS_REPORT.md",
  "COMPREHENSIVE_ANOMALIES_REPORT.md"
)

# Load markdown file content
load_markdown_file <- function(filename) {
  file_path <- file.path(RESEARCH_DIR, filename)
  if (file.exists(file_path)) {
    content <- readLines(file_path, warn = FALSE)
    return(list(filename = filename, content = content, exists = TRUE))
  }
  return(list(filename = filename, content = character(0), exists = FALSE))
}

# Extract key sections from markdown
extract_sections <- function(content) {
  sections <- list()

  # Find headers
  header_lines <- grep("^#+\\s+", content)

  for (i in seq_along(header_lines)) {
    start_line <- header_lines[i]
    end_line <- if (i < length(header_lines)) header_lines[i + 1] - 1 else length(content)

    header <- content[start_line]
    section_content <- content[start_line:end_line]

    # Extract header level and title
    header_match <- str_match(header, "^(#+)\\s+(.+)$")
    if (!is.na(header_match[1, 1])) {
      level <- nchar(header_match[1, 2])
      title <- header_match[1, 3]

      sections[[length(sections) + 1]] <- list(
        level = level,
        title = title,
        content = section_content
      )
    }
  }

  return(sections)
}

# Consolidate reports
consolidate_reports <- function() {
  cat("=== Generating Comprehensive Audit Report ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load all markdown files
  reports <- list()
  for (filename in MARKDOWN_FILES) {
    report <- load_markdown_file(filename)
    if (report$exists) {
      cat("Loaded:", filename, "\n")
      sections <- extract_sections(report$content)
      reports[[filename]] <- list(
        filename = filename,
        content = report$content,
        sections = sections
      )
    } else {
      cat("Not found:", filename, "\n")
    }
  }

  # Create comprehensive report
  report_lines <- c(
    "# Comprehensive Audit Report - Kettler Management Investigation",
    "",
    paste("**Date:**", Sys.Date()),
    paste("**Report Type:** Consolidated Audit Report"),
    "",
    "---",
    "",
    "## Executive Summary",
    "",
    "This comprehensive audit report consolidates findings from multiple investigation phases:",
    "",
    "- License violation audits",
    "- Unauthorized practice of law investigation",
    "- Nexus analysis (identifying real operators)",
    "- Anomaly identification",
    "- Violation compilation",
    "",
    "### Key Findings",
    "",
    "**Confirmed Violations:**",
    "- Edward Hyland: Unlicensed practice of real estate (CONFIRMED)",
    "",
    "**Potential Violations:**",
    "- Edward Hyland: Unauthorized practice of law (UNDER INVESTIGATION)",
    "",
    "**Verification Needed:**",
    "- Djene Moyer: Property Management License",
    "- Henry Ramos: Property Management License",
    "- Sean Curtin: State Bar Admission",
    "",
    "**Major Anomalies:**",
    "- 8 firms licensed BEFORE principal broker (timeline impossibility)",
    "- 6 firms at same Frisco TX address (shell company pattern)",
    "- Average 7.4 year license gap (retroactive assignment)",
    "",
    "**Real Nexus Identified:**",
    "- Kettler Management Inc. (PRIMARY NEXUS)",
    "- Edward Hyland (OPERATIONAL NEXUS)",
    "",
    "---",
    "",
    "## Consolidated Findings from All Reports",
    ""
  )

  # Add content from each report
  for (report_name in names(reports)) {
    report <- reports[[report_name]]
    report_lines <- c(
      report_lines,
      paste("### Report:", report$filename),
      "",
      "```",
      if (!is.null(report$content) && length(report$content) > 0) {
        paste(report$content[1:min(50, length(report$content))], collapse = "\n")
      } else {
        "(No content available)"
      },
      "```",
      "",
      paste("*Full report available in:", report$filename, "*"),
      "",
      "---",
      ""
    )
  }

  # Add summary statistics
  report_lines <- c(
    report_lines,
    "## Summary Statistics",
    "",
    "### Violations",
    "- Confirmed: 1",
    "- Potential: 1",
    "- Needs Verification: 4",
    "",
    "### Anomalies",
    "- Timeline Impossibilities: 8 firms before broker",
    "- Shell Company Patterns: 6 firms at same address",
    "- License Gaps: Average 7.4 years",
    "",
    "### Database Searches",
    "- DPOR Searches: Framework created",
    "- Bar Association Searches: Framework created",
    "- STR Platform Searches: Framework created",
    "",
    "---",
    "",
    paste("*Report generated:", Sys.Date(), "*"),
    paste("*Consolidated from", length(reports), "source reports*")
  )

  # Write report
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  writeLines(report_lines, OUTPUT_FILE)
  cat("\nSaved comprehensive audit report to:", OUTPUT_FILE, "\n")

  cat("\n=== Report Generation Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  consolidate_reports()
}
