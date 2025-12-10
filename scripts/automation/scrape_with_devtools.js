/**
 * Advanced Web Scraping with Chrome DevTools Integration
 *
 * This script uses Chrome DevTools Protocol features to scrape license information
 * with better reliability and data extraction capabilities.
 *
 * Features:
 * - Network monitoring
 * - DOM inspection
 * - Console logging
 * - Performance monitoring
 * - Structured data extraction
 */

/**
 * Enhanced page evaluation with DevTools-like inspection
 */
async function scrapeWithDevTools(page, employee, state) {
  console.log(`[DevTools] Scraping ${employee.name} in ${state}...`);

  try {
    // Enable console logging
    page.on('console', msg => {
      if (msg.type() === 'error') {
        console.error(`[Console Error] ${msg.text()}`);
      }
    });

    // Monitor network requests
    const networkRequests = [];
    page.on('request', request => {
      networkRequests.push({
        url: request.url(),
        method: request.method(),
        resourceType: request.resourceType()
      });
    });

    // Wait for page load with DevTools inspection
    await page.waitForLoadState('networkidle');

    // Use DevTools evaluation to get comprehensive page data
    const pageData = await page.evaluate((emp, stateName) => {
      // Get all performance metrics
      const performance = window.performance;
      const timing = performance.timing;

      // Extract all tables
      const tables = Array.from(document.querySelectorAll('table')).map((table, index) => {
        const rows = Array.from(table.querySelectorAll('tr')).map(row => {
          const cells = Array.from(row.querySelectorAll('td, th')).map(cell => ({
            text: cell.innerText.trim(),
            colspan: cell.colSpan || 1,
            rowspan: cell.rowSpan || 1
          }));
          return {
            cells: cells,
            rowText: row.innerText.trim()
          };
        });
        return {
          index: index,
          id: table.id || null,
          className: table.className || null,
          rowCount: rows.length,
          rows: rows,
          fullText: table.innerText.trim()
        };
      });

      // Extract all forms
      const forms = Array.from(document.querySelectorAll('form')).map((form, index) => {
        const inputs = Array.from(form.querySelectorAll('input, select, textarea')).map(input => ({
          type: input.type || input.tagName.toLowerCase(),
          name: input.name || null,
          id: input.id || null,
          value: input.value || null,
          placeholder: input.placeholder || null,
          label: input.labels && input.labels.length > 0 ? input.labels[0].innerText : null
        }));
        return {
          index: index,
          id: form.id || null,
          action: form.action || null,
          method: form.method || 'GET',
          inputs: inputs
        };
      });

      // Extract license-specific data
      const licenseData = {
        employeeName: emp.name,
        state: stateName,
        pageTitle: document.title,
        url: window.location.href,
        timestamp: new Date().toISOString(),

        // Search for license information patterns
        licenseNumbers: [],
        licenseTypes: [],
        statuses: [],
        expirationDates: [],

        // Text analysis
        bodyText: document.body.innerText,
        bodyTextLower: document.body.innerText.toLowerCase(),

        // Check for results indicators
        hasResults: false,
        noResultsMessage: null,
        resultsCount: 0
      };

      // Extract license numbers (common patterns)
      const licensePatterns = [
        /\b[A-Z]{1,3}\d{4,10}\b/g,  // e.g., BR40000429, CT12345
        /\b\d{4,10}\b/g,             // Numeric only
        /License\s*(?:#|Number|No\.?)\s*:?\s*([A-Z0-9-]+)/gi,
        /License\s+([A-Z0-9-]+)/gi
      ];

      licensePatterns.forEach(pattern => {
        const matches = document.body.innerText.match(pattern);
        if (matches) {
          licenseData.licenseNumbers.push(...matches.map(m => m.trim()));
        }
      });

      // Extract license types
      const licenseTypePatterns = [
        /Real\s+Estate\s+Broker/gi,
        /Real\s+Estate\s+Salesperson/gi,
        /Broker/gi,
        /Salesperson/gi
      ];

      licenseTypePatterns.forEach(pattern => {
        const matches = document.body.innerText.match(pattern);
        if (matches) {
          licenseData.licenseTypes.push(...matches.map(m => m.trim()));
        }
      });

      // Check for status indicators
      const statusPatterns = [
        /Status\s*:?\s*(Active|Inactive|Expired|Pending|Suspended)/gi,
        /(Active|Inactive|Expired|Pending|Suspended)/gi
      ];

      statusPatterns.forEach(pattern => {
        const matches = document.body.innerText.match(pattern);
        if (matches) {
          licenseData.statuses.push(...matches.map(m => m.trim()));
        }
      });

      // Extract expiration dates
      const datePatterns = [
        /Expiration\s*(?:Date|Dt\.?)\s*:?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/gi,
        /Expires?\s*:?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/gi,
        /(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/g
      ];

      datePatterns.forEach(pattern => {
        const matches = document.body.innerText.match(pattern);
        if (matches) {
          licenseData.expirationDates.push(...matches.map(m => m.trim()));
        }
      });

      // Check for results
      const noResultsPatterns = [
        /no\s+results?/gi,
        /no\s+records?\s+found/gi,
        /no\s+matches?/gi,
        /no\s+licenses?/gi,
        /not\s+found/gi
      ];

      noResultsPatterns.forEach(pattern => {
        if (pattern.test(document.body.innerText)) {
          licenseData.hasResults = false;
          licenseData.noResultsMessage = document.body.innerText.match(pattern)?.[0] || 'No results found';
        }
      });

      // Count results in tables
      tables.forEach(table => {
        const empNameLower = emp.name.toLowerCase();
        const lastNameLower = emp.lastName.toLowerCase();
        const firstNameLower = emp.firstName.toLowerCase();

        table.rows.forEach(row => {
          const rowTextLower = row.rowText.toLowerCase();
          if (rowTextLower.includes(lastNameLower) && rowTextLower.includes(firstNameLower)) {
            licenseData.hasResults = true;
            licenseData.resultsCount++;
          }
        });
      });

      // Extract structured data from tables
      const structuredData = tables.map(table => {
        // Try to identify header row
        const headerRow = table.rows[0];
        const headers = headerRow ? headerRow.cells.map(c => c.text) : [];

        // Extract data rows
        const dataRows = table.rows.slice(1).map(row => {
          const rowData = {};
          row.cells.forEach((cell, index) => {
            const header = headers[index] || `column_${index}`;
            rowData[header.toLowerCase().replace(/\s+/g, '_')] = cell.text;
          });
          return rowData;
        });

        return {
          headers: headers,
          dataRows: dataRows,
          rowCount: dataRows.length
        };
      });

      return {
        performance: {
          loadTime: timing.loadEventEnd - timing.navigationStart,
          domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
          pageLoad: timing.loadEventEnd - timing.navigationStart
        },
        tables: tables,
        forms: forms,
        licenseData: licenseData,
        structuredData: structuredData,
        domStats: {
          totalElements: document.querySelectorAll('*').length,
          tables: document.querySelectorAll('table').length,
          forms: document.querySelectorAll('form').length,
          links: document.querySelectorAll('a').length,
          images: document.querySelectorAll('img').length
        }
      };
    }, employee, state);

    return {
      employee: employee.name,
      state: state,
      searchExecuted: true,
      pageData: pageData,
      networkRequests: networkRequests.slice(0, 20), // Limit to first 20 requests
      timestamp: new Date().toISOString()
    };

  } catch (error) {
    return {
      employee: employee.name,
      state: state,
      searchExecuted: false,
      error: error.message,
      stack: error.stack,
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * Extract license information from scraped data
 */
function extractLicenseInfo(scrapedData) {
  if (!scrapedData.searchExecuted || !scrapedData.pageData) {
    return {
      found: false,
      error: scrapedData.error || 'Search not executed'
    };
  }

  const licenseData = scrapedData.pageData.licenseData;
  const structuredData = scrapedData.pageData.structuredData;

  // Check if license was found
  const found = licenseData.hasResults ||
                licenseData.licenseNumbers.length > 0 ||
                structuredData.some(table => table.dataRows.length > 0);

  // Extract license details from structured data
  const licenses = [];
  structuredData.forEach(table => {
    table.dataRows.forEach(row => {
      const license = {
        licenseNumber: row.license_number || row.license_no || row.number || null,
        licenseType: row.license_type || row.type || null,
        status: row.status || null,
        expirationDate: row.expiration_date || row.expires || row.expiration || null,
        name: row.name || row.full_name || null,
        rawData: row
      };

      if (license.licenseNumber || license.name) {
        licenses.push(license);
      }
    });
  });

  return {
    found: found,
    noResults: !found && licenseData.noResultsMessage !== null,
    noResultsMessage: licenseData.noResultsMessage,
    licenses: licenses,
    licenseNumbers: [...new Set(licenseData.licenseNumbers)],
    licenseTypes: [...new Set(licenseData.licenseTypes)],
    statuses: [...new Set(licenseData.statuses)],
    expirationDates: [...new Set(licenseData.expirationDates)],
    resultsCount: licenseData.resultsCount,
    pageUrl: licenseData.url,
    pageTitle: licenseData.pageTitle
  };
}

/**
 * Scrape Connecticut license search
 */
async function scrapeConnecticut(page, employee) {
  console.log(`[DevTools] Scraping Connecticut for ${employee.name}...`);

  // Navigate to Connecticut search page
  await page.goto('https://www.elicense.ct.gov/lookup/licenselookup.aspx', {
    waitUntil: 'networkidle',
    timeout: 60000
  });

  // Select license type
  const licenseType = employee.licenseType || 'REAL ESTATE BROKER';
  await page.selectOption('select[name*="LicenseType"], select[id*="LicenseType"]', {
    label: licenseType
  });

  // Fill form
  await page.fill('input[name*="LastName"], input[id*="LastName"]', employee.lastName);
  await page.fill('input[name*="FirstName"], input[id*="FirstName"]', employee.firstName);

  // Submit
  await page.click('input[type="submit"], button[type="submit"], input[value*="Search"]');
  await page.waitForLoadState('networkidle');

  // Scrape with DevTools
  return await scrapeWithDevTools(page, employee, 'Connecticut');
}

/**
 * Scrape Maryland license search
 */
async function scrapeMaryland(page, employee) {
  console.log(`[DevTools] Scraping Maryland for ${employee.name}...`);

  // Navigate to Maryland search page
  await page.goto('https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name', {
    waitUntil: 'networkidle',
    timeout: 60000
  });

  // Fill form
  await page.fill('input[name*="lastname"], input[name*="last_name"]', employee.lastName);
  await page.fill('input[name*="firstname"], input[name*="first_name"]', employee.firstName);

  // Wait for CAPTCHA (manual completion required)
  console.log('Waiting for CAPTCHA completion...');
  await page.waitForTimeout(10000); // Give time for manual CAPTCHA

  // Submit
  await page.click('input[type="submit"][value*="Search"]');
  await page.waitForLoadState('networkidle');

  // Scrape with DevTools
  return await scrapeWithDevTools(page, employee, 'Maryland');
}

// Export functions
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    scrapeWithDevTools,
    extractLicenseInfo,
    scrapeConnecticut,
    scrapeMaryland
  };
}
