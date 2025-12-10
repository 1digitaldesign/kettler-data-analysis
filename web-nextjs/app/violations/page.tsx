import { ViolationsTable } from '@/components/ViolationsTable'
import { ViolationStats } from '@/components/ViolationStats'

export default async function ViolationsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Violations & Evidence</h1>
        <p className="text-gray-600">
          Documented violations, unlicensed practice evidence, and regulatory infractions
        </p>
      </div>

      <ViolationStats />
      <ViolationsTable />
    </div>
  )
}
