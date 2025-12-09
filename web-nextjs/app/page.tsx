import { QuickStats } from '@/components/QuickStats'
import { RecentFindings } from '@/components/RecentFindings'
import { LicenseGapChart } from '@/components/charts/LicenseGapChart'
import { StateDistributionChart } from '@/components/charts/StateDistributionChart'

export default async function HomePage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          Kettler Data Analysis Dashboard
        </h1>
        <p className="text-gray-600">
          Comprehensive visualization and analysis of firm licenses, connections, and violations
        </p>
      </div>

      <QuickStats />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-2xl font-semibold mb-4">License Gap Analysis</h2>
          <LicenseGapChart />
        </div>

        <div className="card">
          <h2 className="text-2xl font-semibold mb-4">State Distribution</h2>
          <StateDistributionChart />
        </div>
      </div>

      <RecentFindings />
    </div>
  )
}
