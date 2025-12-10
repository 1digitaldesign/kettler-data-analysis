/**
 * Connecticut DCP License Search Automation Script
 *
 * This script automates license searches for Kettler Management employees
 * in Connecticut using the eLicense portal.
 *
 * Usage: Run via Playwright MCP browser_run_code tool
 *
 * License Types:
 * - REAL ESTATE BROKER: For executives/managers
 * - REAL ESTATE SALESPERSON: For staff/property managers
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
 * Search function for a single employee
 */
async function searchEmployee(page, employee) {
  console.log(`Searching for ${employee.name} (${employee.licenseType})...`);

  try {
    // Navigate to search page
    await page.goto('https://www.elicense.ct.gov/lookup/licenselookup.aspx');
    await page.waitForTimeout(2000);

    // Select license type dropdown
    const licenseTypeSelect = page.locator('select[name*="LicenseType"], select[id*="LicenseType"]').first();
    await licenseTypeSelect.waitFor({ timeout: 10000 });
    await licenseTypeSelect.selectOption({ label: employee.licenseType });
    await page.waitForTimeout(1000);

    // Fill last name
    const lastNameInput = page.locator('input[name*="LastName"], input[id*="LastName"]').first();
    await lastNameInput.fill(employee.lastName);
    await page.waitForTimeout(500);

    // Fill first name
    const firstNameInput = page.locator('input[name*="FirstName"], input[id*="FirstName"]').first();
    await firstNameInput.fill(employee.firstName);
    await page.waitForTimeout(500);

    // Click search button
    const searchButton = page.locator('input[type="submit"], button[type="submit"], input[value*="Search"], button:has-text("Search")').first();
    await searchButton.click();
    await page.waitForTimeout(3000);

    // Evaluate results
    const results = await page.evaluate((emp) => {
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
        hasResults: hasResults,
        nameFound: nameFound,
        noResults: noResults,
        pageText: document.body.innerText.substring(0, 1000) // First 1000 chars for context
      };
    }, employee);

    return {
      employee: employee.name,
      licenseType: employee.licenseType,
      searchExecuted: true,
      results: results,
      timestamp: new Date().toISOString()
    };

  } catch (error) {
    return {
      employee: employee.name,
      licenseType: employee.licenseType,
      searchExecuted: false,
      error: error.message,
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * Main execution function
 * Run this via browser_run_code with: searchAllEmployees()
 */
async function searchAllEmployees() {
  const results = [];

  for (const employee of employees) {
    const result = await searchEmployee(page, employee);
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
