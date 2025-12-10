import { AlertTriangle, Info } from 'lucide-react'

export async function RecentFindings() {
  // This would fetch from research summaries
  const findings = [
    {
      type: 'critical' as const,
      title: '8 Firms Licensed Before Skidmore',
      description: 'Timeline impossibility proves Skidmore is a front person',
      date: '2025-12-07',
    },
    {
      type: 'warning' as const,
      title: '6 Firms at Same Frisco TX Address',
      description: 'Shell company pattern identified',
      date: '2025-12-07',
    },
    {
      type: 'info' as const,
      title: 'Kettler Management Identified as Primary Nexus',
      description: 'Operational evidence connects Kettler to all activities',
      date: '2025-12-07',
    },
  ]

  const iconMap = {
    critical: AlertTriangle,
    warning: AlertTriangle,
    info: Info,
  }

  const colorMap = {
    critical: 'text-red-600 bg-red-50 border-red-200',
    warning: 'text-amber-600 bg-amber-50 border-amber-200',
    info: 'text-blue-600 bg-blue-50 border-blue-200',
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-semibold mb-4">Recent Findings</h2>
      <div className="space-y-4">
        {findings.map((finding, index) => {
          const Icon = iconMap[finding.type]
          return (
            <div
              key={index}
              className={`p-4 rounded-lg border ${colorMap[finding.type]}`}
            >
              <div className="flex items-start space-x-3">
                <Icon className="w-5 h-5 mt-0.5 flex-shrink-0" />
                <div className="flex-1">
                  <h3 className="font-semibold mb-1">{finding.title}</h3>
                  <p className="text-sm opacity-90">{finding.description}</p>
                  <p className="text-xs mt-2 opacity-75">{finding.date}</p>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
