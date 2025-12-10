/**
 * Redis Queue Configuration for Scheduler
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

function createQueue() {
  const queue = new Queue('scheduler-queue', {
    redis: redisConfig
  });

  queue.on('completed', (job) => {
    logger.info(`Scheduled job ${job.id} completed`);
  });

  queue.on('failed', (job, err) => {
    logger.error(`Scheduled job ${job.id} failed:`, err);
  });

  return queue;
}

module.exports = { createQueue };
