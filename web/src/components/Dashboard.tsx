import axios from 'axios'
import { AlertTriangle, Database, FileText, Search, TrendingUp } from 'lucide-react'
import { useEffect, useState } from 'react'

interface DashboardStats {
  totalFirms: number
  totalConnections: number
  violationsFound: number
  fraudIndicators: number
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      // Try to load from API, fallback to local data
      const response = await axios.get('/api/dashboard/stats').catch(() => null)
      if (response?.data) {
        setStats(response.data)
      } else {
        // Fallback: load from local files
        const firmsResponse = await fetch('/data/source/skidmore_all_firms_complete.json')
        const firmsData = firmsResponse.ok ? await firmsResponse.json() : []
        setStats({
          totalFirms: Array.isArray(firmsData) ? firmsData.length : 0,
          totalConnections: 0,
          violationsFound: 0,
          fraudIndicators: 0
        })
      }
    } catch (error) {
      console.error('Error loading dashboard data:', error)
      setStats({
        totalFirms: 0,
        totalConnections: 0,
        violationsFound: 0,
        fraudIndicators: 0
      })
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    )
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-sm text-gray-600">
          Overview of Kettler Data Analysis findings and statistics
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Database className="h-6 w-6 text-gray-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Total Firms</dt>
                  <dd className="text-lg font-medium text-gray-900">{stats?.totalFirms || 0}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Search className="h-6 w-6 text-gray-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Connections Found</dt>
                  <dd className="text-lg font-medium text-gray-900">{stats?.totalConnections || 0}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <AlertTriangle className="h-6 w-6 text-red-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Violations</dt>
                  <dd className="text-lg font-medium text-gray-900">{stats?.violationsFound || 0}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TrendingUp className="h-6 w-6 text-yellow-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Fraud Indicators</dt>
                  <dd className="text-lg font-medium text-gray-900">{stats?.fraudIndicators || 0}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <button
            onClick={() => window.location.href = '/search'}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition-colors"
          >
            <Search className="inline-block mr-2 h-5 w-5" />
            Search Databases
          </button>
          <button
            onClick={() => window.location.href = '/analysis'}
            className="bg-green-500 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg transition-colors"
          >
            <FileText className="inline-block mr-2 h-5 w-5" />
            Run Analysis
          </button>
          <button
            onClick={() => window.location.href = '/visualization'}
            className="bg-purple-500 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-lg transition-colors"
          >
            <TrendingUp className="inline-block mr-2 h-5 w-5" />
            View Visualizations
          </button>
        </div>
      </div>
    </div>
  )
}
