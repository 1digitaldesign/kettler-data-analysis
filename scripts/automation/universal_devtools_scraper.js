/**
 * Universal DevTools Scraper - Multi-State, Multi-Use Case
 *
 * A comprehensive scraping framework using Chrome DevTools capabilities
 * for license searches across all states and extensible for any use case.
 *
 * Features:
 * - Multi-state support (CT, MD, NJ, NY, DC, VA)
 * - All employees support
 * - Universal scraping functions
 * - Extensible for any use case
 * - Network monitoring
 * - DOM inspection
 * - Pattern matching
 * - Structured data extraction
 */

/**
 * Employee database - All employees across all states
 */
const ALL_EMPLOYEES = [
  // Executive Leadership
  { name: "Robert Kettler", lastName: "Kettler", firstName: "Robert", title: "CEO", priority: "HIGH" },
  { name: "Caitlin Skidmore", lastName: "Skidmore", firstName: "Caitlin", title: "Principal Broker", priority: "HIGH" },
  { name: "Cindy Fisher", lastName: "Fisher", firstName: "Cindy", title: "President", priority: "MEDIUM" },
  { name: "Pat Cassada", lastName: "Cassada", firstName: "Pat", title: "CFO", priority: "MEDIUM" },
  { name: "Luke Davis", lastName: "Davis", firstName: "Luke", title: "CIO", priority: "MEDIUM" },
  { name: "Sean Curtin", lastName: "Curtin", firstName: "Sean", title: "General Counsel", priority: "MEDIUM" },

  // Operations Management
  { name: "Robert Grealy", lastName: "Grealy", firstName: "Robert", title: "SVP Operations", priority: "MEDIUM" },
  { name: "Todd Bowen", lastName: "Bowen", firstName: "Todd", title: "SVP Strategic Services", priority: "MEDIUM" },
  { name: "Amy Groff", lastName: "Groff", firstName: "Amy", title: "VP Operations", priority: "MEDIUM" },
  { name: "Kristina Thoummarath", lastName: "Thoummarath", firstName: "Kristina", title: "Chief of Staff", priority: "MEDIUM" },
  { name: "Christina Chang", lastName: "Chang", firstName: "Christina", title: "Head of Asset Management", priority: "MEDIUM" },
  { name: "Jeffrey Williams", lastName: "Williams", firstName: "Jeffrey", title: "VP Human Resources", priority: "MEDIUM" },

  // Property Management
  { name: "Edward Hyland", lastName: "Hyland", firstName: "Edward", title: "Senior Regional Manager", priority: "HIGH" },
  { name: "Djene Moyer", lastName: "Moyer", firstName: "Djene", title: "Community Manager", priority: "MEDIUM" },
  { name: "Henry Ramos", lastName: "Ramos", firstName: "Henry", title: "Property Manager", priority: "MEDIUM" },

  // Additional Employees
  { name: "Liddy Bisanz", lastName: "Bisanz", firstName: "Liddy", title: "Unknown", priority: "MEDIUM" },
  { name: "Leah Douthit", lastName: "Douthit", firstName: "Leah", title: "Unknown", priority: "MEDIUM" }
];

/**
 * State configuration - All states with their search portals
 */
