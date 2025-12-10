'use client'

import { useEffect, useState } from 'react'
import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

interface LicenseGap {
  'Firm.Name': string
  'Gap.Years': string | number
}

export function LicenseGapChart() {
  const [data, setData] = useState<LicenseGap[]>([])

  useEffect(() => {
    fetch('/api/data/license-gaps')
      .then(res => res.json())
      .then(result => {
        const gaps = result.license_gaps || []
        // Sort by gap years descending and take top 10
        const sorted = gaps
          .filter((g: LicenseGap) => typeof g['Gap.Years'] === 'number')
          .sort((a: LicenseGap, b: LicenseGap) =>
            (b['Gap.Years'] as number) - (a['Gap.Years'] as number)
          )
          .slice(0, 10)
        setData(sorted)
      })
      .catch(console.error)
  }, [])

  const getColor = (gap: number) => {
    if (gap >= 10) return '#ef4444' // red
    if (gap >= 5) return '#f59e0b' // amber
    return '#3b82f6' // blue
  }

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="Firm.Name"
          angle={-45}
          textAnchor="end"
          height={120}
          interval={0}
          tick={{ fontSize: 10 }}
        />
        <YAxis label={{ value: 'Years', angle: -90, position: 'insideLeft' }} />
        <Tooltip
          formatter={(value: number) => [`${value} years`, 'Gap']}
          labelStyle={{ fontWeight: 'bold' }}
        />
        <Bar dataKey="Gap.Years" name="Gap Years">
          {data.map((entry, index) => (
            <Cell
              key={`cell-${index}`}
              fill={getColor(entry['Gap.Years'] as number)}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
