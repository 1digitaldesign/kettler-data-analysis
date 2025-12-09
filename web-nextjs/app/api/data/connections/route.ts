import { getConnections } from '@/lib/api'
import { NextResponse } from 'next/server'

export async function GET() {
  try {
    const connections = await getConnections()
    return NextResponse.json(connections)
  } catch (error) {
    console.error('Error fetching connections:', error)
    return NextResponse.json(
      { error: 'Failed to fetch connections' },
      { status: 500 }
    )
  }
}
