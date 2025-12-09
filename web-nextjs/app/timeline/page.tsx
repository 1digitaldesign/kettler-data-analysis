import { TimelineChart } from '@/components/charts/TimelineChart'

export default async function TimelinePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Timeline Analysis</h1>
        <p className="text-gray-600">
          Chronological view of license issuances, expirations, and key events
        </p>
      </div>

      <TimelineChart />
    </div>
  )
}
