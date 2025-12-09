import { getFirms } from '@/lib/api'
import { NextResponse } from 'next/server'

export async function GET() {
  try {
    const firms = await getFirms()
    return NextResponse.json(firms)
  } catch (error) {
    console.error('Error fetching firms:', error)
    return NextResponse.json(
      { error: 'Failed to fetch firms' },
      { status: 500 }
    )
  }
}
