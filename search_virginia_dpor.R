#!/usr/bin/env Rscript
# Virginia DPOR License Search Implementation
# State-specific search functions for Virginia DPOR website

library(httr)
library(rvest)
library(dplyr)
library(stringr)

# Load httr functions explicitly
POST <- httr::POST
GET <- httr::GET
status_code <- httr::status_code
content <- httr::content
add_headers <- httr::add_headers
timeout <- httr::timeout

# Virginia DPOR uses an iframe-based search system
VIRGINIA_BASE_URL <- "https://dporweb.dpor.virginia.gov/LicenseLookup"
VIRGINIA_SEARCH_URL <- "https://dporweb.dpor.virginia.gov/LicenseLookup/Search"

# Search Virginia DPOR for a firm or individual
search_virginia_dpor <- function(search_term, search_type = "firm") {
  tryCatch({
    # Virginia DPOR uses an iframe, so we need to access the actual search endpoint
    # Try direct POST request to the search URL
    search_url <- "https://dporweb.dpor.virginia.gov/LicenseLookup/Search"

    # Make POST request with search term
    response <- POST(
      search_url,
      body = list("search-text" = search_term),
      encode = "form",
      add_headers(
        "User-Agent" = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer" = "https://www.dpor.virginia.gov/LicenseLookup",
        "Accept" = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
      ),
      timeout(30)
    )

    if (status_code(response) == 200) {
      # Parse results
      results <- parse_virginia_results(response, search_term, search_type)
      return(results)
    } else {
      cat("HTTP error:", status_code(response), "\n")
      return(data.frame())
    }
  }, error = function(e) {
    cat("Error searching Virginia DPOR:", e$message, "\n")
    return(data.frame())
  })
}

# Parse Virginia DPOR search results
parse_virginia_results <- function(response, search_term, search_type) {
  tryCatch({
    # Handle both response object and raw HTML
    if (inherits(response, "response") || inherits(response, "session")) {
      html <- read_html(response)
    } else {
      html <- read_html(response)
    }

    # Initialize results dataframe
    results <- data.frame(
      state = character(),
      search_term = character(),
      license_number = character(),
      name = character(),
      address = character(),
      license_type = character(),
      expiration_date = character(),
      status = character(),
      principal_broker = character(),
      initial_cert_date = character(),
      stringsAsFactors = FALSE
    )

    # Look for results table
    # Virginia DPOR typically displays results in tables
    tables <- html %>% html_nodes("table")

    if (length(tables) > 0) {
      # Try to parse each table
      for (table in tables) {
        table_data <- tryCatch({
          html_table(table, fill = TRUE, header = TRUE)
        }, error = function(e) {
          return(NULL)
        })

        if (!is.null(table_data) && nrow(table_data) > 0) {
          # Standardize column names (Virginia DPOR may use different column names)
          col_names <- tolower(colnames(table_data))

          # Map common column name variations
          license_matches <- grep("license|lic#|lic no", col_names, value = TRUE)
          license_col <- if (length(license_matches) > 0) license_matches[1] else NULL
          name_matches <- grep("name|licensee|company", col_names, value = TRUE)
          name_col <- if (length(name_matches) > 0) name_matches[1] else NULL
          address_matches <- grep("address|location", col_names, value = TRUE)
          address_col <- if (length(address_matches) > 0) address_matches[1] else NULL
          type_matches <- grep("type|license type", col_names, value = TRUE)
          type_col <- if (length(type_matches) > 0) type_matches[1] else NULL
          exp_matches <- grep("expir|exp date|expiration", col_names, value = TRUE)
          exp_col <- if (length(exp_matches) > 0) exp_matches[1] else NULL
          status_matches <- grep("status|active", col_names, value = TRUE)
          status_col <- if (length(status_matches) > 0) status_matches[1] else NULL

          # Extract data
          for (i in 1:nrow(table_data)) {
            row <- table_data[i, ]

            result_row <- data.frame(
              state = "VA",
              search_term = search_term,
              license_number = if (!is.null(license_col)) as.character(row[[license_col]]) else "",
              name = if (!is.null(name_col)) as.character(row[[name_col]]) else "",
              address = if (!is.null(address_col)) as.character(row[[address_col]]) else "",
              license_type = if (!is.null(type_col)) as.character(row[[type_col]]) else "",
              expiration_date = if (!is.null(exp_col)) as.character(row[[exp_col]]) else "",
              status = if (!is.null(status_col)) as.character(row[[status_col]]) else "",
              principal_broker = "",
              initial_cert_date = "",
              stringsAsFactors = FALSE
            )

            results <- rbind(results, result_row)
          }
        }
      }
    }

    # Also check for div-based results (some states use divs instead of tables)
    result_divs <- html %>% html_nodes("div.result, div.license-result, div.search-result")

    if (length(result_divs) > 0 && nrow(results) == 0) {
      for (div in result_divs) {
        # Extract text content
        text_content <- html_text(div)

        # Try to extract license number (typically formatted as numbers)
        license_match <- str_extract(text_content, "\\d{10,}")

        # Extract name (usually first line or bold text)
        name_elem <- div %>% html_node("strong, h3, h4, .name")
        name <- if (!is.null(name_elem)) html_text(name_elem) else ""

        # Extract address
        address_elem <- div %>% html_node(".address, .location")
        address <- if (!is.null(address_elem)) html_text(address_elem) else ""

        if (nchar(name) > 0 || !is.na(license_match)) {
          result_row <- data.frame(
            state = "VA",
            search_term = search_term,
            license_number = if (!is.na(license_match)) license_match else "",
            name = name,
            address = address,
            license_type = "",
            expiration_date = "",
            status = "",
            principal_broker = "",
            initial_cert_date = "",
            stringsAsFactors = FALSE
          )

          results <- rbind(results, result_row)
        }
      }
    }

    # Clean up results
    results <- results %>%
      filter(nchar(name) > 0 | nchar(license_number) > 0) %>%
      distinct()

    return(results)
  }, error = function(e) {
    cat("Error parsing Virginia results:", e$message, "\n")
    return(data.frame())
  })
}

