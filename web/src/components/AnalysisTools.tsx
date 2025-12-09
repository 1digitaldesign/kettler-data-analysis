import axios from 'axios'
import { AlertCircle, CheckCircle, Play } from 'lucide-react'
import { useState } from 'react'

interface AnalysisResult {
  type: string
  status: 'success' | 'error' | 'running'
  message: string
  data?: any
}

export default function AnalysisTools() {
  const [running, setRunning] = useState(false)
  const [results, setResults] = useState<AnalysisResult[]>([])

  const runAnalysis = async (analysisType: string) => {
    setRunning(true)
    const newResult: AnalysisResult = {
      type: analysisType,
      status: 'running',
      message: 'Running analysis...'
    }
    setResults(prev => [...prev, newResult])

    try {
      const response = await axios.post(`/api/analysis/${analysisType}`)
      setResults(prev => prev.map(r =>
        r.type === analysisType
          ? { ...r, status: 'success', message: 'Analysis complete', data: response.data }
          : r
      ))
    } catch (error: any) {
      setResults(prev => prev.map(r =>
        r.type === analysisType
          ? { ...r, status: 'error', message: error.message || 'Analysis failed' }
          : r
      ))
    } finally {
      setRunning(false)
    }
  }

  const analyses = [
    { id: 'fraud', name: 'Fraud Pattern Analysis', description: 'Identify fraud indicators and patterns' },
    { id: 'nexus', name: 'Nexus Pattern Analysis', description: 'Analyze connection patterns and control structures' },
    { id: 'timeline', name: 'Timeline Analysis', description: 'Create timeline of events and anomalies' },
    { id: 'anomalies', name: 'Anomaly Consolidation', description: 'Consolidate all identified anomalies' },
    { id: 'violations', name: 'Violation Compilation', description: 'Compile all violations found' },
  ]

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Analysis Tools</h1>
        <p className="mt-2 text-sm text-gray-600">
          Run comprehensive analyses on the data
        </p>
      </div>

      {/* Analysis Cards */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {analyses.map((analysis) => {
          const result = results.find(r => r.type === analysis.id)
          const isRunning = running && result?.status === 'running'

          return (
            <div key={analysis.id} className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{analysis.name}</h3>
              <p className="text-sm text-gray-600 mb-4">{analysis.description}</p>

              <button
                onClick={() => runAnalysis(analysis.id)}
                disabled={isRunning}
                className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition-colors disabled:opacity-50 flex items-center justify-center"
              >
                {isRunning ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Running...
                  </>
                ) : (
                  <>
                    <Play className="mr-2 h-4 w-4" />
                    Run Analysis
                  </>
                )}
              </button>

              {result && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="flex items-center gap-2">
                    {result.status === 'success' ? (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    ) : result.status === 'error' ? (
                      <AlertCircle className="h-5 w-5 text-red-500" />
                    ) : null}
                    <span className={`text-sm ${
                      result.status === 'success' ? 'text-green-700' :
                      result.status === 'error' ? 'text-red-700' :
                      'text-gray-700'
                    }`}>
                      {result.message}
                    </span>
                  </div>
                  {result.data && (
                    <div className="mt-2 text-xs text-gray-500">
                      {JSON.stringify(result.data).substring(0, 100)}...
                    </div>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Run All Button */}
      <div className="mt-8 text-center">
        <button
          onClick={() => {
            analyses.forEach(a => runAnalysis(a.id))
          }}
          disabled={running}
          className="bg-green-500 hover:bg-green-700 text-white font-bold py-3 px-8 rounded-lg transition-colors disabled:opacity-50"
        >
          Run All Analyses
        </button>
      </div>
    </div>
  )
}
