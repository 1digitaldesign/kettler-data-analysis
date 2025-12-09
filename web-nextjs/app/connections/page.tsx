import { ConnectionNetwork } from '@/components/ConnectionNetwork'
import { ConnectionStats } from '@/components/ConnectionStats'

export default async function ConnectionsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Connection Analysis</h1>
        <p className="text-gray-600">
          Visualize relationships and connections between firms, individuals, and entities
        </p>
      </div>

      <ConnectionStats />
      <ConnectionNetwork />
    </div>
  )
}
