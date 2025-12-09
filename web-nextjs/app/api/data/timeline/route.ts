import { getTimeline } from '@/lib/api'
import { NextResponse } from 'next/server'

export async function GET() {
  try {
    const timeline = await getTimeline()
    return NextResponse.json(timeline)
  } catch (error) {
    console.error('Error fetching timeline:', error)
    return NextResponse.json(
      { error: 'Failed to fetch timeline' },
      { status: 500 }
    )
  }
}
