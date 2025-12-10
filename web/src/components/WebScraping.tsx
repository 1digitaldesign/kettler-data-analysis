import axios from 'axios'
import { AlertCircle, CheckCircle, Download, Globe, Loader, Play } from 'lucide-react'
import { useState } from 'react'

interface ScrapingJob {
  id: string
  platform: string
  target: string
  status: 'pending' | 'running' | 'completed' | 'error'
  results?: any
  error?: string
  startedAt?: Date
  completedAt?: Date
}

export default function WebScraping() {
  const [platform, setPlatform] = useState<'airbnb' | 'vrbo' | 'front' | 'multi'>('airbnb')
  const [targets, setTargets] = useState<string>('')
  const [jobs, setJobs] = useState<ScrapingJob[]>([])
  const [loading, setLoading] = useState(false)

  const platforms = [
    { id: 'airbnb', name: 'Airbnb', description: 'Scrape Airbnb listings' },
    { id: 'vrbo', name: 'VRBO', description: 'Scrape VRBO listings' },
    { id: 'front', name: 'Front Websites', description: 'Scrape front company websites' },
    { id: 'multi', name: 'Multi-Platform', description: 'Scrape across multiple platforms' },
    { id: 'acris', name: 'ACRIS (NYC)', description: 'Search NYC property records' },
  ]

  const handleScrape = async () => {
    if (!targets.trim()) {
      alert('Please enter at least one target (address or URL)')
      return
    }

    const targetList = targets.split('\n').filter(t => t.trim())
    if (targetList.length === 0) {
      alert('Please enter at least one valid target')
      return
    }

    setLoading(true)
    const jobId = `job_${Date.now()}`
    const newJob: ScrapingJob = {
      id: jobId,
      platform,
      target: targetList.join(', '),
      status: 'running',
      startedAt: new Date(),
    }
    setJobs(prev => [newJob, ...prev])

    try {
      const response = await axios.post('/api/scraping/scrape', {
        platform,
        targets: targetList,
      })

      setJobs(prev => prev.map(job =>
        job.id === jobId
          ? {
              ...job,
              status: 'completed',
              results: response.data,
              completedAt: new Date(),
            }
          : job
      ))
    } catch (error: any) {
      setJobs(prev => prev.map(job =>
        job.id === jobId
          ? {
              ...job,
              status: 'error',
              error: error.response?.data?.detail || error.message || 'Scraping failed',
              completedAt: new Date(),
            }
          : job
      ))
    } finally {
      setLoading(false)
    }
  }

  const exportResults = (job: ScrapingJob) => {
    if (!job.results) return

    const dataStr = JSON.stringify(job.results, null, 2)
    const blob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `scraping_${job.platform}_${job.id}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <Globe className="h-8 w-8 text-blue-500" />
          <h1 className="text-3xl font-bold text-gray-900">Web Scraping</h1>
        </div>
        <p className="text-sm text-gray-600">
          Scrape data from various platforms including Airbnb, VRBO, and company websites
        </p>
      </div>

      {/* Configuration Panel */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Scraping Configuration</h2>

        {/* Platform Selection */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Platform
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {platforms.map((p) => (
              <button
                key={p.id}
                onClick={() => setPlatform(p.id as any)}
                className={`p-4 border-2 rounded-lg text-left transition-all ${
                  platform === p.id
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="font-semibold text-gray-900">{p.name}</div>
                <div className="text-xs text-gray-600 mt-1">{p.description}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Target Input */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Targets (one per line - addresses or URLs)
          </label>
          <textarea
            value={targets}
            onChange={(e) => setTargets(e.target.value)}
            placeholder="800 John Carlyle Street, Alexandria, VA&#10;https://www.example.com"
            rows={6}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
          />
          <p className="mt-2 text-xs text-gray-500">
            Enter addresses for Airbnb/VRBO searches, or URLs for website scraping
          </p>
        </div>

        {/* Scrape Button */}
        <button
          onClick={handleScrape}
          disabled={loading || !targets.trim()}
          className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
        >
          {loading ? (
            <>
              <Loader className="animate-spin mr-2 h-5 w-5" />
              Scraping...
            </>
          ) : (
            <>
              <Play className="mr-2 h-5 w-5" />
              Start Scraping
            </>
          )}
        </button>
      </div>

      {/* Results */}
      {jobs.length > 0 && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">
              Scraping Jobs ({jobs.length})
            </h2>
          </div>
          <div className="divide-y divide-gray-200">
            {jobs.map((job) => (
              <div key={job.id} className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-xs font-medium text-blue-600 bg-blue-100 px-2 py-1 rounded">
                        {job.platform.toUpperCase()}
                      </span>
                      {job.status === 'running' && (
                        <Loader className="animate-spin h-4 w-4 text-blue-500" />
                      )}
                      {job.status === 'completed' && (
                        <CheckCircle className="h-4 w-4 text-green-500" />
                      )}
                      {job.status === 'error' && (
                        <AlertCircle className="h-4 w-4 text-red-500" />
                      )}
                      <span className={`text-sm font-medium ${
                        job.status === 'completed' ? 'text-green-700' :
                        job.status === 'error' ? 'text-red-700' :
                        job.status === 'running' ? 'text-blue-700' :
                        'text-gray-700'
                      }`}>
                        {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-1">
                      <strong>Target:</strong> {job.target}
                    </p>
                    {job.startedAt && (
                      <p className="text-xs text-gray-500">
                        Started: {job.startedAt.toLocaleString()}
                        {job.completedAt && ` • Completed: ${job.completedAt.toLocaleString()}`}
                      </p>
                    )}
                  </div>
                  {job.status === 'completed' && job.results && (
                    <button
                      onClick={() => exportResults(job)}
                      className="flex items-center gap-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-700 transition-colors"
                    >
                      <Download className="h-4 w-4" />
                      Export
                    </button>
                  )}
                </div>

                {/* Results Display */}
                {job.status === 'completed' && job.results && (
                  <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                    <h3 className="text-sm font-semibold text-gray-900 mb-2">Results</h3>
                    {job.results.listings && (
                      <div className="text-sm text-gray-700">
                        <strong>{job.results.listings.length}</strong> listings found
                      </div>
                    )}
                    {job.results.scraped_data && (
                      <div className="text-sm text-gray-700">
                        <strong>{job.results.scraped_data.length}</strong> items scraped
                      </div>
                    )}
                    {job.results.platform && (
                      <div className="text-sm text-gray-700 mt-2">
                        Platform: <strong>{job.results.platform}</strong>
                      </div>
                    )}
                    {job.results.listings && job.results.listings.length > 0 && (
                      <div className="mt-4 max-h-64 overflow-y-auto">
                        {job.results.listings.slice(0, 5).map((listing: any, idx: number) => (
                          <div key={idx} className="mb-2 p-2 bg-white rounded border border-gray-200">
                            <div className="text-xs font-medium text-gray-900">
                              {listing.title || listing.address || `Listing ${idx + 1}`}
                            </div>
                            {listing.price && (
                              <div className="text-xs text-gray-600">Price: {listing.price}</div>
                            )}
                          </div>
                        ))}
                        {job.results.listings.length > 5 && (
                          <div className="text-xs text-gray-500 mt-2">
                            ... and {job.results.listings.length - 5} more
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}

                {/* Error Display */}
                {job.status === 'error' && job.error && (
                  <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <p className="text-sm text-red-700">
                      <strong>Error:</strong> {job.error}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {jobs.length === 0 && (
        <div className="bg-white shadow rounded-lg p-12 text-center">
          <Globe className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">
            Configure your scraping parameters above and click "Start Scraping" to begin
          </p>
        </div>
      )}
    </div>
  )
}
