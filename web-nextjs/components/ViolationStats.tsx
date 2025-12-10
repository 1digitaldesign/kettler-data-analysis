'use client'

import { AlertTriangle, Ban, FileWarning } from 'lucide-react'
import { useEffect, useState } from 'react'

export function ViolationStats() {
  const [stats, setStats] = useState({
    totalViolations: 0,
    unlicensedPractice: 0,
    criticalIssues: 0,
  })

  useEffect(() => {
    fetch('/api/data/violations')
      .then(res => res.json())
      .then(data => {
        const violations = data.violations || []
        setStats({
          totalViolations: violations.length,
          unlicensedPractice: violations.filter((v: any) =>
            v.type?.toLowerCase().includes('unlicensed') ||
            v.category?.toLowerCase().includes('unlicensed')
          ).length,
          criticalIssues: violations.filter((v: any) =>
            v.severity === 'critical' || v.priority === 'high'
          ).length,
        })
      })
      .catch(console.error)
  }, [])

  const statCards = [
    {
      name: 'Total Violations',
      value: stats.totalViolations,
      icon: FileWarning,
      color: 'text-red-600',
      bgColor: 'bg-red-100',
    },
    {
      name: 'Unlicensed Practice',
      value: stats.unlicensedPractice,
      icon: Ban,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100',
    },
    {
      name: 'Critical Issues',
      value: stats.criticalIssues,
      icon: AlertTriangle,
      color: 'text-red-700',
      bgColor: 'bg-red-200',
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
