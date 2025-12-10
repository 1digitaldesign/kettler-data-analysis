/**
 * Connecticut DCP License Search - DevTools Enhanced Version
 *
 * This script uses Chrome DevTools capabilities for enhanced data extraction
 * and better reliability.
 */

// Import DevTools scraping functions
const { scrapeWithDevTools, extractLicenseInfo, scrapeConnecticut } = require('./scrape_with_devtools.js');

// Employee list
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
 * Search employee with DevTools enhanced scraping
 */
async function searchEmployeeWithDevTools(page, employee) {
  console.log(`[DevTools] Searching for ${employee.name} (${employee.licenseType})...`);

  try {
    // Use DevTools scraping function
    const scrapedData = await scrapeConnecticut(page, employee);

    // Extract license information
    const licenseInfo = extractLicenseInfo(scrapedData);

    // Log results
    console.log(`[DevTools] Results for ${employee.name}:`);
    console.log(`  - Found: ${licenseInfo.found}`);
    console.log(`  - No Results: ${licenseInfo.noResults}`);
    console.log(`  - Results Count: ${licenseInfo.resultsCount}`);
    if (licenseInfo.licenses.length > 0) {
      console.log(`  - Licenses: ${licenseInfo.licenses.length}`);
      licenseInfo.licenses.forEach((license, index) => {
        console.log(`    ${index + 1}. ${license.licenseNumber || 'N/A'} - ${license.status || 'N/A'}`);
      });
    }

    return {
      employee: employee.name,
      licenseType: employee.licenseType,
      searchExecuted: scrapedData.searchExecuted,
      licenseInfo: licenseInfo,
      scrapedData: {
        performance: scrapedData.pageData?.performance,
        domStats: scrapedData.pageData?.domStats,
        networkRequests: scrapedData.networkRequests?.length || 0
      },
      timestamp: new Date().toISOString()
    };

  } catch (error) {
    console.error(`[DevTools] Error searching for ${employee.name}:`, error);
    return {
      employee: employee.name,
      licenseType: employee.licenseType,
      searchExecuted: false,
      error: error.message,
      stack: error.stack,
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * Search all employees with DevTools
 */
async function searchAllEmployeesWithDevTools() {
  console.log('[DevTools] Starting batch search with DevTools enhancement...');
  const results = [];

  for (const employee of employees) {
    const result = await searchEmployeeWithDevTools(page, employee);
    results.push(result);

    // Log summary
    if (result.searchExecuted) {
      const status = result.licenseInfo?.found ? 'LICENSE FOUND' : 'NO LICENSE';
      console.log(`✓ ${employee.name}: ${status}`);
    } else {
      console.log(`✗ ${employee.name}: ERROR - ${result.error}`);
    }

    // Wait between searches
    await page.waitForTimeout(2000);
  }

  // Summary
  console.log('\n[DevTools] Search Summary:');
  const successful = results.filter(r => r.searchExecuted).length;
  const found = results.filter(r => r.licenseInfo?.found).length;
  const errors = results.filter(r => !r.searchExecuted).length;

  console.log(`  - Total: ${results.length}`);
  console.log(`  - Successful: ${successful}`);
  console.log(`  - Licenses Found: ${found}`);
  console.log(`  - Errors: ${errors}`);

  return results;
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    searchEmployeeWithDevTools,
    searchAllEmployeesWithDevTools,
    employees
  };
}

// If running directly
if (typeof page !== 'undefined') {
  searchAllEmployeesWithDevTools().then(results => {
    console.log('\n[DevTools] All searches complete');
    console.log('Results:', JSON.stringify(results, null, 2));
  }).catch(error => {
    console.error('[DevTools] Batch search failed:', error);
  });
}
