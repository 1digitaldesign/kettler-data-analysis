#!/usr/bin/env Rscript
# Extract Evidence from PDF Documents
# Extracts text and metadata from PDF files for fraud investigation

library(pdftools)
library(stringr)
library(jsonlite)

# Configuration
# Navigate to project root (two levels up from scripts/extraction)
if (basename(getwd()) == "extraction") {
  project_root <- normalizePath(file.path(getwd(), "..", ".."))
} else {
  project_root <- getwd()
}

# Process PDFs from multiple subdirectories
EVIDENCE_SUBDIRS <- c(
  "pdfs",
  "emails",
  "legal_documents",
  "linkedin_profiles",
  "airbnb",
  "accommodation_forms",
  "correspondence"
)

OUTPUT_DIR <- file.path(project_root, "research")
dir.create(OUTPUT_DIR, showWarnings = FALSE, recursive = TRUE)

cat("Project root:", project_root, "\n")
cat("Output directory:", OUTPUT_DIR, "\n")

# Extract text from PDF
extract_pdf_text <- function(pdf_path) {
  tryCatch({
    text <- pdf_text(pdf_path)
    return(paste(text, collapse = "\n"))
  }, error = function(e) {
    cat("Error extracting text from", pdf_path, ":", e$message, "\n")
    return("")
  })
}

# Extract metadata from PDF
extract_pdf_metadata <- function(pdf_path) {
  tryCatch({
    info <- pdf_info(pdf_path)
    return(list(
      title = info$title,
      author = info$author,
      creator = info$creator,
      producer = info$producer,
      creation_date = info$created,
      modification_date = info$modified,
      pages = info$pages,
      file_size = file.info(pdf_path)$size
    ))
  }, error = function(e) {
    return(list())
  })
}

  # Extract entities from text (emails, phone numbers, addresses, dates)
extract_entities <- function(text) {
  entities <- list()

  # Email addresses
  email_pattern <- "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"
  entities$emails <- unique(unlist(str_extract_all(text, email_pattern)))

  # Phone numbers
  phone_pattern <- "\\b(\\+?1[-.]?)?\\(?([0-9]{3})\\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\\b"
  entities$phones <- unique(unlist(str_extract_all(text, phone_pattern)))

  # Dates
  date_pattern <- "(?i)\\b(\\d{1,2}[/-]\\d{1,2}[/-]\\d{2,4}|\\d{4}[-]\\d{2}[-]\\d{2}|(January|February|March|April|May|June|July|August|September|October|November|December)\\s+\\d{1,2},?\\s+\\d{4})\\b"
  entities$dates <- unique(unlist(str_extract_all(text, regex(date_pattern, ignore_case = TRUE))))

  # Addresses (basic pattern)
  address_pattern <- "(?i)\\d+\\s+[A-Za-z0-9\\s,.-]+(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Boulevard|Blvd|Lane|Ln|Court|Ct|Way|Place|Pl)[^,]*,\\s*[A-Za-z\\s]+,\\s*[A-Z]{2}\\s+\\d{5}"
  entities$addresses <- unique(unlist(str_extract_all(text, regex(address_pattern, ignore_case = TRUE))))

  # Unit numbers
  unit_pattern <- "(?i)Unit\\s+(\\d+[A-Z]?|[A-Z]\\d+)"
  entities$units <- unique(unlist(str_extract_all(text, regex(unit_pattern, ignore_case = TRUE))))

  # License numbers
  license_pattern <- "\\b\\d{6,12}\\b"
  entities$license_numbers <- unique(unlist(str_extract_all(text, license_pattern)))

  # Company/Firm names (capitalized words)
  firm_pattern <- "\\b([A-Z][a-z]+\\s+)+(Inc|LLC|Corporation|Corp|Company|Co|Ltd|Limited|Management|Partners|Properties|Residential|Services)\\b"
  entities$firms <- unique(unlist(str_extract_all(text, firm_pattern)))

  return(entities)
}

