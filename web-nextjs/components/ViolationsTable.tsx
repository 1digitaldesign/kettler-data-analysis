'use client'

import { AlertTriangle, Calendar } from 'lucide-react'
import { useEffect, useState } from 'react'

interface Violation {
  id?: string
  type?: string
  category?: string
  entity?: string
  description?: string
  date?: string
  severity?: string
  evidence?: string
}

export function ViolationsTable() {
  const [violations, setViolations] = useState<Violation[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/data/violations')
      .then(res => res.json())
      .then(data => {
        const violationsList = data.violations || []
        setViolations(violationsList)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }, [])

  const getSeverityColor = (severity?: string) => {
    switch (severity?.toLowerCase()) {
      case 'critical':
      case 'high':
        return 'bg-red-100 text-red-800'
      case 'medium':
        return 'bg-amber-100 text-amber-800'
      case 'low':
        return 'bg-blue-100 text-blue-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return <div className="card text-center py-12">Loading violations...</div>
  }

  if (violations.length === 0) {
    return (
      <div className="card">
        <p className="text-center text-gray-500 py-12">
          No violation data available. Check data files.
        </p>
      </div>
    )
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-semibold mb-4">Violations List</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Type
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Entity
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Description
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Severity
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Date
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {violations.map((violation, index) => (
              <tr key={violation.id || index} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <AlertTriangle className="w-4 h-4 text-red-500 mr-2" />
                    <span className="text-sm font-medium text-gray-900">
                      {violation.type || violation.category || 'Unknown'}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {violation.entity || '—'}
                </td>
                <td className="px-6 py-4 text-sm text-gray-500">
                  {violation.description || '—'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {violation.severity && (
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getSeverityColor(violation.severity)}`}>
                      {violation.severity}
                    </span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {violation.date ? (
                    <div className="flex items-center">
                      <Calendar className="w-4 h-4 mr-1" />
                      {new Date(violation.date).toLocaleDateString()}
                    </div>
                  ) : (
                    '—'
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
