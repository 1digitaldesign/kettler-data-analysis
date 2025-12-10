/**
 * Scheduler Service
 *
 * Schedules periodic license searches and maintenance tasks
 */

const express = require('express');
const cron = require('node-cron');
const axios = require('axios');
const { createQueue } = require('./queue');
const logger = require('./logger');

require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3004;

// Service URLs
const SCRAPER_SERVICE_URL = process.env.SCRAPER_SERVICE_URL || 'http://scraper-service:3001';
const PROCESSOR_SERVICE_URL = process.env.PROCESSOR_SERVICE_URL || 'http://data-processing-service:3002';

// Initialize queue
const schedulerQueue = createQueue();

// Express app for health checks
app.use(express.json());

app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'scheduler-service',
    timestamp: new Date().toISOString()
  });
});

// Schedule definitions
const schedules = [
  {
    name: 'daily-license-search',
    cron: '0 2 * * *', // 2 AM daily
    enabled: process.env.DAILY_SEARCH_ENABLED !== 'false',
    handler: async () => {
      logger.info('Running daily license search');
      await scheduleDailySearch();
    }
  },
  {
    name: 'weekly-consolidation',
    cron: '0 3 * * 0', // 3 AM every Sunday
    enabled: process.env.WEEKLY_CONSOLIDATION_ENABLED !== 'false',
    handler: async () => {
      logger.info('Running weekly consolidation');
      await scheduleWeeklyConsolidation();
    }
  },
  {
    name: 'monthly-report-generation',
    cron: '0 4 1 * *', // 4 AM on the 1st of every month
    enabled: process.env.MONTHLY_REPORTS_ENABLED !== 'false',
    handler: async () => {
      logger.info('Running monthly report generation');
      await scheduleMonthlyReports();
    }
  }
];

// Schedule handlers
async function scheduleDailySearch() {
  try {
    // Get all employees and states from config
    const employees = require('./config/employees.json');
    const states = require('./config/states.json');

    // Schedule searches for high-priority employees
    const highPriorityEmployees = employees.filter(emp => emp.priority === 'HIGH');

    for (const employee of highPriorityEmployees) {
      for (const state of states) {
        try {
          await axios.post(`${SCRAPER_SERVICE_URL}/api/v1/scrape/employee`, {
            employee,
            state: state.name
          });
          logger.info(`Scheduled search for ${employee.name} in ${state.name}`);
        } catch (error) {
          logger.error(`Error scheduling search for ${employee.name}: ${error.message}`);
        }
      }
    }
  } catch (error) {
    logger.error('Error in daily search scheduling:', error);
  }
}

async function scheduleWeeklyConsolidation() {
  try {
    await axios.post(`${PROCESSOR_SERVICE_URL}/api/v1/process/consolidate`, {
      output_format: 'csv'
    });
    logger.info('Weekly consolidation scheduled');
  } catch (error) {
    logger.error('Error scheduling weekly consolidation:', error);
  }
}

async function scheduleMonthlyReports() {
  try {
    const states = require('./config/states.json');
    const stateNames = states.map(s => s.name);

    await axios.post(`${PROCESSOR_SERVICE_URL}/api/v1/process/generate-letters`, {
      states: stateNames
    });
    logger.info('Monthly report generation scheduled');
  } catch (error) {
    logger.error('Error scheduling monthly reports:', error);
  }
}

// Initialize schedules
function initializeSchedules() {
  schedules.forEach(schedule => {
    if (schedule.enabled) {
      cron.schedule(schedule.cron, schedule.handler, {
        scheduled: true,
        timezone: process.env.TZ || 'America/New_York'
      });
      logger.info(`Schedule '${schedule.name}' initialized: ${schedule.cron}`);
    } else {
      logger.info(`Schedule '${schedule.name}' is disabled`);
    }
  });
}

// Start Express server
app.listen(PORT, () => {
  logger.info(`Scheduler service listening on port ${PORT}`);
  initializeSchedules();
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  logger.info('SIGTERM received, shutting down gracefully');
  await schedulerQueue.close();
  process.exit(0);
});

module.exports = app;
