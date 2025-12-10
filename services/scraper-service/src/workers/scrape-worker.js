/**
 * Scrape Worker
 * Processes scrape jobs from the queue
 */

const { scrapeEmployee } = require('../scraper');
const logger = require('../logger');

module.exports = async (job) => {
  const { employee, state, options } = job.data;

  logger.info(`Processing scrape job ${job.id}: ${employee.name} in ${state}`);

  try {
    // Update progress
    await job.progress(10);

    // Execute scrape
    const result = await scrapeEmployee(employee, state, options);

    // Update progress
    await job.progress(100);

    logger.info(`Job ${job.id} completed successfully`);

    return result;

  } catch (error) {
    logger.error(`Job ${job.id} failed:`, error);
    throw error;
  }
};