# Search for a specific firm in Virginia
search_firm_virginia <- function(firm_name) {
  name_variations <- c(
    firm_name,
    str_remove(firm_name, "\\s+(Inc|LLC|Corporation|Corp|Company|Co)$"),
    paste0(str_remove(firm_name, "\\s+(Inc|LLC|Corporation|Corp|Company|Co)$"), " Inc"),
    paste0(str_remove(firm_name, "\\s+(Inc|LLC|Corporation|Corp|Company|Co)$"), " LLC")
  )

  all_results <- data.frame()

  for (variation in unique(name_variations)) {
    cat("Searching Virginia for:", variation, "\n")
    results <- search_virginia_dpor(variation, "firm")

    if (nrow(results) > 0) {
      all_results <- rbind(all_results, results)
      cat("Found", nrow(results), "results\n")
    }

    Sys.sleep(2)  # Rate limiting
  }

  # Deduplicate
  if (nrow(all_results) > 0) {
    all_results <- all_results %>% distinct()
  }

  return(all_results)
}

# Search for Caitlin Skidmore in Virginia
search_skidmore_virginia <- function() {
  name_variations <- c(
    "Caitlin Skidmore",
    "Caitlin Marie Skidmore",
    "SKIDMORE, CAITLIN MARIE",
    "SKIDMORE, CAITLIN",
    "Skidmore, Caitlin",
    "Skidmore, Caitlin Marie"
  )

  all_results <- data.frame()

  for (variation in name_variations) {
    cat("Searching Virginia for:", variation, "\n")
    results <- search_virginia_dpor(variation, "individual")

    if (nrow(results) > 0) {
      all_results <- rbind(all_results, results)
      cat("Found", nrow(results), "results\n")
    }

    Sys.sleep(2)  # Rate limiting
  }

  # Deduplicate
  if (nrow(all_results) > 0) {
    all_results <- all_results %>% distinct()
  }

  return(all_results)
}

# Test function - only runs if explicitly called, not when sourced
# To run tests, call: test_virginia_search()
test_virginia_search <- function() {
  cat("Running Virginia DPOR search test...\n")
  test_results <- search_firm_virginia("Bell Partners Inc")
  print(test_results)
  return(test_results)
}
