'use client'

import { format, parseISO } from 'date-fns'
import { useEffect, useState } from 'react'
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

interface TimelineEvent {
  date: string
  event_type: string
  entity: string
  details: string
}

export function TimelineChart() {
  const [timelineData, setTimelineData] = useState<TimelineEvent[]>([])

  useEffect(() => {
    fetch('/api/data/timeline')
      .then(res => res.json())
      .then(data => {
        const events = data.timeline || []
        // Group by date and count events
        const dateCounts: Record<string, number> = {}
        events.forEach((event: TimelineEvent) => {
          const date = event.date.split('T')[0] // Get date part only
          dateCounts[date] = (dateCounts[date] || 0) + 1
        })

        const chartData = Object.entries(dateCounts)
          .map(([date, count]) => ({
            date: format(parseISO(date), 'yyyy-MM-dd'),
            count,
            displayDate: format(parseISO(date), 'MMM yyyy'),
          }))
          .sort((a, b) => a.date.localeCompare(b.date))

        setTimelineData(chartData as any)
      })
      .catch(console.error)
  }, [])

  return (
    <div className="card">
      <h2 className="text-2xl font-semibold mb-4">License Issuance Timeline</h2>
      <ResponsiveContainer width="100%" height={500}>
        <LineChart data={timelineData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="displayDate"
            angle={-45}
            textAnchor="end"
            height={100}
            interval={0}
            tick={{ fontSize: 10 }}
          />
          <YAxis label={{ value: 'Events', angle: -90, position: 'insideLeft' }} />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="count"
            stroke="#3b82f6"
            strokeWidth={2}
            name="License Events"
            dot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
