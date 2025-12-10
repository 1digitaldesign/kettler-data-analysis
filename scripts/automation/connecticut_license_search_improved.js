/**
 * Connecticut DCP License Search Automation Script - IMPROVED VERSION
 *
 * This script automates license searches with better blank page handling
 * and improved error diagnostics.
 *
 * Usage: Run via Playwright MCP browser_run_code tool
 */

// Employee list with appropriate license types
const employees = [
  { name: "Caitlin Skidmore", lastName: "Skidmore", firstName: "Caitlin", licenseType: "REAL ESTATE BROKER", priority: "HIGH" },
  { name: "Cindy Fisher", lastName: "Fisher", firstName: "Cindy", licenseType: "REAL ESTATE BROKER", priority: "MEDIUM" },
  { name: "Luke Davis", lastName: "Davis", firstName: "Luke", licenseType: "REAL ESTATE BROKER", priority: "MEDIUM" },
  { name: "Pat Cassada", lastName: "Cassada", firstName: "Pat", licenseType: "REAL ESTATE BROKER", priority: "MEDIUM" },
  { name: "Sean Curtin", lastName: "Curtin", firstName: "Sean", licenseType: "REAL ESTATE BROKER", priority: "MEDIUM" },
  { name: "Amy Groff", lastName: "Groff", firstName: "Amy", licenseType: "REAL ESTATE SALESPERSON", priority: "MEDIUM" },
  { name: "Robert Grealy", lastName: "Grealy", firstName: "Robert", licenseType: "REAL ESTATE BROKER", priority: "MEDIUM" },
  { name: "Djene Moyer", lastName: "Moyer", firstName: "Djene", licenseType: "REAL ESTATE SALESPERSON", priority: "MEDIUM" },
  { name: "Henry Ramos", lastName: "Ramos", firstName: "Henry", licenseType: "REAL ESTATE SALESPERSON", priority: "MEDIUM" },
  { name: "Kristina Thoummarath", lastName: "Thoummarath", firstName: "Kristina", licenseType: "REAL ESTATE SALESPERSON", priority: "MEDIUM" },
  { name: "Christina Chang", lastName: "Chang", firstName: "Christina", licenseType: "REAL ESTATE SALESPERSON", priority: "MEDIUM" },
  { name: "Todd Bowen", lastName: "Bowen", firstName: "Todd", licenseType: "REAL ESTATE BROKER", priority: "MEDIUM" },
  { name: "Jeffrey Williams", lastName: "Williams", firstName: "Jeffrey", licenseType: "REAL ESTATE SALESPERSON", priority: "MEDIUM" }
];

/**
 * Wait for page to be fully loaded (not blank)
 */
async function waitForPageLoad(page, timeout = 30000) {
  try {
    // Wait for network to be idle
    await page.waitForLoadState('networkidle', { timeout });

    // Wait for DOM content
    await page.waitForLoadState('domcontentloaded', { timeout });

    // Check if page has content
    const hasContent = await page.evaluate(() => {
      return document.body && document.body.innerText.trim().length > 0;
    });

    if (!hasContent) {
      // Wait a bit more for JavaScript to render
      await page.waitForTimeout(3000);

      // Check again
      const hasContentAfterWait = await page.evaluate(() => {
        return document.body && document.body.innerText.trim().length > 0;
      });

      if (!hasContentAfterWait) {
        throw new Error('Page appears blank after waiting');
      }
    }

    return true;
  } catch (error) {
    // Get page diagnostics
    const diagnostics = await page.evaluate(() => {
      return {
        url: window.location.href,
        title: document.title,
        bodyText: document.body ? document.body.innerText.substring(0, 200) : 'No body',
        bodyLength: document.body ? document.body.innerText.length : 0,
        readyState: document.readyState,
        hasScripts: document.scripts.length > 0
      };
    });

    console.error('Page load diagnostics:', diagnostics);
    throw error;
  }
}

/**
 * Search function for a single employee with improved blank page handling
 */
