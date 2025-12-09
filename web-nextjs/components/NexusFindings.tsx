'use client'

import { useEffect, useState } from 'react'
import ReactMarkdown from 'react-markdown'

export function NexusFindings() {
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/data/nexus-findings')
      .then(res => res.text())
      .then(text => {
        setContent(text)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <div className="card text-center py-12">Loading findings...</div>
  }

  return (
    <div className="card prose max-w-none">
      <h2 className="text-2xl font-semibold mb-4">Final Nexus Findings</h2>
      <div className="markdown-content">
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>
    </div>
  )
}
