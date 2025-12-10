import axios from 'axios'
import { Download, Search } from 'lucide-react'
import { useState } from 'react'

interface SearchResult {
  id: string
  source: string
  text: string
  similarity: number
  metadata: Record<string, any>
}

export default function SearchInterface() {
  const [query, setQuery] = useState('')
  const [searchType, setSearchType] = useState<'vector' | 'dpor' | 'regulatory'>('vector')
  const [results, setResults] = useState<SearchResult[]>([])
  const [loading, setLoading] = useState(false)

  const handleSearch = async () => {
    if (!query.trim()) return

    setLoading(true)
    try {
      if (searchType === 'vector') {
        // Vector similarity search
        const response = await axios.post('/api/search/vector', { query, top_k: 10 })
        setResults(response.data.results || [])
      } else if (searchType === 'dpor') {
        // DPOR database search
        const response = await axios.post('/api/search/dpor', { query, state: 'all' })
        setResults(response.data.results || [])
      } else {
        // Regulatory agency search
        const response = await axios.get('/api/search/regulatory')
        setResults(response.data.agencies || [])
      }
    } catch (error) {
      console.error('Search error:', error)
      // Fallback: show mock results
      setResults([{
        id: '1',
        source: 'mock',
        text: 'Mock result for: ' + query,
        similarity: 0.85,
        metadata: {}
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Search Interface</h1>
        <p className="mt-2 text-sm text-gray-600">
          Search across all data sources using vector similarity or database queries
        </p>
      </div>

      {/* Search Bar */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <div className="flex gap-4">
          <div className="flex-1">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="Enter search query..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <select
            value={searchType}
            onChange={(e) => setSearchType(e.target.value as any)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="vector">Vector Search</option>
            <option value="dpor">DPOR Database</option>
            <option value="regulatory">Regulatory Agencies</option>
          </select>
          <button
            onClick={handleSearch}
            disabled={loading}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition-colors disabled:opacity-50 flex items-center"
          >
            <Search className="mr-2 h-5 w-5" />
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </div>

      {/* Results */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h2 className="text-lg font-semibold text-gray-900">
            Results ({results.length})
          </h2>
          {results.length > 0 && (
            <button className="text-sm text-blue-600 hover:text-blue-800 flex items-center">
              <Download className="mr-1 h-4 w-4" />
              Export
            </button>
          )}
        </div>
        <div className="divide-y divide-gray-200">
          {results.length === 0 ? (
            <div className="px-6 py-12 text-center text-gray-500">
              {loading ? 'Searching...' : 'Enter a query and click Search to find results'}
            </div>
          ) : (
            results.map((result, idx) => (
              <div key={result.id || idx} className="px-6 py-4 hover:bg-gray-50">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xs font-medium text-blue-600 bg-blue-100 px-2 py-1 rounded">
                        {result.source}
                      </span>
                      {result.similarity && (
                        <span className="text-xs text-gray-500">
                          Similarity: {(result.similarity * 100).toFixed(1)}%
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-700">{result.text}</p>
                    {result.metadata && Object.keys(result.metadata).length > 0 && (
                      <div className="mt-2 text-xs text-gray-500">
                        {Object.entries(result.metadata).slice(0, 3).map(([key, value]) => (
                          <span key={key} className="mr-4">
                            <strong>{key}:</strong> {String(value)}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
