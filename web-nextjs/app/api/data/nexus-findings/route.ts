import { getNexusFindings } from '@/lib/api'
import { NextResponse } from 'next/server'

export async function GET() {
  try {
    const findings = await getNexusFindings()
    return new NextResponse(findings, {
      headers: {
        'Content-Type': 'text/markdown',
      },
    })
  } catch (error) {
    console.error('Error fetching nexus findings:', error)
    return NextResponse.json(
      { error: 'Failed to fetch nexus findings' },
      { status: 500 }
    )
  }
}