const STATE_CONFIGS = {
  "Connecticut": {
    name: "Connecticut",
    abbreviation: "CT",
    agency: "Connecticut Department of Consumer Protection (DCP)",
    searchUrl: "https://www.elicense.ct.gov/lookup/licenselookup.aspx",
    licenseTypes: {
      broker: "REAL ESTATE BROKER",
      salesperson: "REAL ESTATE SALESPERSON",
      team: "REAL ESTATE TEAM"
    },
    formSelectors: {
      licenseType: 'select[name*="LicenseType"], select[id*="LicenseType"]',
      lastName: 'input[name*="LastName"], input[id*="LastName"]',
      firstName: 'input[name*="FirstName"], input[id*="FirstName"]',
      submit: 'input[type="submit"], button[type="submit"], input[value*="Search"]'
    },
    requiresCaptcha: false,
    waitTime: 2000
  },
  "Maryland": {
    name: "Maryland",
    abbreviation: "MD",
    agency: "Maryland Department of Labor, Licensing and Regulation (DLLR)",
    searchUrl: "https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name",
    formSelectors: {
      lastName: 'input[name*="lastname"], input[name*="last_name"], input[id*="lastname"]',
      firstName: 'input[name*="firstname"], input[name*="first_name"], input[id*="firstname"]',
      submit: 'input[type="submit"][value*="Search"], button:has-text("Search")'
    },
    requiresCaptcha: true,
    captchaWaitTime: 300000, // 5 minutes
    waitTime: 2000
  },
  "New Jersey": {
    name: "New Jersey",
    abbreviation: "NJ",
    agency: "New Jersey Division of Consumer Affairs",
    searchUrl: "https://newjersey.mylicense.com/verification/Search.aspx?facility=N",
    formSelectors: {
      profession: 'select[name*="Profession"], select[id*="Profession"]',
      licenseType: 'select[name*="LicenseType"], select[id*="LicenseType"]',
      lastName: 'input[name*="LastName"], input[id*="LastName"]',
      firstName: 'input[name*="FirstName"], input[id*="FirstName"]',
      submit: 'input[type="submit"], button[type="submit"], input[value*="Search"]'
    },
    requiresCaptcha: false,
    waitTime: 2000
  },
  "New York": {
    name: "New York",
    abbreviation: "NY",
    agency: "New York Department of State",
    searchUrl: "https://www.dos.ny.gov/licensing/lookup/indiv.asp",
    formSelectors: {
      searchType: 'input[type="radio"][value*="Individual"], input[name*="SearchType"]',
      lastName: 'input[name*="LastName"], input[id*="LastName"]',
      firstName: 'input[name*="FirstName"], input[id*="FirstName"]',
      submit: 'input[type="submit"], button[type="submit"], input[value*="Search"]'
    },
    requiresCaptcha: false,
    waitTime: 2000
  },
  "District of Columbia": {
    name: "District of Columbia",
    abbreviation: "DC",
    agency: "DC Office of Consumer Protection and Licensing Administration",
    searchUrl: "https://govservices.dcra.dc.gov/oplaportal/Home/GetLicenseSearchDetails",
    formSelectors: {
      lastName: 'input[name*="LastName"], input[id*="LastName"]',
      firstName: 'input[name*="FirstName"], input[id*="FirstName"]',
      submit: 'input[type="submit"], button[type="submit"], input[value*="Search"]'
    },
    requiresCaptcha: false,
    waitTime: 2000,
    isApiBased: true // May use API calls instead of form submission
  },
  "Virginia": {
    name: "Virginia",
    abbreviation: "VA",
    agency: "Virginia Department of Professional and Occupational Regulation",
    searchUrl: "https://www.dpor.virginia.gov/LicenseLookup",
    formSelectors: {
      licenseType: 'select[name*="LicenseType"], select[id*="LicenseType"]',
      lastName: 'input[name*="LastName"], input[id*="LastName"]',
      firstName: 'input[name*="FirstName"], input[id*="FirstName"]',
      submit: 'input[type="submit"], button[type="submit"], input[value*="Search"]'
    },
    requiresCaptcha: false,
    waitTime: 2000
  }
};

/**
 * Universal DevTools scraping function
 * Works for any state and any use case
 */
