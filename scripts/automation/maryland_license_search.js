/**
 * Maryland DLLR License Search Automation Script
 *
 * This script automates license searches for Kettler Management employees
 * in Maryland using the DLLR Electronic Licensing portal.
 *
 * Usage: Run via Playwright MCP browser_run_code tool
 *
 * NOTE: This site requires CAPTCHA completion. The script will:
 * 1. Fill the form
 * 2. Wait for manual CAPTCHA completion
 * 3. Execute the search
 *
 * For automated CAPTCHA solving, integrate with 2Captcha, Anti-Captcha, or CapSolver
 */

// Employee list (excluding Edward Hyland - already complete)
const employees = [
  { name: "Robert Kettler", lastName: "Kettler", firstName: "Robert", priority: "HIGH", status: "waiting_captcha" },
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
 * Search function for a single employee
 * Requires manual CAPTCHA completion
 */
async function searchEmployee(page, employee, waitForCaptcha = true) {
  console.log(`Searching for ${employee.name}...`);

  try {
    // Navigate to search page
    await page.goto('https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name');
    await page.waitForTimeout(2000);

    // Fill last name
    const lastNameInput = page.locator('input[name*="lastname"], input[name*="last_name"], input[id*="lastname"]').first();
    await lastNameInput.waitFor({ timeout: 10000 });
    await lastNameInput.fill(employee.lastName);
    await page.waitForTimeout(500);

    // Fill first name
    const firstNameInput = page.locator('input[name*="firstname"], input[name*="first_name"], input[id*="firstname"]').first();
    await firstNameInput.fill(employee.firstName);
    await page.waitForTimeout(500);

    // Wait for CAPTCHA completion (manual)
    if (waitForCaptcha) {
      console.log(`Waiting for manual CAPTCHA completion for ${employee.name}...`);

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
    const searchButton = page.locator('input[type="submit"][value*="Search"], button:has-text("Search")').first();
    await searchButton.click();
    await page.waitForTimeout(3000);

    // Evaluate results
    const results = await page.evaluate((emp) => {
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
        hasTable: hasTable,
        exactMatch: exactMatch,
        noResults: noResults,
        licenseInfo: licenseInfo,
        pageText: pageText.substring(0, 2000) // First 2000 chars for context
      };
    }, employee);

    return {
      employee: employee.name,
      searchExecuted: true,
      results: results,
      timestamp: new Date().toISOString()
    };

  } catch (error) {
    return {
      employee: employee.name,
      searchExecuted: false,
      error: error.message,
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * Main execution function
 * Run this via browser_run_code with: searchAllEmployees()
 *
 * NOTE: This will require manual CAPTCHA completion for each search
 */
async function searchAllEmployees() {
  const results = [];

  for (const employee of employees) {
    // Skip if already waiting for CAPTCHA (Robert Kettler)
    if (employee.status === "waiting_captcha") {
      console.log(`Skipping ${employee.name} - already waiting for CAPTCHA`);
      continue;
    }

    const result = await searchEmployee(page, employee, true);
    results.push(result);

    // Wait between searches
    await page.waitForTimeout(2000);
  }

  return results;
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { searchEmployee, searchAllEmployees, employees };
}
