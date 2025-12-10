/**
 * Scraper Service - Express API Server
 *
 * Provides REST API endpoints for browser automation and license searches
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const { createQueue } = require('./queue');
const { scrapeEmployee, scrapeBatch } = require('./scraper');
const logger = require('./logger');

require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use('/api/', limiter);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'scraper-service', timestamp: new Date().toISOString() });
});

// Initialize queue
const scrapeQueue = createQueue();

// API Routes

/**
 * POST /api/v1/scrape/employee
 * Search for a single employee in a specific state
 */
app.post('/api/v1/scrape/employee', async (req, res) => {
  try {
    const { employee, state, options } = req.body;

    if (!employee || !state) {
      return res.status(400).json({
        error: 'Missing required fields: employee and state are required'
      });
    }

    logger.info(`Scraping employee: ${employee.name} in ${state}`);

    // Add job to queue
    const job = await scrapeQueue.add('scrape-employee', {
      employee,
      state,
      options: options || {}
    }, {
      attempts: 3,
      backoff: {
        type: 'exponential',
        delay: 2000
      }
    });

    res.json({
      jobId: job.id,
      status: 'queued',
      message: `Job queued for ${employee.name} in ${state}`
    });

  } catch (error) {
    logger.error('Error queuing scrape job:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * POST /api/v1/scrape/batch
 * Batch search for multiple employees
 */
app.post('/api/v1/scrape/batch', async (req, res) => {
  try {
    const { employees, state, options } = req.body;

    if (!employees || !Array.isArray(employees) || employees.length === 0) {
      return res.status(400).json({
        error: 'Missing required field: employees array is required'
      });
    }

    if (!state) {
      return res.status(400).json({
        error: 'Missing required field: state is required'
      });
    }

    logger.info(`Batch scraping ${employees.length} employees in ${state}`);

    const jobs = [];
    for (const employee of employees) {
      const job = await scrapeQueue.add('scrape-employee', {
        employee,
        state,
        options: options || {}
      }, {
        attempts: 3,
        backoff: {
          type: 'exponential',
          delay: 2000
        }
      });
      jobs.push(job.id);
    }

    res.json({
      jobIds: jobs,
      count: jobs.length,
      status: 'queued',
      message: `Batch job queued: ${jobs.length} employees in ${state}`
    });

  } catch (error) {
    logger.error('Error queuing batch scrape job:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/v1/scrape/status/:jobId
 * Get status of a scrape job
 */
app.get('/api/v1/scrape/status/:jobId', async (req, res) => {
  try {
    const { jobId } = req.params;
    const job = await scrapeQueue.getJob(jobId);

    if (!job) {
      return res.status(404).json({ error: 'Job not found' });
    }

    const state = await job.getState();
    const progress = job.progress();

    res.json({
      jobId: job.id,
      state,
      progress,
      data: job.returnvalue || null,
      failedReason: job.failedReason || null
    });

  } catch (error) {
    logger.error('Error getting job status:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/v1/scrape/jobs
 * List all jobs (with pagination)
 */
app.get('/api/v1/scrape/jobs', async (req, res) => {
  try {
    const { state = 'all', page = 1, limit = 50 } = req.query;

    const states = state === 'all'
      ? ['completed', 'active', 'waiting', 'failed', 'delayed']
      : [state];

    const jobs = [];
    for (const jobState of states) {
      const jobList = await scrapeQueue.getJobs([jobState], (page - 1) * limit, page * limit - 1);
      jobs.push(...jobList);
    }

    res.json({
      jobs: jobs.map(job => ({
        id: job.id,
        state: job.opts.state || 'unknown',
        data: job.data,
        progress: job.progress()
      })),
      page: parseInt(page),
      limit: parseInt(limit),
      total: jobs.length
    });

  } catch (error) {
    logger.error('Error listing jobs:', error);
    res.status(500).json({ error: error.message });
  }
});

// Start server
app.listen(PORT, () => {
  logger.info(`Scraper service listening on port ${PORT}`);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  logger.info('SIGTERM received, shutting down gracefully');
  await scrapeQueue.close();
  process.exit(0);
});

module.exports = app;
