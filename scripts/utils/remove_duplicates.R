#!/usr/bin/env Rscript
# Remove duplicate entries from all_findings.csv

library(dplyr)

# Read CSV
df <- read.csv("research/license_searches/consolidated/all_findings.csv")

cat("=== Removing Duplicates ===\n")
cat("Total entries before:", nrow(df), "\n")

# Remove duplicates - keep first occurrence of each employee+state combination
df_dedup <- df %>%
  distinct(employee, state, .keep_all = TRUE)

cat("Total entries after:", nrow(df_dedup), "\n")
cat("Removed:", nrow(df) - nrow(df_dedup), "duplicates\n")

# Check Thomas Bisanz specifically
tb <- df_dedup[df_dedup$employee == "Thomas Bisanz", ]
cat("\nThomas Bisanz after deduplication:\n")
cat("  Total entries:", nrow(tb), "\n")
cat("  Unique states:", length(unique(tb$state)), "\n")
cat("  Maryland included:", "Maryland" %in% tb$state, "\n")

# Save updated CSV
write.csv(df_dedup, "research/license_searches/consolidated/all_findings.csv", row.names = FALSE)
cat("\n✅ CSV updated - duplicates removed\n")
