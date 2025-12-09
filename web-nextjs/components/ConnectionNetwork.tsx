'use client'

import dynamic from 'next/dynamic'
import { useEffect, useState } from 'react'

// Dynamically import to avoid SSR issues
const ForceGraph2D = dynamic(() => import('react-force-graph-2d'), {
  ssr: false,
})

export function ConnectionNetwork() {
  const [graphData, setGraphData] = useState<{
    nodes: Array<{ id: string; name: string; group: number }>
    links: Array<{ source: string; target: string; value: number }>
  }>({ nodes: [], links: [] })

  useEffect(() => {
    fetch('/api/data/connections')
      .then(res => res.json())
      .then(data => {
        // Transform connection data into graph format
        const nodes = new Map<string, { id: string; name: string; group: number }>()
        const links: Array<{ source: string; target: string; value: number }> = []

        // Add nodes and links based on connection data
        // This is a simplified example - adjust based on your actual data structure
        if (data.firm_firm_connections) {
          Object.entries(data.firm_firm_connections).forEach(([firm1, connections]: [string, any]) => {
            if (!nodes.has(firm1)) {
              nodes.set(firm1, { id: firm1, name: firm1, group: 1 })
            }
            if (connections && typeof connections === 'object') {
              Object.keys(connections).forEach(firm2 => {
                if (!nodes.has(firm2)) {
                  nodes.set(firm2, { id: firm2, name: firm2, group: 1 })
                }
                links.push({ source: firm1, target: firm2, value: 1 })
              })
            }
          })
        }

        setGraphData({
          nodes: Array.from(nodes.values()),
          links,
        })
      })
      .catch(console.error)
  }, [])

  if (graphData.nodes.length === 0) {
    return (
      <div className="card">
        <p className="text-center text-gray-500 py-12">
          No connection data available. Loading connection matrix...
        </p>
      </div>
    )
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-semibold mb-4">Network Graph</h2>
      <div className="border rounded-lg overflow-hidden" style={{ height: '600px' }}>
        <ForceGraph2D
          graphData={graphData}
          nodeLabel={(node: any) => node.name}
          nodeColor={(node: any) => node.group === 1 ? '#3b82f6' : '#10b981'}
          linkColor={() => '#94a3b8'}
          nodeVal={(node: any) => 10}
        />
      </div>
    </div>
  )
}
