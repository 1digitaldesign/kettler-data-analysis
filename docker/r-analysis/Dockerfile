# R Analysis Service Dockerfile
FROM rocker/r-ver:4.3.2

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libpoppler-cpp-dev \
    libv8-dev \
    pandoc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install R packages in batches to avoid timeouts
RUN R -e "install.packages(c('dplyr', 'jsonlite', 'stringr', 'httr', 'rvest', 'pdftools', 'readxl', 'data.table', 'reticulate', 'knitr', 'ggplot2'), repos='https://cran.rstudio.com/')" && \
    R -e "install.packages('plumber', repos='https://cran.rstudio.com/', dependencies=TRUE)" && \
    R -e "if (!require('plumber', quietly=TRUE)) stop('plumber installation failed')"

# Copy application code
COPY . /app

# Set R library path
ENV R_LIBS=/usr/local/lib/R/site-library

# Expose port for API (if needed)
EXPOSE 8001

# Default command - can be overridden
CMD ["Rscript", "--version"]
