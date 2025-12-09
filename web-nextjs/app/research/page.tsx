import { NexusFindings } from '@/components/NexusFindings'
import { ResearchSummary } from '@/components/ResearchSummary'

export default async function ResearchPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Research & Analysis</h1>
        <p className="text-gray-600">
          Comprehensive research findings, nexus analysis, and evidence summaries
        </p>
      </div>

      <NexusFindings />
      <ResearchSummary />
    </div>
  )
}
