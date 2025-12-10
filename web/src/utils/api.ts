/**
 * API utility functions for efficient data fetching
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export interface DashboardStats {
  totalFirms: number
  totalConnections: number
  violationsFound: number
  fraudIndicators: number
}

export interface SearchResult {
  id: string
  source: string
  text: string
  similarity?: number
  metadata: Record<string, any>
}

export interface AnalysisResult {
  status: 'success' | 'error' | 'running'
  data?: any
  message?: string
}

/**
 * Fetch dashboard statistics
 */
export async function getDashboardStats(): Promise<DashboardStats> {
  const response = await api.get('/api/dashboard/stats')
  return response.data
}

/**
 * Vector similarity search
 */
export async function vectorSearch(query: string, topK: number = 10): Promise<SearchResult[]> {
  const response = await api.post('/api/search/vector', { query, top_k: topK })
  return response.data.results || []
}

/**
 * DPOR database search
 */
export async function dporSearch(query: string, state: string = 'all'): Promise<SearchResult[]> {
  const response = await api.post('/api/search/dpor', { query, state })
  return response.data.results || []
}

/**
 * Get regulatory agencies
 */
export async function getRegulatoryAgencies(): Promise<any> {
  const response = await api.get('/api/search/regulatory')
  return response.data.agencies || []
}

/**
 * Run analysis
 */
export async function runAnalysis(analysisType: string): Promise<AnalysisResult> {
  const response = await api.post(`/api/analysis/${analysisType}`)
  return response.data
}

/**
 * Get visualization data
 */
export async function getVisualizationData(): Promise<{
  connections: Array<{ name: string; value: number }>
  violations: Array<{ name: string; value: number }>
}> {
  const response = await api.get('/api/visualization/data')
  return response.data
}

/**
 * Run web scraping
 */
export async function runScraping(platform: string, targets: string[]): Promise<any> {
  const response = await api.post('/api/scraping/scrape', {
    platform,
    targets,
  })
  return response.data
}

/**
 * Get available scraping platforms
 */
export async function getScrapingPlatforms(): Promise<any> {
  const response = await api.get('/api/scraping/platforms')
  return response.data
}

export default api