async function searchEmployee(page, employee) {
  console.log(`Searching for ${employee.name} (${employee.licenseType})...`);

  try {
    // Navigate to search page with better options
    console.log('Navigating to search page...');
    await page.goto('https://www.elicense.ct.gov/lookup/licenselookup.aspx', {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    // Wait for page to be fully loaded (not blank)
    console.log('Waiting for page to load...');
    await waitForPageLoad(page);

    // Verify page loaded correctly
    const pageTitle = await page.title();
    console.log(`Page loaded: ${pageTitle}`);

    // Wait for form elements to be visible
    await page.waitForTimeout(2000);

    // Select license type dropdown with better error handling
    console.log('Selecting license type...');
    const licenseTypeSelect = page.locator('select[name*="LicenseType"], select[id*="LicenseType"]').first();
    await licenseTypeSelect.waitFor({ state: 'visible', timeout: 15000 });
    await licenseTypeSelect.selectOption({ label: employee.licenseType });
    await page.waitForTimeout(1000);

    // Fill last name
    console.log('Filling last name...');
    const lastNameInput = page.locator('input[name*="LastName"], input[id*="LastName"]').first();
    await lastNameInput.waitFor({ state: 'visible', timeout: 10000 });
    await lastNameInput.fill(employee.lastName);
    await page.waitForTimeout(500);

    // Fill first name
    console.log('Filling first name...');
    const firstNameInput = page.locator('input[name*="FirstName"], input[id*="FirstName"]').first();
    await firstNameInput.waitFor({ state: 'visible', timeout: 10000 });
    await firstNameInput.fill(employee.firstName);
    await page.waitForTimeout(500);

    // Click search button
    console.log('Clicking search button...');
    const searchButton = page.locator('input[type="submit"], button[type="submit"], input[value*="Search"], button:has-text("Search")').first();
    await searchButton.waitFor({ state: 'visible', timeout: 10000 });
    await searchButton.click();

    // Wait for results page to load
    console.log('Waiting for results...');
    await page.waitForLoadState('networkidle', { timeout: 30000 });
    await waitForPageLoad(page);
    await page.waitForTimeout(3000);

    // Evaluate results with better error handling
    console.log('Evaluating results...');
    const results = await page.evaluate((emp) => {
      // Check if page has content
      if (!document.body || document.body.innerText.trim().length === 0) {
        return {
          error: 'Page is blank',
          hasContent: false
        };
      }

      const pageText = document.body.innerText.toLowerCase();
      const empNameLower = emp.name.toLowerCase();

      // Check if results table exists
      const resultsTable = document.querySelector('table, .results-table, #results');
      const hasResults = resultsTable && resultsTable.innerText.length > 0;

      // Check for exact name match
      const nameFound = pageText.includes(empNameLower) ||
                       pageText.includes(emp.lastName.toLowerCase()) ||
                       pageText.includes(emp.firstName.toLowerCase());

      // Check for "no results" messages
      const noResults = pageText.includes('no results') ||
                       pageText.includes('no records found') ||
                       pageText.includes('no matches');

      return {
        hasContent: true,
        hasResults: hasResults,
        nameFound: nameFound,
        noResults: noResults,
        pageText: document.body.innerText.substring(0, 1000),
        pageTitle: document.title,
        url: window.location.href
      };
    }, employee);

    if (results.error) {
      throw new Error(results.error);
    }

    return {
      employee: employee.name,
      licenseType: employee.licenseType,
      searchExecuted: true,
      results: results,
      timestamp: new Date().toISOString()
    };

  } catch (error) {
    // Get page diagnostics on error
    let diagnostics = null;
    try {
      diagnostics = await page.evaluate(() => {
        return {
          url: window.location.href,
          title: document.title,
          bodyText: document.body ? document.body.innerText.substring(0, 500) : 'No body',
          bodyLength: document.body ? document.body.innerText.length : 0,
          readyState: document.readyState
        };
      });
    } catch (e) {
      diagnostics = { error: 'Could not get diagnostics' };
    }

    return {
      employee: employee.name,
      licenseType: employee.licenseType,
      searchExecuted: false,
      error: error.message,
      diagnostics: diagnostics,
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * Main execution function
 */
async function searchAllEmployees() {
  const results = [];

  for (const employee of employees) {
    const result = await searchEmployee(page, employee);
    results.push(result);

    // Log result
    if (result.searchExecuted) {
      console.log(`✓ ${employee.name}: ${result.results.noResults ? 'No license found' : 'Results found'}`);
    } else {
      console.log(`✗ ${employee.name}: Error - ${result.error}`);
    }

    // Wait between searches
    await page.waitForTimeout(2000);
  }

  return results;
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { searchEmployee, searchAllEmployees, employees, waitForPageLoad };
}

// If running directly, execute
if (typeof page !== 'undefined') {
  searchAllEmployees().then(results => {
    console.log('Search complete:', results);
  }).catch(error => {
    console.error('Search failed:', error);
  });
}
