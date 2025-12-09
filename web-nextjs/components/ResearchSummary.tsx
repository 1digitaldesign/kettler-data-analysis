import { Database, FileText, Search } from 'lucide-react'

export function ResearchSummary() {
  const researchAreas = [
    {
      name: 'Nexus Analysis',
      description: 'Identification of primary operators and front persons',
      icon: Search,
      count: '1 report',
    },
    {
      name: 'Connection Matrix',
      description: 'Firm-to-firm and individual connections',
      icon: Database,
      count: '8 analyses',
    },
    {
      name: 'Violation Evidence',
      description: 'Unlicensed practice and regulatory violations',
      icon: FileText,
      count: '6 compilations',
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {researchAreas.map((area) => {
        const Icon = area.icon
        return (
          <div key={area.name} className="card hover:shadow-lg transition-shadow">
            <div className="flex items-start space-x-4">
              <div className="p-3 bg-primary-100 rounded-lg">
                <Icon className="w-6 h-6 text-primary-600" />
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold mb-1">{area.name}</h3>
                <p className="text-sm text-gray-600 mb-2">{area.description}</p>
                <p className="text-xs text-gray-500">{area.count}</p>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
