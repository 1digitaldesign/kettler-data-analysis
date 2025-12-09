#!/usr/bin/env Rscript
# Load Paths Utility
# Simple wrapper to load paths.R from bin scripts

# Find project root by going up from bin directory
script_dir <- if (exists("ofile")) {
  dirname(normalizePath(ofile))
} else {
  # Try to get script directory from command args
  args <- commandArgs(trailingOnly = FALSE)
  script_arg <- grep("^--file=", args, value = TRUE)
  if (length(script_arg) > 0) {
    dirname(sub("^--file=", "", script_arg))
  } else {
    getwd()
  }
}

# Go up one level to project root
project_root <- if (file.exists(file.path(script_dir, "..", "README.md"))) {
  normalizePath(file.path(script_dir, ".."))
} else {
  # Fallback: search from current directory
  current_dir <- getwd()
  for (i in 1:10) {
    if (file.exists(file.path(current_dir, "README.md")) &&
        file.exists(file.path(current_dir, "bin"))) {
      project_root <- current_dir
      break
    }
    current_dir <- dirname(current_dir)
    if (current_dir == dirname(current_dir)) break
  }
  if (!exists("project_root")) project_root <- getwd()
}

# Source paths utility
source(file.path(project_root, "scripts", "utils", "paths.R"))