async function scrapeWithDevToolsUniversal(page, employee, stateConfig, options = {}) {
  const {
    enableNetworkMonitoring = true,
    enableConsoleLogging = true,
    enablePerformanceMetrics = true,
    extractPatterns = true,
    extractTables = true,
    extractForms = true,
    customExtractors = []
  } = options;

  console.log(`[Universal DevTools] Scraping ${employee.name} in ${stateConfig.name}...`);

  try {
    // Setup monitoring
    const networkRequests = [];
    const consoleMessages = [];
    const errors = [];

    if (enableNetworkMonitoring) {
      page.on('request', request => {
        networkRequests.push({
          url: request.url(),
          method: request.method(),
          resourceType: request.resourceType(),
          headers: request.headers(),
          timestamp: Date.now()
        });
      });

      page.on('response', response => {
        const request = networkRequests.find(r => r.url === response.url());
        if (request) {
          request.status = response.status();
          request.statusText = response.statusText();
          request.responseHeaders = response.headers();
        }
      });
    }

    if (enableConsoleLogging) {
      page.on('console', msg => {
        consoleMessages.push({
          type: msg.type(),
          text: msg.text(),
          location: msg.location(),
          timestamp: Date.now()
        });
        if (msg.type() === 'error') {
          errors.push(msg.text());
        }
      });

      page.on('pageerror', error => {
        errors.push({
          message: error.message,
          stack: error.stack,
          timestamp: Date.now()
        });
      });
    }

    // Wait for page load
    await page.waitForLoadState('networkidle', { timeout: 60000 });
    await page.waitForTimeout(stateConfig.waitTime || 2000);

    // Comprehensive page data extraction
    const pageData = await page.evaluate((emp, stateName, extractPatterns, extractTables, extractForms) => {
      const data = {
        employee: emp,
        state: stateName,
        pageTitle: document.title,
        url: window.location.href,
        timestamp: new Date().toISOString(),

        // Performance metrics
        performance: null,

        // DOM statistics
        domStats: {
          totalElements: document.querySelectorAll('*').length,
          tables: document.querySelectorAll('table').length,
          forms: document.querySelectorAll('form').length,
          links: document.querySelectorAll('a').length,
          images: document.querySelectorAll('img').length,
          scripts: document.querySelectorAll('script').length,
          stylesheets: document.querySelectorAll('link[rel="stylesheet"]').length
        },

        // Text content
        bodyText: document.body.innerText,
        bodyTextLower: document.body.innerText.toLowerCase(),
        htmlLength: document.documentElement.outerHTML.length,

        // Extracted data
        tables: [],
        forms: [],
        links: [],
        images: [],
        patterns: {},
        structuredData: []
      };

      // Performance metrics
      if (window.performance && window.performance.timing) {
        const timing = window.performance.timing;
        data.performance = {
          navigationStart: timing.navigationStart,
          domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
          loadComplete: timing.loadEventEnd - timing.navigationStart,
          firstPaint: timing.responseStart - timing.navigationStart,
          domInteractive: timing.domInteractive - timing.navigationStart
        };
      }

      // Extract tables
      if (extractTables) {
        data.tables = Array.from(document.querySelectorAll('table')).map((table, index) => {
          const rows = Array.from(table.querySelectorAll('tr')).map(row => {
            const cells = Array.from(row.querySelectorAll('td, th')).map(cell => ({
              text: cell.innerText.trim(),
              html: cell.innerHTML.trim(),
              colspan: cell.colSpan || 1,
              rowspan: cell.rowSpan || 1,
              className: cell.className || null,
              id: cell.id || null
            }));
            return {
              cells: cells,
              rowText: row.innerText.trim(),
              rowHtml: row.innerHTML.trim(),
              className: row.className || null,
              id: row.id || null
            };
          });

          return {
            index: index,
            id: table.id || null,
            className: table.className || null,
            rowCount: rows.length,
            columnCount: rows.length > 0 ? rows[0].cells.length : 0,
            rows: rows,
            fullText: table.innerText.trim(),
            fullHtml: table.innerHTML.trim()
          };
        });
      }

      // Extract forms
      if (extractForms) {
        data.forms = Array.from(document.querySelectorAll('form')).map((form, index) => {
          const inputs = Array.from(form.querySelectorAll('input, select, textarea, button')).map(input => ({
            type: input.type || input.tagName.toLowerCase(),
            tagName: input.tagName.toLowerCase(),
            name: input.name || null,
            id: input.id || null,
            value: input.value || input.textContent || null,
            placeholder: input.placeholder || null,
            required: input.required || false,
            disabled: input.disabled || false,
            label: input.labels && input.labels.length > 0 ? input.labels[0].innerText.trim() : null,
            options: input.tagName === 'SELECT' ? Array.from(input.options).map(opt => ({
              value: opt.value,
              text: opt.text,
              selected: opt.selected
            })) : null
          }));

          return {
            index: index,
            id: form.id || null,
            className: form.className || null,
            action: form.action || null,
            method: form.method || 'GET',
            inputs: inputs,
            inputCount: inputs.length
          };
        });
      }

      // Extract links
      data.links = Array.from(document.querySelectorAll('a')).slice(0, 100).map(link => ({
        text: link.innerText.trim(),
        href: link.href,
        title: link.title || null,
        target: link.target || null
      }));

      // Extract images
      data.images = Array.from(document.querySelectorAll('img')).slice(0, 50).map(img => ({
        src: img.src,
        alt: img.alt || null,
        title: img.title || null,
        width: img.width || null,
        height: img.height || null
      }));

      // Pattern extraction
      if (extractPatterns) {
        const patterns = {
          // License patterns
          licenseNumbers: [],
          licenseTypes: [],
          statuses: [],
          expirationDates: [],
          issueDates: [],

          // Contact patterns
          emails: [],
          phones: [],
          addresses: [],

          // Date patterns
          dates: [],

          // Number patterns
          numbers: [],

          // Custom patterns
          custom: {}
        };

        const text = document.body.innerText;
        const textLower = text.toLowerCase();

        // License number patterns
        const licensePatterns = [
          /\b[A-Z]{1,3}\d{4,10}\b/g,
          /\b\d{4,10}\b/g,
          /License\s*(?:#|Number|No\.?)\s*:?\s*([A-Z0-9-]+)/gi,
          /License\s+([A-Z0-9-]+)/gi,
          /(?:License|Lic\.?)\s*:?\s*([A-Z0-9-]{4,15})/gi
        ];

        licensePatterns.forEach(pattern => {
          const matches = text.match(pattern);
          if (matches) {
            patterns.licenseNumbers.push(...matches.map(m => m.trim()).filter(m => m.length > 0));
          }
        });

        // License type patterns
        const licenseTypePatterns = [
          /Real\s+Estate\s+(?:Broker|Salesperson|Agent|Appraiser)/gi,
          /(?:Broker|Salesperson|Agent|Appraiser)\s+License/gi,
          /License\s+Type\s*:?\s*([A-Za-z\s]+)/gi
        ];

        licenseTypePatterns.forEach(pattern => {
          const matches = text.match(pattern);
          if (matches) {
            patterns.licenseTypes.push(...matches.map(m => m.trim()).filter(m => m.length > 0));
          }
        });

        // Status patterns
        const statusPatterns = [
          /Status\s*:?\s*(Active|Inactive|Expired|Pending|Suspended|Revoked|Renewed)/gi,
          /(?:License\s+)?(Active|Inactive|Expired|Pending|Suspended|Revoked|Renewed)/gi
        ];

        statusPatterns.forEach(pattern => {
          const matches = text.match(pattern);
          if (matches) {
            patterns.statuses.push(...matches.map(m => m.trim()).filter(m => m.length > 0));
          }
        });

        // Date patterns
        const datePatterns = [
          /(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/g,
          /(?:Expiration|Expires?|Exp\.?)\s*(?:Date|Dt\.?)\s*:?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/gi,
          /(?:Issue|Issued|Issue\s+Date)\s*:?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/gi
        ];

        datePatterns.forEach(pattern => {
          const matches = text.match(pattern);
          if (matches) {
            patterns.dates.push(...matches.map(m => m.trim()).filter(m => m.length > 0));
          }
        });

        // Email patterns
        const emailPattern = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g;
        const emails = text.match(emailPattern);
        if (emails) {
          patterns.emails = [...new Set(emails)];
        }

        // Phone patterns
        const phonePatterns = [
          /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g,
          /\(\d{3}\)\s*\d{3}[-.]?\d{4}/g,
          /\+\d{1,3}[-.]?\d{1,4}[-.]?\d{1,4}[-.]?\d{1,9}/g
        ];

        phonePatterns.forEach(pattern => {
          const matches = text.match(pattern);
          if (matches) {
            patterns.phones.push(...matches.map(m => m.trim()));
          }
        });

        // Remove duplicates
        patterns.licenseNumbers = [...new Set(patterns.licenseNumbers)];
        patterns.licenseTypes = [...new Set(patterns.licenseTypes)];
        patterns.statuses = [...new Set(patterns.statuses)];
        patterns.dates = [...new Set(patterns.dates)];
        patterns.phones = [...new Set(patterns.phones)];

        data.patterns = patterns;
      }

      // Structured data extraction from tables
      if (extractTables && data.tables.length > 0) {
        data.structuredData = data.tables.map(table => {
          if (table.rows.length === 0) return null;

          // Try to identify header row
          const headerRow = table.rows[0];
          const headers = headerRow ? headerRow.cells.map(c => c.text.toLowerCase().replace(/\s+/g, '_')) : [];

          // Extract data rows
          const dataRows = table.rows.slice(1).map(row => {
            const rowData = {};
            row.cells.forEach((cell, index) => {
              const header = headers[index] || `column_${index}`;
              rowData[header] = cell.text;
            });
            return rowData;
          });

          return {
            tableIndex: table.index,
            headers: headers,
            dataRows: dataRows,
            rowCount: dataRows.length
          };
        }).filter(item => item !== null);
      }

      // Check for results indicators
      data.resultsIndicators = {
        hasResults: false,
        noResults: false,
        noResultsMessage: null,
        resultsCount: 0,
        employeeNameFound: false
      };

      const empNameLower = emp.name.toLowerCase();
      const lastNameLower = emp.lastName.toLowerCase();
      const firstNameLower = emp.firstName.toLowerCase();

      // Check for employee name
      if (data.bodyTextLower.includes(lastNameLower) && data.bodyTextLower.includes(firstNameLower)) {
        data.resultsIndicators.employeeNameFound = true;
      }

      // Check for "no results" messages
      const noResultsPatterns = [
        /no\s+results?/gi,
        /no\s+records?\s+found/gi,
        /no\s+matches?/gi,
        /no\s+licenses?/gi,
        /not\s+found/gi,
        /no\s+data\s+available/gi
      ];

      noResultsPatterns.forEach(pattern => {
        if (pattern.test(data.bodyText)) {
          data.resultsIndicators.noResults = true;
          const match = data.bodyText.match(pattern);
          if (match) {
            data.resultsIndicators.noResultsMessage = match[0];
          }
        }
      });

      // Count results in tables
      if (data.tables.length > 0) {
        data.tables.forEach(table => {
          table.rows.forEach(row => {
            const rowTextLower = row.rowText.toLowerCase();
            if (rowTextLower.includes(lastNameLower) && rowTextLower.includes(firstNameLower)) {
              data.resultsIndicators.hasResults = true;
              data.resultsIndicators.resultsCount++;
            }
          });
        });
      }

      return data;
    }, employee, stateConfig.name, extractPatterns, extractTables, extractForms);

    // Apply custom extractors
    if (customExtractors && customExtractors.length > 0) {
      for (const extractor of customExtractors) {
        try {
          const customData = await extractor(page, pageData, employee, stateConfig);
          pageData.customData = pageData.customData || {};
          pageData.customData[extractor.name || 'extractor'] = customData;
        } catch (error) {
          console.error(`[Custom Extractor Error] ${extractor.name || 'Unknown'}:`, error);
        }
      }
    }

    return {
      employee: employee.name,
      state: stateConfig.name,
      stateAbbreviation: stateConfig.abbreviation,
      searchExecuted: true,
      pageData: pageData,
      networkRequests: enableNetworkMonitoring ? networkRequests.slice(0, 50) : [],
      consoleMessages: enableConsoleLogging ? consoleMessages.slice(0, 50) : [],
      errors: errors.length > 0 ? errors : null,
      timestamp: new Date().toISOString()
    };

  } catch (error) {
    return {
      employee: employee.name,
      state: stateConfig.name,
      stateAbbreviation: stateConfig.abbreviation,
      searchExecuted: false,
      error: error.message,
      stack: error.stack,
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * Universal search function - works for any state
 */
async function searchEmployeeUniversal(page, employee, stateName, options = {}) {
  const stateConfig = STATE_CONFIGS[stateName];

  if (!stateConfig) {
    throw new Error(`State configuration not found for: ${stateName}`);
  }

  console.log(`[Universal] Searching ${employee.name} in ${stateConfig.name}...`);

  try {
    // Navigate to search page
    await page.goto(stateConfig.searchUrl, {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    await page.waitForTimeout(stateConfig.waitTime || 2000);

    // Fill form based on state configuration
    if (stateConfig.formSelectors.lastName) {
      const lastNameInput = page.locator(stateConfig.formSelectors.lastName).first();
      await lastNameInput.waitFor({ state: 'visible', timeout: 15000 });
      await lastNameInput.fill(employee.lastName);
    }

    if (stateConfig.formSelectors.firstName) {
      const firstNameInput = page.locator(stateConfig.formSelectors.firstName).first();
      await firstNameInput.waitFor({ state: 'visible', timeout: 15000 });
      await firstNameInput.fill(employee.firstName);
    }

    // Handle license type selection if needed
    if (stateConfig.formSelectors.licenseType && employee.licenseType) {
      const licenseTypeSelect = page.locator(stateConfig.formSelectors.licenseType).first();
      await licenseTypeSelect.waitFor({ state: 'visible', timeout: 15000 });
      await licenseTypeSelect.selectOption({ label: employee.licenseType });
    }

    // Handle profession selection (New Jersey)
    if (stateConfig.formSelectors.profession) {
      const professionSelect = page.locator(stateConfig.formSelectors.profession).first();
      await professionSelect.waitFor({ state: 'visible', timeout: 15000 });
      await professionSelect.selectOption({ label: 'All' });
    }

    // Handle search type selection (New York)
    if (stateConfig.formSelectors.searchType) {
      const searchTypeRadio = page.locator(stateConfig.formSelectors.searchType).first();
      await searchTypeRadio.waitFor({ state: 'visible', timeout: 15000 });
      await searchTypeRadio.click();
    }

    // Handle CAPTCHA if required
    if (stateConfig.requiresCaptcha) {
      console.log(`[Universal] Waiting for CAPTCHA completion in ${stateConfig.name}...`);
      const submitButton = page.locator(stateConfig.formSelectors.submit).first();

      let attempts = 0;
      const maxAttempts = stateConfig.captchaWaitTime / 1000 || 300;

      while (attempts < maxAttempts) {
        const isDisabled = await submitButton.getAttribute('disabled');
        if (!isDisabled) {
          console.log(`[Universal] CAPTCHA completed for ${employee.name}`);
          break;
        }
        await page.waitForTimeout(1000);
        attempts++;
      }
    }

    // Submit form
    const submitButton = page.locator(stateConfig.formSelectors.submit).first();
    await submitButton.waitFor({ state: 'visible', timeout: 15000 });
    await submitButton.click();

    // Wait for results
    await page.waitForLoadState('networkidle', { timeout: 30000 });
    await page.waitForTimeout(stateConfig.waitTime || 2000);

    // Scrape with DevTools
    return await scrapeWithDevToolsUniversal(page, employee, stateConfig, options);

  } catch (error) {
    console.error(`[Universal] Error searching ${employee.name} in ${stateConfig.name}:`, error);
    return {
      employee: employee.name,
      state: stateConfig.name,
      searchExecuted: false,
      error: error.message,
      stack: error.stack,
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * Batch search all employees in a state
 */
async function searchAllEmployeesInState(page, stateName, options = {}) {
  const stateConfig = STATE_CONFIGS[stateName];

  if (!stateConfig) {
    throw new Error(`State configuration not found for: ${stateName}`);
  }

  console.log(`[Universal] Starting batch search for ${stateConfig.name}...`);
  console.log(`[Universal] Employees to search: ${ALL_EMPLOYEES.length}`);

  const results = [];
  const {
    filterEmployees = null, // Function to filter employees
    onProgress = null, // Callback for progress updates
    delayBetweenSearches = 2000
  } = options;

  let employeesToSearch = ALL_EMPLOYEES;
  if (filterEmployees) {
    employeesToSearch = employeesToSearch.filter(filterEmployees);
  }

  for (let i = 0; i < employeesToSearch.length; i++) {
    const employee = employeesToSearch[i];

    if (onProgress) {
      onProgress({
        current: i + 1,
        total: employeesToSearch.length,
        employee: employee.name,
        state: stateName
      });
    }

    console.log(`[Universal] [${i + 1}/${employeesToSearch.length}] Searching ${employee.name}...`);

    const result = await searchEmployeeUniversal(page, employee, stateName, options);
    results.push(result);

    // Log result summary
    if (result.searchExecuted) {
      const hasResults = result.pageData?.resultsIndicators?.hasResults || false;
      const noResults = result.pageData?.resultsIndicators?.noResults || false;
      const status = hasResults ? 'LICENSE FOUND' : (noResults ? 'NO LICENSE' : 'UNKNOWN');
      console.log(`[Universal] ✓ ${employee.name}: ${status}`);
    } else {
      console.log(`[Universal] ✗ ${employee.name}: ERROR - ${result.error}`);
    }

    // Delay between searches
    if (i < employeesToSearch.length - 1) {
      await page.waitForTimeout(delayBetweenSearches);
    }
  }

  // Summary
  const successful = results.filter(r => r.searchExecuted).length;
  const found = results.filter(r => r.pageData?.resultsIndicators?.hasResults).length;
  const errors = results.filter(r => !r.searchExecuted).length;

  console.log(`\n[Universal] Batch Search Summary for ${stateConfig.name}:`);
  console.log(`  - Total: ${results.length}`);
  console.log(`  - Successful: ${successful}`);
  console.log(`  - Licenses Found: ${found}`);
  console.log(`  - Errors: ${errors}`);

  return {
    state: stateName,
    stateConfig: stateConfig,
    results: results,
    summary: {
      total: results.length,
      successful: successful,
      found: found,
      errors: errors,
      successRate: (successful / results.length * 100).toFixed(2) + '%'
    },
    timestamp: new Date().toISOString()
  };
}

/**
 * Search all employees across all states
 */
async function searchAllEmployeesAllStates(page, options = {}) {
  console.log('[Universal] Starting comprehensive search across all states...');

  const {
    states = Object.keys(STATE_CONFIGS),
    onStateComplete = null,
    onComplete = null
  } = options;

  const allResults = {};

  for (const stateName of states) {
    console.log(`\n[Universal] ===== Processing ${stateName} =====`);

    const stateResults = await searchAllEmployeesInState(page, stateName, options);
    allResults[stateName] = stateResults;

    if (onStateComplete) {
      onStateComplete(stateName, stateResults);
    }

    // Delay between states
    await page.waitForTimeout(3000);
  }

  // Overall summary
  const totalSearches = Object.values(allResults).reduce((sum, r) => sum + r.summary.total, 0);
  const totalSuccessful = Object.values(allResults).reduce((sum, r) => sum + r.summary.successful, 0);
  const totalFound = Object.values(allResults).reduce((sum, r) => sum + r.summary.found, 0);
  const totalErrors = Object.values(allResults).reduce((sum, r) => sum + r.summary.errors, 0);

  console.log(`\n[Universal] ===== Overall Summary =====`);
  console.log(`  - Total Searches: ${totalSearches}`);
  console.log(`  - Successful: ${totalSuccessful}`);
  console.log(`  - Licenses Found: ${totalFound}`);
  console.log(`  - Errors: ${totalErrors}`);
  console.log(`  - Success Rate: ${(totalSuccessful / totalSearches * 100).toFixed(2)}%`);

  const overallResults = {
    states: allResults,
    summary: {
      totalSearches: totalSearches,
      totalSuccessful: totalSuccessful,
      totalFound: totalFound,
      totalErrors: totalErrors,
      successRate: (totalSuccessful / totalSearches * 100).toFixed(2) + '%'
    },
    timestamp: new Date().toISOString()
  };

  if (onComplete) {
    onComplete(overallResults);
  }

  return overallResults;
}

/**
 * Extract license information from scraped data (universal)
 */
function extractLicenseInfoUniversal(scrapedData) {
  if (!scrapedData.searchExecuted || !scrapedData.pageData) {
    return {
      found: false,
      error: scrapedData.error || 'Search not executed'
    };
  }

  const pageData = scrapedData.pageData;
  const resultsIndicators = pageData.resultsIndicators || {};
  const patterns = pageData.patterns || {};
  const structuredData = pageData.structuredData || [];

  // Determine if license was found
  const found = resultsIndicators.hasResults ||
                (patterns.licenseNumbers && patterns.licenseNumbers.length > 0) ||
                structuredData.some(table => table.dataRows && table.dataRows.length > 0);

  // Extract licenses from structured data
  const licenses = [];
  structuredData.forEach(table => {
    if (table.dataRows) {
      table.dataRows.forEach(row => {
        const license = {
          licenseNumber: row.license_number || row.license_no || row.number ||
                        row.license || patterns.licenseNumbers?.[0] || null,
          licenseType: row.license_type || row.type || patterns.licenseTypes?.[0] || null,
          status: row.status || patterns.statuses?.[0] || null,
          expirationDate: row.expiration_date || row.expires || row.expiration ||
                         patterns.dates?.[0] || null,
          issueDate: row.issue_date || row.issued || null,
          name: row.name || row.full_name || row.licensee_name || null,
          rawData: row
        };

        // Only add if we have meaningful data
        if (license.licenseNumber || license.name || license.licenseType) {
          licenses.push(license);
        }
      });
    }
  });

  return {
    found: found,
    noResults: resultsIndicators.noResults || false,
    noResultsMessage: resultsIndicators.noResultsMessage || null,
    licenses: licenses,
    licenseNumbers: patterns.licenseNumbers || [],
    licenseTypes: patterns.licenseTypes || [],
    statuses: patterns.statuses || [],
    expirationDates: patterns.dates || [],
    resultsCount: resultsIndicators.resultsCount || 0,
    employeeNameFound: resultsIndicators.employeeNameFound || false,
    pageUrl: pageData.url,
    pageTitle: pageData.pageTitle,
    patterns: patterns,
    structuredData: structuredData
  };
}

// Export all functions
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    ALL_EMPLOYEES,
    STATE_CONFIGS,
    scrapeWithDevToolsUniversal,
    searchEmployeeUniversal,
    searchAllEmployeesInState,
    searchAllEmployeesAllStates,
    extractLicenseInfoUniversal
  };
}
