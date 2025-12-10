import { getViolations } from '@/lib/api'
import { NextResponse } from 'next/server'

export async function GET() {
  try {
    const violations = await getViolations()
    return NextResponse.json(violations)
  } catch (error) {
    console.error('Error fetching violations:', error)
    return NextResponse.json(
      { error: 'Failed to fetch violations' },
      { status: 500 }
    )
  }
}
