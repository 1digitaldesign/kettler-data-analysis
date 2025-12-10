import { FirmsFilters } from '@/components/FirmsFilters'
import { FirmsTable } from '@/components/FirmsTable'

export default async function FirmsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Firms Explorer</h1>
        <p className="text-gray-600">
          Browse and search through all registered firms associated with Caitlin Skidmore
        </p>
      </div>

      <FirmsFilters />
      <FirmsTable />
    </div>
  )
}
