/**
 * Maryland DLLR License Search Automation Script - IMPROVED VERSION
 *
 * This script automates license searches with better blank page handling
 * and improved error diagnostics.
 *
 * NOTE: This site requires CAPTCHA completion. The script will:
 * 1. Fill the form
 * 2. Wait for manual CAPTCHA completion
 * 3. Execute the search
 */

// Employee list
const employees = [
  { name: "Robert Kettler", lastName: "Kettler", firstName: "Robert", priority: "HIGH", status: "pending" },
  { name: "Caitlin Skidmore", lastName: "Skidmore", firstName: "Caitlin", priority: "HIGH", status: "pending" },
  { name: "Cindy Fisher", lastName: "Fisher", firstName: "Cindy", priority: "MEDIUM", status: "pending" },
  { name: "Luke Davis", lastName: "Davis", firstName: "Luke", priority: "MEDIUM", status: "pending" },
  { name: "Pat Cassada", lastName: "Cassada", firstName: "Pat", priority: "MEDIUM", status: "pending" },
  { name: "Sean Curtin", lastName: "Curtin", firstName: "Sean", priority: "MEDIUM", status: "pending" },
  { name: "Amy Groff", lastName: "Groff", firstName: "Amy", priority: "MEDIUM", status: "pending" },
  { name: "Robert Grealy", lastName: "Grealy", firstName: "Robert", priority: "MEDIUM", status: "pending" },
  { name: "Djene Moyer", lastName: "Moyer", firstName: "Djene", priority: "MEDIUM", status: "pending" },
  { name: "Henry Ramos", lastName: "Ramos", firstName: "Henry", priority: "MEDIUM", status: "pending" },
  { name: "Kristina Thoummarath", lastName: "Thoummarath", firstName: "Kristina", priority: "MEDIUM", status: "pending" },
  { name: "Christina Chang", lastName: "Chang", firstName: "Christina", priority: "MEDIUM", status: "pending" },
  { name: "Todd Bowen", lastName: "Bowen", firstName: "Todd", priority: "MEDIUM", status: "pending" },
  { name: "Jeffrey Williams", lastName: "Williams", firstName: "Jeffrey", priority: "MEDIUM", status: "pending" }
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
async function searchEmployee(page, employee, waitForCaptcha = true) {
  console.log(`Searching for ${employee.name}...`);

  try {
    // Navigate to search page with better options
    console.log('Navigating to search page...');
    await page.goto('https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name', {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    // Wait for page to be fully loaded (not blank)
    console.log('Waiting for page to load...');
    await waitForPageLoad(page);

    // Verify page loaded correctly
    const pageTitle = await page.title();
    console.log(`Page loaded: ${pageTitle}`);

    await page.waitForTimeout(2000);

    // Fill last name with better error handling
    console.log('Filling last name...');
    const lastNameInput = page.locator('input[name*="lastname"], input[name*="last_name"], input[id*="lastname"]').first();
    await lastNameInput.waitFor({ state: 'visible', timeout: 15000 });
    await lastNameInput.fill(employee.lastName);
    await page.waitForTimeout(500);

    // Fill first name
    console.log('Filling first name...');
    const firstNameInput = page.locator('input[name*="firstname"], input[name*="first_name"], input[id*="firstname"]').first();
    await firstNameInput.waitFor({ state: 'visible', timeout: 15000 });
    await firstNameInput.fill(employee.firstName);
    await page.waitForTimeout(500);

    // Wait for CAPTCHA completion (manual)
    if (waitForCaptcha) {
      console.log(`Waiting for manual CAPTCHA completion for ${employee.name}...`);
      console.log('Please complete the CAPTCHA in the browser window...');

      // Wait for search button to become enabled (indicates CAPTCHA completed)
      const searchButton = page.locator('input[type="submit"][value*="Search"], button:has-text("Search"), input[type="submit"]:not([disabled])').first();

      // Poll for button to become enabled (CAPTCHA completion)
      let attempts = 0;
      const maxAttempts = 300; // 5 minutes max wait

      while (attempts < maxAttempts) {
        const isDisabled = await searchButton.getAttribute('disabled');
        if (!isDisabled) {
          console.log(`CAPTCHA completed for ${employee.name}`);
          break;
        }
        await page.waitForTimeout(1000);
        attempts++;
      }

      if (attempts >= maxAttempts) {
        return {
          employee: employee.name,
          searchExecuted: false,
          error: "CAPTCHA timeout - manual completion required",
          timestamp: new Date().toISOString()
        };
      }
    }

    // Click search button
    console.log('Clicking search button...');
    const searchButton = page.locator('input[type="submit"][value*="Search"], button:has-text("Search")').first();
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

      const pageText = document.body.innerText;
      const pageTextLower = pageText.toLowerCase();
      const empNameLower = emp.name.toLowerCase();
      const lastNameLower = emp.lastName.toLowerCase();
      const firstNameLower = emp.firstName.toLowerCase();

      // Check for results table
      const resultsTable = document.querySelector('table, .results, #results');
      const hasTable = resultsTable !== null;

      // Check for exact name match
      const exactMatch = pageTextLower.includes(empNameLower) ||
                        (pageTextLower.includes(lastNameLower) && pageTextLower.includes(firstNameLower));

      // Check for "no results" messages
      const noResults = pageTextLower.includes('no results') ||
                       pageTextLower.includes('no records found') ||
                       pageTextLower.includes('no matches') ||
                       pageTextLower.includes('no license found');

      // Extract license information if found
      let licenseInfo = null;
      if (exactMatch && hasTable) {
        const rows = resultsTable.querySelectorAll('tr');
        for (const row of rows) {
          const rowText = row.innerText.toLowerCase();
          if (rowText.includes(lastNameLower) && rowText.includes(firstNameLower)) {
            licenseInfo = {
              name: row.cells[0]?.innerText || '',
              licenseNumber: row.cells[1]?.innerText || '',
              status: row.cells[2]?.innerText || '',
              expiration: row.cells[3]?.innerText || ''
            };
            break;
          }
        }
      }

      return {
        hasContent: true,
        hasTable: hasTable,
        exactMatch: exactMatch,
        noResults: noResults,
        licenseInfo: licenseInfo,
        pageText: pageText.substring(0, 2000),
        pageTitle: document.title,
        url: window.location.href
      };
    }, employee);

    if (results.error) {
      throw new Error(results.error);
    }

    return {
      employee: employee.name,
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
    const result = await searchEmployee(page, employee, true);
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
