/**
 * Complete Virginia License Searches for All Employees
 *
 * Searches Virginia DPOR for all 15 Kettler employees
 */

const employees = [
  { name: "Robert Kettler", lastName: "Kettler", firstName: "Robert" },
  { name: "Caitlin Skidmore", lastName: "Skidmore", firstName: "Caitlin" },
  { name: "Cindy Fisher", lastName: "Fisher", firstName: "Cindy" },
  { name: "Pat Cassada", lastName: "Cassada", firstName: "Pat" },
  { name: "Luke Davis", lastName: "Davis", firstName: "Luke" },
  { name: "Sean Curtin", lastName: "Curtin", firstName: "Sean" },
  { name: "Robert Grealy", lastName: "Grealy", firstName: "Robert" },
  { name: "Todd Bowen", lastName: "Bowen", firstName: "Todd" },
  { name: "Amy Groff", lastName: "Groff", firstName: "Amy" },
  { name: "Kristina Thoummarath", lastName: "Thoummarath", firstName: "Kristina" },
  { name: "Christina Chang", lastName: "Chang", firstName: "Christina" },
  { name: "Jeffrey Williams", lastName: "Williams", firstName: "Jeffrey" },
  { name: "Edward Hyland", lastName: "Hyland", firstName: "Edward" },
  { name: "Djene Moyer", lastName: "Moyer", firstName: "Djene" },
  { name: "Henry Ramos", lastName: "Ramos", firstName: "Henry" }
];

async function searchVirginiaEmployee(page, employee) {
  console.log(`Searching Virginia DPOR for: ${employee.name}`);

  try {
    // Navigate to search page
    await page.goto('https://www.dpor.virginia.gov/LicenseLookup', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    // Wait for iframe to load
    const iframe = await page.frameLocator('iframe').first();

    // Fill search box with full name
    const searchBox = iframe.locator('textbox[name*="Search"], textbox[placeholder*="Search"]').first();
    await searchBox.fill(`${employee.firstName} ${employee.lastName}`);

    // Click search button
    const searchButton = iframe.locator('button:has-text("Search")').first();
    await searchButton.click();

    // Wait for results
    await page.waitForTimeout(3000);

    // Extract results
    const results = await iframe.evaluate((emp) => {
      const bodyText = document.body.innerText.toLowerCase();
      const empNameLower = `${emp.firstName} ${emp.lastName}`.toLowerCase();

      // Check if employee name appears in results
      const hasName = bodyText.includes(empNameLower) ||
                      bodyText.includes(emp.lastName.toLowerCase());

      // Look for license numbers (pattern: alphanumeric codes)
      const licensePattern = /license\s*(?:number|#)?\s*:?\s*([A-Z0-9-]+)/gi;
      const licenseMatches = bodyText.match(licensePattern);

      // Look for "real estate" mentions
      const hasRealEstate = bodyText.includes('real estate') ||
                           bodyText.includes('realtor') ||
                           bodyText.includes('broker') ||
                           bodyText.includes('salesperson');

      return {
        employee: emp.name,
        searchExecuted: true,
        nameFound: hasName,
        hasRealEstateLicense: hasName && hasRealEstate,
        licenseMatches: licenseMatches || [],
        bodyText: document.body.innerText.substring(0, 2000),
        hasResults: bodyText.length > 500
      };
    }, employee);

    return {
      ...results,
      state: "Virginia",
      searchDate: new Date().toISOString().split('T')[0]
    };

  } catch (error) {
    console.error(`Error searching ${employee.name}:`, error);
    return {
      employee: employee.name,
      state: "Virginia",
      searchExecuted: false,
      error: error.message,
      searchDate: new Date().toISOString().split('T')[0]
    };
  }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { searchVirginiaEmployee, employees };
}
