// Maryland DLLR License Search with CAPTCHA Solving Service
// This script uses a CAPTCHA solving service to automate searches
// Requires: API key from 2Captcha, Anti-Captcha, or CapSolver

const { chromium } = require('playwright');

// Configuration
const MARYLAND_URL = 'https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name';
const CAPTCHA_SERVICE_API_KEY = process.env.CAPTCHA_API_KEY || 'YOUR_API_KEY_HERE';
const CAPTCHA_SERVICE = process.env.CAPTCHA_SERVICE || '2captcha'; // Options: '2captcha', 'anticaptcha', 'capsolver'

// Employees to search
const EMPLOYEES = [
  { name: 'Edward Hyland', last_name: 'Hyland', first_name: 'Edward', priority: 'HIGH' },
  { name: 'Robert Kettler', last_name: 'Kettler', first_name: 'Robert', priority: 'HIGH' },
  { name: 'Caitlin Skidmore', last_name: 'Skidmore', first_name: 'Caitlin', priority: 'HIGH' },
  { name: 'Cindy Fisher', last_name: 'Fisher', first_name: 'Cindy', priority: 'MEDIUM' },
  { name: 'Luke Davis', last_name: 'Davis', first_name: 'Luke', priority: 'MEDIUM' },
  { name: 'Pat Cassada', last_name: 'Cassada', first_name: 'Pat', priority: 'MEDIUM' },
  { name: 'Sean Curtin', last_name: 'Curtin', first_name: 'Sean', priority: 'MEDIUM' },
  { name: 'Amy Groff', last_name: 'Groff', first_name: 'Amy', priority: 'MEDIUM' },
  { name: 'Robert Grealy', last_name: 'Grealy', first_name: 'Robert', priority: 'MEDIUM' },
  { name: 'Djene Moyer', last_name: 'Moyer', first_name: 'Djene', priority: 'MEDIUM' },
  { name: 'Henry Ramos', last_name: 'Ramos', first_name: 'Henry', priority: 'MEDIUM' },
  { name: 'Kristina Thoummarath', last_name: 'Thoummarath', first_name: 'Kristina', priority: 'MEDIUM' },
  { name: 'Christina Chang', last_name: 'Chang', first_name: 'Christina', priority: 'MEDIUM' },
  { name: 'Todd Bowen', last_name: 'Bowen', first_name: 'Todd', priority: 'MEDIUM' },
  { name: 'Jeffrey Williams', last_name: 'Williams', first_name: 'Jeffrey', priority: 'MEDIUM' }
];

// Solve CAPTCHA using service
async function solveCaptcha(page) {
  console.log(`Solving CAPTCHA using ${CAPTCHA_SERVICE}...`);

  try {
    // Method 1: Using playwright-recaptcha library (if installed)
    // const { solveRecaptcha } = require('playwright-recaptcha');
    // await solveRecaptcha(page, {
    //   apiKey: CAPTCHA_SERVICE_API_KEY,
    //   provider: CAPTCHA_SERVICE
    // });

    // Method 2: Direct API integration with 2Captcha
    if (CAPTCHA_SERVICE === '2captcha') {
      return await solveWith2Captcha(page);
    }

    // Method 3: Manual fallback - wait for user to complete
    console.log('CAPTCHA service not configured. Waiting for manual completion...');
    await page.waitForFunction(
      () => {
        const button = document.querySelector('button[type="submit"], input[type="submit"]');
        return button && !button.disabled;
      },
      { timeout: 300000 } // 5 minutes
    );
    return true;

  } catch (error) {
    console.error('CAPTCHA solving error:', error);
    return false;
  }
}

// 2Captcha integration
async function solveWith2Captcha(page) {
  const axios = require('axios');

  // Get site key from page
  const siteKey = await page.evaluate(() => {
    const recaptchaFrame = document.querySelector('iframe[src*="recaptcha"]');
    if (recaptchaFrame) {
      const src = recaptchaFrame.src;
      const match = src.match(/k=([^&]+)/);
      return match ? match[1] : null;
    }
    return null;
  });

  if (!siteKey) {
    throw new Error('Could not find reCAPTCHA site key');
  }

  // Get page URL
  const pageUrl = page.url();

  // Submit CAPTCHA to 2Captcha
  const submitResponse = await axios.post('http://2captcha.com/in.php', null, {
    params: {
      key: CAPTCHA_SERVICE_API_KEY,
      method: 'userrecaptcha',
      googlekey: siteKey,
      pageurl: pageUrl,
      json: 1
    }
  });

  if (submitResponse.data.status !== 1) {
    throw new Error(`2Captcha submit failed: ' + submitResponse.data.request`);
  }

  const taskId = submitResponse.data.request;
  console.log(`CAPTCHA task submitted. Task ID: ${taskId}`);

  // Poll for solution
  let solution = null;
  for (let i = 0; i < 60; i++) {
    await new Promise(resolve => setTimeout(resolve, 5000)); // Wait 5 seconds

    const resultResponse = await axios.get('http://2captcha.com/res.php', {
      params: {
        key: CAPTCHA_SERVICE_API_KEY,
        action: 'get',
        id: taskId,
        json: 1
      }
    });

    if (resultResponse.data.status === 1) {
      solution = resultResponse.data.request;
      break;
    } else if (resultResponse.data.request !== 'CAPCHA_NOT_READY') {
      throw new Error(`2Captcha error: ${resultResponse.data.request}`);
    }
  }

  if (!solution) {
    throw new Error('CAPTCHA solution timeout');
  }

  // Inject solution into page
  await page.evaluate((token) => {
    document.getElementById('g-recaptcha-response').innerHTML = token;
    const callback = window[`___grecaptcha_cfg`].clients[0].callback;
    if (callback) {
      callback(token);
    }
  }, solution);

  // Wait for button to become enabled
  await page.waitForFunction(
    () => {
      const button = document.querySelector('button[type="submit"], input[type="submit"]');
      return button && !button.disabled;
    },
    { timeout: 10000 }
  );

  return true;
}

