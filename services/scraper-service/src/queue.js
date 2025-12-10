/**
 * Redis Queue Configuration
 * Uses Bull for job queue management
 */

const Queue = require('bull');
const logger = require('./logger');

const REDIS_HOST = process.env.REDIS_HOST || 'redis';
const REDIS_PORT = process.env.REDIS_PORT || 6379;
const REDIS_PASSWORD = process.env.REDIS_PASSWORD || '';

const redisConfig = {
  host: REDIS_HOST,
  port: REDIS_PORT,
  ...(REDIS_PASSWORD && { password: REDIS_PASSWORD }),
  retryStrategy: (times) => {
    const delay = Math.min(times * 50, 2000);
    return delay;
  }
};

/**
 * Create scrape queue
 */
function createQueue() {
  const queue = new Queue('scrape-queue', {
    redis: redisConfig,
    defaultJobOptions: {
      removeOnComplete: {
        age: 3600, // Keep completed jobs for 1 hour
        count: 1000 // Keep max 1000 completed jobs
      },
      removeOnFail: {
        age: 24 * 3600 // Keep failed jobs for 24 hours
      }
    }
  });

  // Queue event handlers
  queue.on('completed', (job, result) => {
    logger.info(`Job ${job.id} completed: ${job.data.employee?.name || 'unknown'}`);
  });

  queue.on('failed', (job, err) => {
    logger.error(`Job ${job.id} failed:`, err);
  });

  queue.on('stalled', (job) => {
    logger.warn(`Job ${job.id} stalled`);
  });

  // Process jobs
  queue.process('scrape-employee', require('./workers/scrape-worker'));

  return queue;
}

module.exports = { createQueue };
