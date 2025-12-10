/**
 * API Gateway - Express Server
 *
 * Routes requests to appropriate microservices
 * Provides service discovery, load balancing, and request aggregation
 */

const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const logger = require('./logger');

require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Service URLs (from environment or defaults)
const SERVICES = {
  scraper: process.env.SCRAPER_SERVICE_URL || 'http://scraper-service:3001',
  processor: process.env.PROCESSOR_SERVICE_URL || 'http://data-processing-service:3002',
  vector: process.env.VECTOR_SERVICE_URL || 'http://vector-service:3003',
  scheduler: process.env.SCHEDULER_SERVICE_URL || 'http://scheduler-service:3004'
};

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 200 // limit each IP to 200 requests per windowMs
});
app.use('/api/', limiter);

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'api-gateway',
    services: Object.keys(SERVICES),
    timestamp: new Date().toISOString()
  });
});

// Service health check endpoint
app.get('/health/services', async (req, res) => {
  const axios = require('axios');
  const serviceHealth = {};

  for (const [name, url] of Object.entries(SERVICES)) {
    try {
      const response = await axios.get(`${url}/health`, { timeout: 5000 });
      serviceHealth[name] = {
        status: 'healthy',
        response: response.data
      };
    } catch (error) {
      serviceHealth[name] = {
        status: 'unhealthy',
        error: error.message
      };
    }
  }

  res.json({
    gateway: 'healthy',
    services: serviceHealth,
    timestamp: new Date().toISOString()
  });
});

// Proxy middleware for scraper service
app.use('/api/v1/scrape', createProxyMiddleware({
  target: SERVICES.scraper,
  changeOrigin: true,
  pathRewrite: {
    '^/api/v1/scrape': '/api/v1/scrape'
  },
  onProxyReq: (proxyReq, req, res) => {
    logger.info(`Proxying ${req.method} ${req.path} to scraper-service`);
  },
  onError: (err, req, res) => {
    logger.error(`Proxy error for scraper-service: ${err.message}`);
    res.status(503).json({ error: 'Scraper service unavailable' });
  }
}));

// Proxy middleware for processor service
app.use('/api/v1/process', createProxyMiddleware({
  target: SERVICES.processor,
  changeOrigin: true,
  pathRewrite: {
    '^/api/v1/process': '/api/v1/process'
  },
  onProxyReq: (proxyReq, req, res) => {
    logger.info(`Proxying ${req.method} ${req.path} to processor-service`);
  },
  onError: (err, req, res) => {
    logger.error(`Proxy error for processor-service: ${err.message}`);
    res.status(503).json({ error: 'Processor service unavailable' });
  }
}));

// Proxy middleware for vector service
app.use('/api/v1/vectors', createProxyMiddleware({
  target: SERVICES.vector,
  changeOrigin: true,
  pathRewrite: {
    '^/api/v1/vectors': '/api/v1/vectors'
  },
  onProxyReq: (proxyReq, req, res) => {
    logger.info(`Proxying ${req.method} ${req.path} to vector-service`);
  },
  onError: (err, req, res) => {
    logger.error(`Proxy error for vector-service: ${err.message}`);
    res.status(503).json({ error: 'Vector service unavailable' });
  }
}));

// Proxy middleware for scheduler service
app.use('/api/v1/scheduler', createProxyMiddleware({
  target: SERVICES.scheduler,
  changeOrigin: true,
  pathRewrite: {
    '^/api/v1/scheduler': '/api/v1/scheduler'
  },
  onProxyReq: (proxyReq, req, res) => {
    logger.info(`Proxying ${req.method} ${req.path} to scheduler-service`);
  },
  onError: (err, req, res) => {
    logger.error(`Proxy error for scheduler-service: ${err.message}`);
    res.status(503).json({ error: 'Scheduler service unavailable' });
  }
}));

// Aggregated endpoints

/**
 * POST /api/v1/search/complete
 * Complete search workflow: scrape -> process -> store vectors
 */
app.post('/api/v1/search/complete', async (req, res) => {
  const axios = require('axios');
  const { employee, state } = req.body;

  try {
    logger.info(`Complete search workflow for ${employee?.name} in ${state}`);

    // Step 1: Scrape
    const scrapeResponse = await axios.post(`${SERVICES.scraper}/api/v1/scrape/employee`, {
      employee,
      state
    });

    const jobId = scrapeResponse.data.jobId;

    // Wait for job completion (simplified - in production use polling)
    // Step 2: Process results
    // Step 3: Store vectors

    res.json({
      status: 'initiated',
      jobId: jobId,
      message: 'Complete search workflow initiated'
    });

  } catch (error) {
    logger.error('Error in complete search workflow:', error);
    res.status(500).json({ error: error.message });
  }
});

// Start server
app.listen(PORT, () => {
  logger.info(`API Gateway listening on port ${PORT}`);
  logger.info('Service URLs:', SERVICES);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

module.exports = app;
