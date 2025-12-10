import { Minus, TrendingDown, TrendingUp } from 'lucide-react'
import { useEffect, useState } from 'react'
import { DashboardStats, getDashboardStats } from '../utils/api'

export default function QuickStats() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [previousStats, setPreviousStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
    const interval = setInterval(loadStats, 30000) // Refresh every 30s
    return () => clearInterval(interval)
  }, [])

  const loadStats = async () => {
    try {
      const newStats = await getDashboardStats()
      if (stats) {
        setPreviousStats(stats)
      }
      setStats(newStats)
    } catch (error) {
      console.error('Error loading stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const getTrend = (current: number, previous: number | null) => {
    if (previous === null) return null
    if (current > previous) return 'up'
    if (current < previous) return 'down'
    return 'same'
  }

  const TrendIcon = ({ trend }: { trend: 'up' | 'down' | 'same' | null }) => {
    if (trend === null) return null
    if (trend === 'up') return <TrendingUp className="h-4 w-4 text-green-500" />
    if (trend === 'down') return <TrendingDown className="h-4 w-4 text-red-500" />
    return <Minus className="h-4 w-4 text-gray-400" />
  }

  if (loading || !stats) {
    return (
      <div className="animate-pulse">
        <div className="h-24 bg-gray-200 rounded"></div>
      </div>
    )
  }

  const firmsTrend = getTrend(stats.totalFirms, previousStats?.totalFirms)
  const connectionsTrend = getTrend(stats.totalConnections, previousStats?.totalConnections)
  const violationsTrend = getTrend(stats.violationsFound, previousStats?.violationsFound)
  const fraudTrend = getTrend(stats.fraudIndicators, previousStats?.fraudIndicators)

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600">Total Firms</p>
            <p className="text-2xl font-bold">{stats.totalFirms}</p>
          </div>
          <TrendIcon trend={firmsTrend} />
        </div>
      </div>
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600">Connections</p>
            <p className="text-2xl font-bold">{stats.totalConnections}</p>
          </div>
          <TrendIcon trend={connectionsTrend} />
        </div>
      </div>
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600">Violations</p>
            <p className="text-2xl font-bold text-red-600">{stats.violationsFound}</p>
          </div>
          <TrendIcon trend={violationsTrend} />
        </div>
      </div>
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600">Fraud Indicators</p>
            <p className="text-2xl font-bold text-yellow-600">{stats.fraudIndicators}</p>
          </div>
          <TrendIcon trend={fraudTrend} />
        </div>
      </div>
    </div>
  )
}
