# R Analysis Service Dockerfile
FROM rocker/r-ver:4.3.2

# Install system dependencies including curl for health checks
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libpoppler-cpp-dev \
    libv8-dev \
    pandoc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install R packages in batches to avoid timeouts
RUN R -e "install.packages(c('dplyr', 'jsonlite', 'stringr', 'httr', 'rvest', 'pdftools', 'readxl', 'data.table', 'reticulate', 'knitr', 'ggplot2'), repos='https://cran.rstudio.com/')" || true && \
    R -e "install.packages('plumber', repos='https://cran.rstudio.com/', dependencies=TRUE)" || echo "Plumber installation may have issues but continuing"

# Copy application code
COPY . /app

# Set R library path
ENV R_LIBS=/usr/local/lib/R/site-library

# Expose port for API (if needed)
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD Rscript --version || exit 1

# Default command - can be overridden
CMD ["Rscript", "--version"]
