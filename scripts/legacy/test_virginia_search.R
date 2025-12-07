#!/usr/bin/env Rscript
# Test Virginia DPOR Search
# Quick test to verify the search system works

source("search_virginia_dpor.R")

cat("=== Testing Virginia DPOR Search ===\n\n")

# Test with one firm
test_firm <- "Bell Partners Inc"
cat("Testing search for:", test_firm, "\n\n")

test_results <- search_firm_virginia(test_firm)

if (nrow(test_results) > 0) {
  cat("\n✓ Search successful! Found", nrow(test_results), "results\n")
  print(head(test_results))

  # Save test results
  write.csv(test_results, "data/raw/test_virginia_bell_partners.csv", row.names = FALSE)
  cat("\nSaved test results to: data/raw/test_virginia_bell_partners.csv\n")
} else {
  cat("\n⚠ No results found (this may be expected if the website structure has changed)\n")
}

cat("\n=== Test Complete ===\n")
