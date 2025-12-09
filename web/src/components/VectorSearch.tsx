import axios from 'axios'
import { FileText, Search, Sparkles } from 'lucide-react'
import { useState } from 'react'

interface VectorResult {
  content_id: string
  distance: number
  similarity: number
  source: string
  text: string
  metadata: Record<string, any>
}

export default function VectorSearch() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<VectorResult[]>([])
  const [loading, setLoading] = useState(false)
  const [topK, setTopK] = useState(10)

  const handleSearch = async () => {
    if (!query.trim()) return

    setLoading(true)
    try {
      const response = await axios.post('/api/search/vector', {
        query,
        top_k: topK
      })
      setResults(response.data.results || [])
    } catch (error) {
      console.error('Vector search error:', error)
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="h-6 w-6 text-purple-500" />
        <h2 className="text-xl font-semibold text-gray-900">Vector Similarity Search</h2>
      </div>

      <p className="text-sm text-gray-600 mb-4">
        Search across all documents using semantic similarity. Finds related content even if exact keywords don't match.
      </p>

      <div className="flex gap-4 mb-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          placeholder="Enter your search query..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
        />
        <select
          value={topK}
          onChange={(e) => setTopK(Number(e.target.value))}
          className="px-4 py-2 border border-gray-300 rounded-lg"
        >
          <option value={5}>Top 5</option>
          <option value={10}>Top 10</option>
          <option value={20}>Top 20</option>
          <option value={50}>Top 50</option>
        </select>
        <button
          onClick={handleSearch}
          disabled={loading}
          className="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-6 rounded-lg transition-colors disabled:opacity-50 flex items-center"
        >
          <Search className="mr-2 h-5 w-5" />
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {results.length > 0 && (
        <div className="mt-6 space-y-4">
          <div className="text-sm text-gray-600">
            Found {results.length} results
          </div>
          {results.map((result, idx) => (
            <div key={result.content_id || idx} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-2">
                <div className="flex items-center gap-2">
                  <FileText className="h-4 w-4 text-gray-400" />
                  <span className="text-xs font-medium text-blue-600 bg-blue-100 px-2 py-1 rounded">
                    {result.source}
                  </span>
                </div>
                <div className="text-right">
                  <div className="text-sm font-semibold text-green-600">
                    {(result.similarity * 100).toFixed(1)}% match
                  </div>
                  <div className="text-xs text-gray-500">
                    Distance: {result.distance.toFixed(4)}
                  </div>
                </div>
              </div>
              <p className="text-sm text-gray-700 mb-2">{result.text}</p>
              {result.metadata && Object.keys(result.metadata).length > 0 && (
                <div className="mt-2 pt-2 border-t border-gray-100">
                  <div className="flex flex-wrap gap-2 text-xs">
                    {Object.entries(result.metadata).slice(0, 5).map(([key, value]) => (
                      <span key={key} className="text-gray-500">
                        <strong>{key}:</strong> {String(value).substring(0, 30)}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