// Search for employee
async function searchEmployee(page, employee) {
  console.log(`\nSearching for: ${employee.name}`);

  try {
    // Navigate to search page
    await page.goto(MARYLAND_URL);
    await page.waitForTimeout(2000);

    // Fill in Last Name
    const lastNameInput = page.locator('input[type="text"]').first();
    await lastNameInput.fill(employee.last_name);
    await page.waitForTimeout(1000);

    // Solve CAPTCHA
    const captchaSolved = await solveCaptcha(page);
    if (!captchaSolved) {
      throw new Error('CAPTCHA solving failed');
    }

    // Click Search button
    const searchButton = page.locator('button[type="submit"], input[type="submit"]');
    await searchButton.click();
    await page.waitForTimeout(3000);

    // Extract results
    const results = await page.evaluate(() => {
      const allText = document.body.innerText;
      const hasEmployee = allText.toLowerCase().includes(employee.last_name.toLowerCase());
      const resultCount = allText.match(/(\d+)\s+results? found/i);
      const hasNoResults = allText.toLowerCase().includes('no results') ||
                          allText.toLowerCase().includes('no records');

      // Try to extract license details from table
      const tables = Array.from(document.querySelectorAll('table'));
      let licenseData = null;

      for (const table of tables) {
        const rows = Array.from(table.querySelectorAll('tr'));
        if (rows.length > 1 && rows[0].innerText.toLowerCase().includes('license')) {
          licenseData = rows.slice(1).map(row => {
            const cells = Array.from(row.querySelectorAll('td, th'));
            return cells.map(cell => cell.innerText.trim());
          });
          break;
        }
      }

      return {
        found: hasEmployee,
        resultCount: resultCount ? parseInt(resultCount[1]) : (hasNoResults ? 0 : 'checking'),
        licenseData: licenseData,
        pageText: allText.substring(0, 2000)
      };
    });

    return {
      employee: employee.name,
      status: 'completed',
      results: results
    };

  } catch (error) {
    console.error(`Error searching for ${employee.name}:`, error);
    return {
      employee: employee.name,
      status: 'error',
      error: error.message
    };
  }
}

// Main execution
async function main() {
  console.log('=== Maryland DLLR License Search with CAPTCHA Service ===\n');
  console.log(`Service: ${CAPTCHA_SERVICE}`);
  console.log(`Total Employees: ${EMPLOYEES.length}\n`);

  if (CAPTCHA_SERVICE_API_KEY === 'YOUR_API_KEY_HERE') {
    console.log('⚠️  WARNING: CAPTCHA_API_KEY not set. Using manual CAPTCHA mode.');
    console.log('Set environment variable: export CAPTCHA_API_KEY=your_key_here\n');
  }

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  const results = [];

  // Search high priority first
  const highPriority = EMPLOYEES.filter(e => e.priority === 'HIGH');
  const mediumPriority = EMPLOYEES.filter(e => e.priority === 'MEDIUM');

  console.log('=== HIGH PRIORITY SEARCHES ===');
  for (const employee of highPriority) {
    const result = await searchEmployee(page, employee);
    results.push(result);
    await page.waitForTimeout(2000); // Rate limiting
  }

  console.log('\n=== MEDIUM PRIORITY SEARCHES ===');
  for (const employee of mediumPriority) {
    const result = await searchEmployee(page, employee);
    results.push(result);
    await page.waitForTimeout(2000); // Rate limiting
  }

  await browser.close();

  // Save results
  const fs = require('fs');
  const path = require('path');
  const outputDir = path.join(__dirname, '../../research/license_searches/maryland');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const outputFile = path.join(outputDir, 'maryland_captcha_service_results.json');
  fs.writeFileSync(outputFile, JSON.stringify({
    metadata: {
      date: new Date().toISOString(),
      service: CAPTCHA_SERVICE,
      total_searches: EMPLOYEES.length,
      completed: results.filter(r => r.status === 'completed').length,
      errors: results.filter(r => r.status === 'error').length
    },
    results: results
  }, null, 2));

  console.log(`\n✅ Results saved to: ${outputFile}`);
  console.log(`Completed: ${results.filter(r => r.status === 'completed').length}/${EMPLOYEES.length}`);
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { searchEmployee, solveCaptcha };
