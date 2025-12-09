'use client'

import { Link as LinkIcon, Network, Users } from 'lucide-react'
import { useEffect, useState } from 'react'

export function ConnectionStats() {
  const [stats, setStats] = useState({
    totalConnections: 0,
    firmClusters: 0,
    hylandConnections: 0,
  })

  useEffect(() => {
    fetch('/api/data/connections')
      .then(res => res.json())
      .then(data => {
        setStats({
          totalConnections: data.summary?.total_firms || 0,
          firmClusters: data.summary?.firm_firm_clusters || 0,
          hylandConnections: data.summary?.hyland_connections || 0,
        })
      })
      .catch(console.error)
  }, [])

  const statCards = [
    {
      name: 'Total Firms',
      value: stats.totalConnections,
      icon: Network,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      name: 'Firm Clusters',
      value: stats.firmClusters,
      icon: Users,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      name: 'Hyland Connections',
      value: stats.hylandConnections,
      icon: LinkIcon,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {statCards.map((stat) => {
        const Icon = stat.icon
        return (
          <div key={stat.name} className="stat-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
              </div>
              <div className={`${stat.bgColor} p-3 rounded-full`}>
                <Icon className={`w-6 h-6 ${stat.color}`} />
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
