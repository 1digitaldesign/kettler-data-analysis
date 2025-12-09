'use client'

import { useEffect, useState } from 'react'
import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts'

interface StateData {
  state: string
  count: number
}

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']

export function StateDistributionChart() {
  const [data, setData] = useState<StateData[]>([])

  useEffect(() => {
    fetch('/api/data/firms')
      .then(res => res.json())
      .then(firms => {
        const stateCounts: Record<string, number> = {}
        firms.forEach((firm: { state: string }) => {
          stateCounts[firm.state] = (stateCounts[firm.state] || 0) + 1
        })
        const stateData = Object.entries(stateCounts).map(([state, count]) => ({
          state,
          count,
        }))
        setData(stateData)
      })
      .catch(console.error)
  }, [])

  return (
    <ResponsiveContainer width="100%" height={400}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ state, percent }) => `${state}: ${(percent * 100).toFixed(0)}%`}
          outerRadius={120}
          fill="#8884d8"
          dataKey="count"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  )
}
