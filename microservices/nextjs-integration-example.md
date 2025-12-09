# Next.js Integration with GCP Microservices

## Overview

This guide shows how to integrate Next.js/Vercel frontend with GCP microservices.

## API Client Setup

### Create API Client (`lib/api-client.ts`)

```typescript
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      throw new Error(error.response.data.detail || 'API Error');
    }
    throw error;
  }
);

export default apiClient;
```

## API Routes (Server-Side)

### Analysis API Route (`pages/api/analysis/fraud.ts`)

```typescript
import type { NextApiRequest, NextApiResponse } from 'next';
import apiClient from '../../../lib/api-client';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const result = await apiClient.post('/api/analysis/fraud', req.body);
    res.status(200).json(result);
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
}
```

### Scraping API Route (`pages/api/scraping/airbnb.ts`)

```typescript
import type { NextApiRequest, NextApiResponse } from 'next';
import apiClient from '../../../lib/api-client';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const result = await apiClient.post('/api/scraping/airbnb', req.body);
    res.status(200).json(result);
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
}
```

## React Hooks

### Use Analysis Hook (`hooks/useAnalysis.ts`)

```typescript
import { useState, useCallback } from 'react';
import apiClient from '../lib/api-client';

export function useAnalysis() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyzeFraud = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await apiClient.post('/api/analysis/fraud', {});
      return result;
    } catch (err: any) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const analyzeNexus = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await apiClient.post('/api/analysis/nexus', {});
      return result;
    } catch (err: any) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const analyzeAll = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await apiClient.post('/api/analysis/all', {});
      return result;
    } catch (err: any) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    error,
    analyzeFraud,
    analyzeNexus,
    analyzeAll,
  };
}
```

### Use Scraping Hook (`hooks/useScraping.ts`)

```typescript
import { useState, useCallback } from 'react';
import apiClient from '../lib/api-client';

export function useScraping() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const scrapeAirbnb = useCallback(async (targets: string[]) => {
    setLoading(true);
    setError(null);
    try {
      const result = await apiClient.post('/api/scraping/airbnb', {
        targets,
      });
      return result;
    } catch (err: any) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const scrapeACRIS = useCallback(async (searchType: string, params: any) => {
    setLoading(true);
    setError(null);
    try {
      const result = await apiClient.post('/api/scraping/acris', {
        search_type: searchType,
        params,
      });
      return result;
    } catch (err: any) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    error,
    scrapeAirbnb,
    scrapeACRIS,
  };
}
```

## React Components

### Analysis Component (`components/Analysis.tsx`)

```typescript
import { useState } from 'react';
import { useAnalysis } from '../hooks/useAnalysis';

export default function Analysis() {
  const { loading, error, analyzeFraud, analyzeNexus, analyzeAll } = useAnalysis();
  const [results, setResults] = useState<any>(null);

  const handleAnalyzeFraud = async () => {
    try {
      const result = await analyzeFraud();
      setResults(result);
    } catch (err) {
      console.error(err);
    }
  };

  const handleAnalyzeNexus = async () => {
    try {
      const result = await analyzeNexus();
      setResults(result);
    } catch (err) {
      console.error(err);
    }
  };

  const handleAnalyzeAll = async () => {
    try {
      const result = await analyzeAll();
      setResults(result);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Analysis</h2>
      <div>
        <button onClick={handleAnalyzeFraud} disabled={loading}>
          Analyze Fraud Patterns
        </button>
        <button onClick={handleAnalyzeNexus} disabled={loading}>
          Analyze Nexus Patterns
        </button>
        <button onClick={handleAnalyzeAll} disabled={loading}>
          Run All Analyses
        </button>
      </div>
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      {results && <pre>{JSON.stringify(results, null, 2)}</pre>}
    </div>
  );
}
```

## Environment Variables

### `.env.local` (Development)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Vercel Environment Variables

Set in Vercel dashboard:
- `NEXT_PUBLIC_API_URL` = `https://api-gateway-xxx.run.app`

## Server-Side Rendering (SSR)

### Get Server-Side Props (`pages/analysis.tsx`)

```typescript
import { GetServerSideProps } from 'next';
import apiClient from '../lib/api-client';

export const getServerSideProps: GetServerSideProps = async () => {
  try {
    const results = await apiClient.post('/api/analysis/all', {});
    return {
      props: {
        analysisResults: results,
      },
    };
  } catch (error) {
    return {
      props: {
        analysisResults: null,
        error: 'Failed to fetch analysis results',
      },
    };
  }
};

export default function AnalysisPage({ analysisResults, error }: any) {
  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h1>Analysis Results</h1>
      <pre>{JSON.stringify(analysisResults, null, 2)}</pre>
    </div>
  );
}
```

## API Route Proxy Pattern

### Proxy Route (`pages/api/proxy/[...path].ts`)

```typescript
import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { path } = req.query;
  const apiPath = Array.isArray(path) ? path.join('/') : path;

  try {
    const response = await axios({
      method: req.method,
      url: `${API_URL}/${apiPath}`,
      data: req.body,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    res.status(response.status).json(response.data);
  } catch (error: any) {
    res.status(error.response?.status || 500).json({
      error: error.response?.data || error.message,
    });
  }
}
```

Usage:
```typescript
// Client-side
const result = await fetch('/api/proxy/api/analysis/fraud', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({}),
});
```

## Error Handling

### Error Boundary (`components/ErrorBoundary.tsx`)

```typescript
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div>
          <h2>Something went wrong.</h2>
          <details>
            {this.state.error && this.state.error.toString()}
          </details>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## Best Practices

1. **Use API Routes for Server-Side**: Keep API keys and secrets on the server
2. **Error Handling**: Always handle errors gracefully
3. **Loading States**: Show loading indicators during API calls
4. **Caching**: Use Next.js caching for frequently accessed data
5. **Type Safety**: Use TypeScript for API responses
6. **Environment Variables**: Never expose API URLs in client-side code

## Deployment Checklist

- [ ] Set `NEXT_PUBLIC_API_URL` in Vercel environment variables
- [ ] Test API connectivity from Vercel deployment
- [ ] Configure CORS in API Gateway
- [ ] Set up error monitoring (Sentry, etc.)
- [ ] Configure rate limiting
- [ ] Set up authentication if needed
