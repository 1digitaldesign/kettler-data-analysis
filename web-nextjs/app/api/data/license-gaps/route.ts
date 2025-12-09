import { getLicenseGaps } from '@/lib/api'
import { NextResponse } from 'next/server'

export async function GET() {
  try {
    const data = await getLicenseGaps()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching license gaps:', error)
    return NextResponse.json(
      { error: 'Failed to fetch license gaps' },
      { status: 500 }
    )
  }
}
