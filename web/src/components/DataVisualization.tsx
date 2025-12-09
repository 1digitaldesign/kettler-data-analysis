import axios from 'axios'
import { useEffect, useState } from 'react'
import { Bar, BarChart, CartesianGrid, Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

interface ChartData {
  name: string
  value: number
}

export default function DataVisualization() {
  const [connectionData, setConnectionData] = useState<ChartData[]>([])
  const [violationData, setViolationData] = useState<ChartData[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadVisualizationData()
  }, [])

  const loadVisualizationData = async () => {
    try {
      // Try to load from API
      const response = await axios.get('/api/visualization/data').catch(() => null)
      if (response?.data) {
        setConnectionData(response.data.connections || [])
        setViolationData(response.data.violations || [])
      } else {
        // Mock data for demonstration
        setConnectionData([
          { name: 'Principal Broker', value: 15 },
          { name: 'Same Address', value: 8 },
          { name: 'Known Firm Match', value: 5 }
        ])
        setViolationData([
          { name: 'License Gaps', value: 12 },
          { name: 'Address Clusters', value: 7 },
          { name: 'Timeline Issues', value: 4 }
        ])
      }
    } catch (error) {
      console.error('Error loading visualization data:', error)
    } finally {
      setLoading(false)
    }
  }

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']

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
        <h1 className="text-3xl font-bold text-gray-900">Data Visualization</h1>
        <p className="mt-2 text-sm text-gray-600">
          Visual representations of analysis results
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Connection Types Chart */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Connection Types</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={connectionData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Violations Chart */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Violation Types</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={violationData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {violationData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
