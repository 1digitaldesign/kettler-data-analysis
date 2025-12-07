#!/usr/bin/env Rscript
# Initialize Vector Store
# Sets up the vector embedding system and runs initial ETL

cat("========================================\n")
cat("Initializing Vector Embedding System\n")
cat("========================================\n\n")

# Check Python availability
python_cmd <- if (system("which python3 > /dev/null 2>&1", ignore.stdout = TRUE, ignore.stderr = TRUE) == 0) {
  "python3"
} else {
  "python"
}

cat("Using Python:", python_cmd, "\n\n")

# Check if required Python packages are installed
cat("Checking Python dependencies...\n")
check_package <- function(package) {
  result <- system(
    paste(python_cmd, "-c", shQuote(paste0("import ", package))),
    ignore.stdout = TRUE,
    ignore.stderr = TRUE
  )
  return(result == 0)
}

packages <- c("sentence_transformers", "faiss", "pandas", "numpy")
missing <- c()

for (pkg in packages) {
  if (check_package(pkg)) {
    cat("  ✓", pkg, "\n")
  } else {
    cat("  ✗", pkg, "(missing)\n")
    missing <- c(missing, pkg)
  }
}

if (length(missing) > 0) {
  cat("\nMissing packages detected. Install with:\n")
  cat("  pip install -r requirements.txt\n\n")
  cat("Or install individually:\n")
  for (pkg in missing) {
    if (pkg == "sentence_transformers") {
      cat("  pip install sentence-transformers\n")
    } else if (pkg == "faiss") {
      cat("  pip install faiss-cpu\n")
    } else {
      cat("  pip install", pkg, "\n")
    }
  }
  stop("Please install missing packages before continuing.")
}

cat("\nAll dependencies available.\n\n")

# Create vector store directory
PROJECT_ROOT <- getwd()
if (basename(PROJECT_ROOT) != "kettler-data-analysis") {
  PROJECT_ROOT <- dirname(dirname(PROJECT_ROOT))
}

VECTOR_DIR <- file.path(PROJECT_ROOT, "data", "vectors")
dir.create(VECTOR_DIR, showWarnings = FALSE, recursive = TRUE)
cat("Vector store directory:", VECTOR_DIR, "\n\n")

# Run initial ETL
cat("Running initial ETL pipeline...\n")
etl_script <- file.path(PROJECT_ROOT, "scripts", "etl", "etl_pipeline.py")

if (!file.exists(etl_script)) {
  stop("ETL script not found: ", etl_script)
}

system_result <- system(
  paste(python_cmd, shQuote(etl_script)),
  intern = FALSE
)

if (system_result == 0) {
  cat("\n✓ Vector store initialized successfully!\n")
} else {
  cat("\n✗ ETL pipeline encountered errors.\n")
  cat("You can run it manually with:\n")
  cat("  python3 scripts/etl/etl_pipeline.py\n")
}

cat("\n========================================\n")
cat("Initialization Complete\n")
cat("========================================\n")
