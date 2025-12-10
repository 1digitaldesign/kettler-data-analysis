'use client'

import { AlertCircle, Building2, Calendar, MapPin } from 'lucide-react'
import { useEffect, useState } from 'react'

interface Firm {
  firm_name: string
  firm_license: string
  state: string
  address: string
  initial_cert_date: string | null
  expiration_date: string
  gap_years: number | null
  firm_type: string
}

export function FirmsTable() {
  const [firms, setFirms] = useState<Firm[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [stateFilter, setStateFilter] = useState<string>('all')

  useEffect(() => {
    fetch('/api/data/firms')
      .then(res => res.json())
      .then(data => {
        setFirms(data)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }, [])

  const filteredFirms = firms.filter(firm => {
    const matchesSearch = firm.firm_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         firm.firm_license.includes(searchTerm) ||
                         firm.address.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesState = stateFilter === 'all' || firm.state === stateFilter
    return matchesSearch && matchesState
  })

  const states = Array.from(new Set(firms.map(f => f.state))).sort()

  if (loading) {
    return <div className="card text-center py-12">Loading firms...</div>
  }

  return (
    <div className="card">
      <div className="mb-4 flex flex-col sm:flex-row gap-4">
        <input
          type="text"
          placeholder="Search firms, licenses, or addresses..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
        <select
          value={stateFilter}
          onChange={(e) => setStateFilter(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500"
        >
          <option value="all">All States</option>
          {states.map(state => (
            <option key={state} value={state}>{state}</option>
          ))}
        </select>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Firm Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                License
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                State
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Type
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Gap Years
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Expiration
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredFirms.map((firm) => (
              <tr key={firm.firm_license} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <Building2 className="w-4 h-4 text-gray-400 mr-2" />
                    <div>
                      <div className="text-sm font-medium text-gray-900">{firm.firm_name}</div>
                      <div className="text-xs text-gray-500 flex items-center mt-1">
                        <MapPin className="w-3 h-3 mr-1" />
                        {firm.address}
                      </div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {firm.firm_license}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                    {firm.state}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {firm.firm_type}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {firm.gap_years !== null && firm.gap_years > 0 ? (
                    <span className="flex items-center text-sm text-red-600">
                      <AlertCircle className="w-4 h-4 mr-1" />
                      {firm.gap_years} years
                    </span>
                  ) : (
                    <span className="text-sm text-gray-400">—</span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <div className="flex items-center">
                    <Calendar className="w-4 h-4 mr-1" />
                    {new Date(firm.expiration_date).toLocaleDateString()}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-4 text-sm text-gray-500">
        Showing {filteredFirms.length} of {firms.length} firms
      </div>
    </div>
  )
}
