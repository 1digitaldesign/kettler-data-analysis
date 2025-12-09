import axios from 'axios'
import { AlertCircle, Building2, CheckCircle, Download, Loader, Search } from 'lucide-react'
import { useState } from 'react'

interface ACRISSearchJob {
  id: string
  searchType: string
  params: Record<string, any>
  status: 'pending' | 'running' | 'completed' | 'error'
  results?: any
  error?: string
  startedAt?: Date
  completedAt?: Date
}

export default function ACRISSearch() {
  const [searchType, setSearchType] = useState<'block_lot' | 'address' | 'party_name' | 'document_id'>('block_lot')
  const [borough, setBorough] = useState('')
  const [block, setBlock] = useState('')
  const [lot, setLot] = useState('')
  const [address, setAddress] = useState('')
  const [partyName, setPartyName] = useState('')
  const [documentId, setDocumentId] = useState('')
  const [jobs, setJobs] = useState<ACRISSearchJob[]>([])
  const [loading, setLoading] = useState(false)

  const boroughs = [
    { value: '1', label: 'Manhattan' },
    { value: '2', label: 'Bronx' },
    { value: '3', label: 'Brooklyn' },
    { value: '4', label: 'Queens' },
    { value: '5', label: 'Staten Island' },
  ]

  const handleSearch = async () => {
    setLoading(true)
    const jobId = `acris_${Date.now()}`

    const params: Record<string, any> = {
      search_type: searchType,
    }

    if (searchType === 'block_lot') {
      if (!borough || !block || !lot) {
        alert('Please fill in Borough, Block, and Lot')
        setLoading(false)
        return
      }
      params.borough = borough
      params.block = block
      params.lot = lot
    } else if (searchType === 'address') {
      if (!address) {
        alert('Please enter an address')
        setLoading(false)
        return
      }
      params.address = address
      if (borough) params.borough = borough
    } else if (searchType === 'party_name') {
      if (!partyName) {
        alert('Please enter a party name')
        setLoading(false)
        return
      }
      params.party_name = partyName
    } else if (searchType === 'document_id') {
      if (!documentId) {
        alert('Please enter a document ID')
        setLoading(false)
        return
      }
      params.document_id = documentId
    }

    const newJob: ACRISSearchJob = {
      id: jobId,
      searchType,
      params,
      status: 'running',
      startedAt: new Date(),
    }
    setJobs(prev => [newJob, ...prev])

    try {
      const response = await axios.post('/api/scraping/acris', params)

      setJobs(prev => prev.map(job =>
        job.id === jobId
          ? {
              ...job,
              status: 'completed',
              results: response.data.data,
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
              error: error.response?.data?.detail || error.message || 'Search failed',
              completedAt: new Date(),
            }
          : job
      ))
    } finally {
      setLoading(false)
    }
  }

  const exportResults = (job: ACRISSearchJob) => {
    if (!job.results) return

    const dataStr = JSON.stringify(job.results, null, 2)
    const blob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `acris_${job.searchType}_${job.id}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <Building2 className="h-8 w-8 text-blue-500" />
          <h1 className="text-3xl font-bold text-gray-900">ACRIS Property Records Search</h1>
        </div>
        <p className="text-sm text-gray-600">
          Search NYC property records from the Automated City Register Information System
        </p>
      </div>

      {/* Search Configuration */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Search Configuration</h2>

        {/* Search Type Selection */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Search Type
          </label>
          <select
            value={searchType}
            onChange={(e) => setSearchType(e.target.value as any)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="block_lot">Block & Lot</option>
            <option value="address">Address</option>
            <option value="party_name">Party Name (Grantor/Grantee)</option>
            <option value="document_id">Document ID</option>
          </select>
        </div>

        {/* Block & Lot Search */}
        {searchType === 'block_lot' && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Borough</label>
              <select
                value={borough}
                onChange={(e) => setBorough(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              >
                <option value="">Select Borough</option>
                {boroughs.map(b => (
                  <option key={b.value} value={b.value}>{b.label}</option>
                ))}
              </select>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Block</label>
                <input
                  type="text"
                  value={block}
                  onChange={(e) => setBlock(e.target.value)}
                  placeholder="Block number"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Lot</label>
                <input
                  type="text"
                  value={lot}
                  onChange={(e) => setLot(e.target.value)}
                  placeholder="Lot number"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
            </div>
          </div>
        )}

        {/* Address Search */}
        {searchType === 'address' && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Address</label>
              <input
                type="text"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                placeholder="123 Main Street"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Borough (Optional)</label>
              <select
                value={borough}
                onChange={(e) => setBorough(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              >
                <option value="">All Boroughs</option>
                {boroughs.map(b => (
                  <option key={b.value} value={b.value}>{b.label}</option>
                ))}
              </select>
            </div>
          </div>
        )}

        {/* Party Name Search */}
        {searchType === 'party_name' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Party Name</label>
            <input
              type="text"
              value={partyName}
              onChange={(e) => setPartyName(e.target.value)}
              placeholder="Enter grantor or grantee name"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
        )}

        {/* Document ID Search */}
        {searchType === 'document_id' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Document ID</label>
            <input
              type="text"
              value={documentId}
              onChange={(e) => setDocumentId(e.target.value)}
              placeholder="ACRIS document ID"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
        )}

        {/* Search Button */}
        <button
          onClick={handleSearch}
          disabled={loading}
          className="mt-6 w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
        >
          {loading ? (
            <>
              <Loader className="animate-spin mr-2 h-5 w-5" />
              Searching...
            </>
          ) : (
            <>
              <Search className="mr-2 h-5 w-5" />
              Search ACRIS
            </>
          )}
        </button>
      </div>

      {/* Results */}
      {jobs.length > 0 && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">
              Search Results ({jobs.length})
            </h2>
          </div>
          <div className="divide-y divide-gray-200">
            {jobs.map((job) => (
              <div key={job.id} className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-xs font-medium text-blue-600 bg-blue-100 px-2 py-1 rounded">
                        {job.searchType.toUpperCase()}
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
                    <div className="text-sm text-gray-600 space-y-1">
                      {Object.entries(job.params).map(([key, value]) => (
                        <div key={key}>
                          <strong>{key.replace('_', ' ')}:</strong> {String(value)}
                        </div>
                      ))}
                    </div>
                    {job.startedAt && (
                      <p className="text-xs text-gray-500 mt-2">
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
                    {job.results.results && (
                      <div className="text-sm text-gray-700">
                        <strong>{job.results.count || job.results.results.length}</strong> records found
                      </div>
                    )}
                    {job.results.results && job.results.results.length > 0 && (
                      <div className="mt-4 max-h-64 overflow-y-auto">
                        {job.results.results.slice(0, 5).map((result: any, idx: number) => (
                          <div key={idx} className="mb-2 p-2 bg-white rounded border border-gray-200">
                            <div className="text-xs font-medium text-gray-900">
                              Record {idx + 1}
                            </div>
                            <div className="text-xs text-gray-600 mt-1">
                              {JSON.stringify(result).substring(0, 200)}...
                            </div>
                          </div>
                        ))}
                        {job.results.results.length > 5 && (
                          <div className="text-xs text-gray-500 mt-2">
                            ... and {job.results.results.length - 5} more records
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
    </div>
  )
}
