-- SQL DDL Schema Definition
-- Kettler Data Analysis Database Schema
-- Generated: 2025-12-08
-- Version: 1.0.0

-- ============================================================================
-- TABLE: firms
-- Description: Real estate firms associated with Caitlin Skidmore as principal broker
-- Primary Key: firm_license
-- ============================================================================

CREATE TABLE IF NOT EXISTS firms (
    firm_license VARCHAR(10) PRIMARY KEY,
    firm_name VARCHAR(255) NOT NULL,
    individual_license VARCHAR(10) NULL,
    license_type VARCHAR(50) NOT NULL CHECK (license_type = 'Real Estate Firm License'),
    firm_type VARCHAR(100) NOT NULL CHECK (firm_type IN (
        'Corporation',
        'LLC - Limited Liability Company',
        'Solely owned LLC',
        'LLC',
        'Limited Partnership',
        'LP'
    )),
    address VARCHAR(500) NOT NULL,
    dba_name VARCHAR(255) NULL,
    initial_cert_date DATE NULL,
    expiration_date DATE NOT NULL,
    principal_broker VARCHAR(255) NOT NULL CHECK (principal_broker = 'SKIDMORE CAITLIN MARIE'),
    gap_years DECIMAL(5,2) NULL,
    state CHAR(2) NOT NULL CHECK (LENGTH(state) = 2),
    notes TEXT NULL,
    needs_verification BOOLEAN NOT NULL DEFAULT FALSE,
    verification_date DATE NULL,

    -- Constraints
    CONSTRAINT firms_expiration_after_initial CHECK (
        expiration_date > initial_cert_date OR initial_cert_date IS NULL
    ),
    CONSTRAINT firms_license_format CHECK (
        firm_license ~ '^[0-9]{10}$'
    ),

    -- Foreign Keys
    CONSTRAINT fk_firms_individual_license FOREIGN KEY (individual_license)
        REFERENCES individual_licenses(license_number)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- Indexes for firms table
CREATE INDEX IF NOT EXISTS idx_firms_firm_name ON firms(firm_name);
CREATE INDEX IF NOT EXISTS idx_firms_state ON firms(state);
CREATE INDEX IF NOT EXISTS idx_firms_principal_broker ON firms(principal_broker);
CREATE INDEX IF NOT EXISTS idx_firms_address ON firms(address);
CREATE INDEX IF NOT EXISTS idx_firms_expiration_date ON firms(expiration_date);

-- ============================================================================
-- TABLE: individual_licenses
-- Description: Individual real estate licenses for Caitlin Skidmore
-- Primary Key: license_number
-- ============================================================================

CREATE TABLE IF NOT EXISTS individual_licenses (
    license_number VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL CHECK (name = 'SKIDMORE, CAITLIN MARIE'),
    address VARCHAR(500) NOT NULL,
    license_type VARCHAR(50) NOT NULL CHECK (license_type = 'Real Estate Individual'),
    board VARCHAR(100) NOT NULL CHECK (board = 'Real Estate Board'),
    state CHAR(2) NULL CHECK (LENGTH(state) = 2),

    -- Constraints
    CONSTRAINT individual_licenses_license_format CHECK (
        license_number ~ '^[0-9]{10}$'
    )
);

-- Indexes for individual_licenses table
CREATE INDEX IF NOT EXISTS idx_individual_licenses_name ON individual_licenses(name);
CREATE INDEX IF NOT EXISTS idx_individual_licenses_address ON individual_licenses(address);
CREATE INDEX IF NOT EXISTS idx_individual_licenses_state ON individual_licenses(state);

-- ============================================================================
-- TABLE: str_listings
-- Description: Short-term rental listings scraped from various platforms
-- Primary Key: listing_id
-- ============================================================================

CREATE TABLE IF NOT EXISTS str_listings (
    listing_id VARCHAR(255) PRIMARY KEY,
    platform VARCHAR(50) NOT NULL CHECK (platform IN ('Airbnb', 'VRBO', 'Front Website', 'Other')),
    property_address VARCHAR(500) NOT NULL,
    property_name VARCHAR(255) NULL,
    scraped_date DATE NOT NULL,
    metadata JSONB NULL,

    -- Composite unique constraint for deduplication
    CONSTRAINT str_listings_unique_platform_address_date UNIQUE (
        platform, property_address, scraped_date
    )
);

-- Indexes for str_listings table
CREATE INDEX IF NOT EXISTS idx_str_listings_platform ON str_listings(platform);
CREATE INDEX IF NOT EXISTS idx_str_listings_property_address ON str_listings(property_address);
CREATE INDEX IF NOT EXISTS idx_str_listings_scraped_date ON str_listings(scraped_date);

-- ============================================================================
-- TABLE: firm_connections
-- Description: Connections and relationships between firms
-- Primary Key: connection_id
-- ============================================================================

CREATE TABLE IF NOT EXISTS firm_connections (
    connection_id VARCHAR(255) PRIMARY KEY,
    firm_license_1 VARCHAR(10) NOT NULL,
    firm_license_2 VARCHAR(10) NOT NULL,
    connection_type VARCHAR(50) NOT NULL CHECK (connection_type IN (
        'same_address',
        'same_principal_broker',
        'same_license_date',
        'other'
    )),
    connection_strength DECIMAL(3,2) NULL CHECK (
        connection_strength >= 0 AND connection_strength <= 1
    ),

    -- Constraints
    CONSTRAINT firm_connections_no_self_connection CHECK (
        firm_license_1 != firm_license_2
    ),
    CONSTRAINT firm_connections_license_format_1 CHECK (
        firm_license_1 ~ '^[0-9]{10}$'
    ),
    CONSTRAINT firm_connections_license_format_2 CHECK (
        firm_license_2 ~ '^[0-9]{10}$'
    ),

    -- Composite unique constraint
    CONSTRAINT firm_connections_unique_pair UNIQUE (
        firm_license_1, firm_license_2
    ),

    -- Foreign Keys
    CONSTRAINT fk_firm_connections_firm_1 FOREIGN KEY (firm_license_1)
        REFERENCES firms(firm_license)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_firm_connections_firm_2 FOREIGN KEY (firm_license_2)
        REFERENCES firms(firm_license)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Indexes for firm_connections table
CREATE INDEX IF NOT EXISTS idx_firm_connections_firm_1 ON firm_connections(firm_license_1);
CREATE INDEX IF NOT EXISTS idx_firm_connections_firm_2 ON firm_connections(firm_license_2);
CREATE INDEX IF NOT EXISTS idx_firm_connections_type ON firm_connections(connection_type);

-- ============================================================================
-- TABLE: analysis_results
-- Description: Analysis outputs and quality reports
-- Primary Key: analysis_id
-- ============================================================================

CREATE TABLE IF NOT EXISTS analysis_results (
    analysis_id VARCHAR(255) PRIMARY KEY,
    analysis_type VARCHAR(50) NOT NULL CHECK (analysis_type IN (
        'data_quality',
        'connection_analysis',
        'validation',
        'summary'
    )),
    analysis_date DATE NOT NULL,
    results JSONB NOT NULL
);

-- Indexes for analysis_results table
CREATE INDEX IF NOT EXISTS idx_analysis_results_type ON analysis_results(analysis_type);
CREATE INDEX IF NOT EXISTS idx_analysis_results_date ON analysis_results(analysis_date);

-- ============================================================================
-- VIEWS
-- ============================================================================

-- View: Firms by State
CREATE OR REPLACE VIEW v_firms_by_state AS
SELECT
    state,
    COUNT(*) AS firm_count,
    MIN(initial_cert_date) AS earliest_license,
    MAX(expiration_date) AS latest_expiration
FROM firms
GROUP BY state
ORDER BY firm_count DESC;

-- View: Firms with Same Address
CREATE OR REPLACE VIEW v_firms_same_address AS
SELECT
    f1.firm_license AS firm_license_1,
    f1.firm_name AS firm_name_1,
    f2.firm_license AS firm_license_2,
    f2.firm_name AS firm_name_2,
    f1.address,
    f1.state
FROM firms f1
JOIN firms f2 ON f1.address = f2.address
WHERE f1.firm_license < f2.firm_license
ORDER BY f1.address, f1.firm_name;

-- View: Firm Connections Summary
CREATE OR REPLACE VIEW v_firm_connections_summary AS
SELECT
    fc.connection_type,
    COUNT(*) AS connection_count,
    AVG(fc.connection_strength) AS avg_strength
FROM firm_connections fc
GROUP BY fc.connection_type
ORDER BY connection_count DESC;

-- View: Firms Expiring Soon
CREATE OR REPLACE VIEW v_firms_expiring_soon AS
SELECT
    firm_license,
    firm_name,
    expiration_date,
    state,
    expiration_date - CURRENT_DATE AS days_until_expiration
FROM firms
WHERE expiration_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '1 year'
ORDER BY expiration_date;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE firms IS 'Real estate firms associated with Caitlin Skidmore as principal broker';
COMMENT ON TABLE individual_licenses IS 'Individual real estate licenses for Caitlin Skidmore across multiple states';
COMMENT ON TABLE str_listings IS 'Short-term rental listings scraped from various platforms';
COMMENT ON TABLE firm_connections IS 'Connections and relationships between firms';
COMMENT ON TABLE analysis_results IS 'Analysis outputs and quality reports';

COMMENT ON COLUMN firms.firm_license IS 'Primary Key: 10-digit Virginia DPOR license number';
COMMENT ON COLUMN firms.individual_license IS 'Foreign Key: References individual_licenses.license_number (optional)';
COMMENT ON COLUMN firms.gap_years IS 'Years between firm license date and Skidmore license date (2025-05-30). Negative if firm licensed after Skidmore.';

COMMENT ON COLUMN individual_licenses.license_number IS 'Primary Key: 10-digit license number';
COMMENT ON COLUMN firm_connections.firm_license_1 IS 'Foreign Key: References firms.firm_license';
COMMENT ON COLUMN firm_connections.firm_license_2 IS 'Foreign Key: References firms.firm_license';