# Extract key information for regulatory filings
extract_regulatory_info <- function(text) {
  info <- list()

  # Violation keywords
  violation_keywords <- c(
    "violation", "violate", "illegal", "unlawful", "fraud", "fraudulent",
    "misrepresentation", "deceptive", "breach", "non-compliance",
    "unauthorized", "improper", "wrongful", "negligent", "negligence"
  )

  info$violation_mentions <- sapply(violation_keywords, function(keyword) {
    pattern <- paste0("(?i)\\b", keyword, "\\b")
    matches <- unlist(str_extract_all(text, regex(pattern, ignore_case = TRUE)))
    return(length(matches))
  })

  # Regulatory agency mentions
  agency_keywords <- c(
    "DPOR", "Department of Professional", "Real Estate Commission",
    "HUD", "Housing and Urban Development", "FTC", "Federal Trade Commission",
    "SEC", "Securities and Exchange", "IRS", "Internal Revenue",
    "BBB", "Better Business Bureau", "Attorney General", "Consumer Protection"
  )

  info$agency_mentions <- sapply(agency_keywords, function(keyword) {
    pattern <- paste0("(?i)", keyword)
    matches <- unlist(str_extract_all(text, regex(pattern, ignore_case = TRUE)))
    return(length(matches))
  })

  # Lease/rental terms
  lease_keywords <- c(
    "lease", "rental", "tenant", "landlord", "eviction", "termination",
    "security deposit", "rent", "maintenance", "repair"
  )

  info$lease_mentions <- sapply(lease_keywords, function(keyword) {
    pattern <- paste0("(?i)\\b", keyword, "\\b")
    matches <- unlist(str_extract_all(text, regex(pattern, ignore_case = TRUE)))
    return(length(matches))
  })

  return(info)
}

# Process all PDFs in evidence directory and subdirectories
process_all_pdfs <- function() {
  # Collect PDFs from all subdirectories
  pdf_files <- character(0)
  evidence_base <- file.path(project_root, "evidence")

  for (subdir in EVIDENCE_SUBDIRS) {
    subdir_path <- file.path(evidence_base, subdir)
    if (dir.exists(subdir_path)) {
      files <- list.files(subdir_path, pattern = "\\.pdf$", full.names = TRUE, ignore.case = TRUE, recursive = TRUE)
      pdf_files <- c(pdf_files, files)
    }
  }

  # Also check root evidence directory
  root_files <- list.files(evidence_base, pattern = "\\.pdf$", full.names = TRUE, ignore.case = TRUE)
  pdf_files <- c(pdf_files, root_files)

  # Remove duplicates
  pdf_files <- unique(pdf_files)

  if (length(pdf_files) == 0) {
    cat("No PDF files found in evidence directories\n")
    return()
  }

  cat("Processing", length(pdf_files), "PDF file(s)...\n\n")

  all_extracted <- list()

  for (pdf_file in pdf_files) {
    cat("Processing:", basename(pdf_file), "\n")

    # Extract text
    text <- extract_pdf_text(pdf_file)

    if (nchar(text) == 0) {
      cat("  Warning: No text extracted from", basename(pdf_file), "\n")
      next
    }

    # Extract metadata
    metadata <- extract_pdf_metadata(pdf_file)

    # Extract entities
    entities <- extract_entities(text)

    # Extract regulatory information
    regulatory_info <- extract_regulatory_info(text)

    # Combine all information
    extracted <- list(
      file = basename(pdf_file),
      file_path = pdf_file,
      metadata = metadata,
      text_length = nchar(text),
      text_preview = if (!is.null(text) && !is.na(text) && nchar(text) > 0) substr(text, 1, 500) else "",
      entities = entities,
      regulatory_info = regulatory_info
    )

    all_extracted[[length(all_extracted) + 1]] <- extracted

    cat("  Extracted", length(entities$emails), "emails,",
        length(entities$addresses), "addresses,",
        length(entities$firms), "firms\n")
  }

  # Save extracted data
  output_file <- file.path(OUTPUT_DIR, "pdf_evidence_extracted.json")
  write_json(all_extracted, output_file, pretty = TRUE)
  cat("\nSaved extracted data to:", output_file, "\n")

  # Create summary CSV
  summary_data <- data.frame(
    file = sapply(all_extracted, function(x) x$file),
    emails = sapply(all_extracted, function(x) length(x$entities$emails)),
    addresses = sapply(all_extracted, function(x) length(x$entities$addresses)),
    firms = sapply(all_extracted, function(x) length(x$entities$firms)),
    violation_mentions = sapply(all_extracted, function(x) sum(x$regulatory_info$violation_mentions)),
    agency_mentions = sapply(all_extracted, function(x) sum(x$regulatory_info$agency_mentions)),
    stringsAsFactors = FALSE
  )

  summary_file <- file.path(OUTPUT_DIR, "pdf_evidence_summary.csv")
  write.csv(summary_data, summary_file, row.names = FALSE)
  cat("Saved summary to:", summary_file, "\n")

  return(all_extracted)
}

# Main execution
if (!interactive()) {
  # Check if pdftools is installed
  if (!require(pdftools, quietly = TRUE)) {
    cat("Installing pdftools package...\n")
    install.packages("pdftools", repos = "https://cran.rstudio.com/")
    library(pdftools)
  }

  process_all_pdfs()
}
