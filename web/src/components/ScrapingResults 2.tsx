import { Calendar, DollarSign, Download, ExternalLink, MapPin } from 'lucide-react'

interface Listing {
  title?: string
  address?: string
  price?: string
  url?: string
  description?: string
  [key: string]: any
}

interface ScrapingResultsProps {
  results: any
  platform: string
  onExport?: () => void
}

export default function ScrapingResults({ results, platform, onExport }: ScrapingResultsProps) {
  const listings: Listing[] = results.listings || results.scraped_data || []

  if (listings.length === 0) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-sm text-yellow-800">No listings found for this search.</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold text-gray-900">
          Found {listings.length} {listings.length === 1 ? 'listing' : 'listings'}
        </h3>
        {onExport && (
          <button
            onClick={onExport}
            className="flex items-center gap-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            <Download className="h-4 w-4" />
            Export JSON
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {listings.map((listing, idx) => (
          <div
            key={idx}
            className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            {listing.title && (
              <h4 className="font-semibold text-gray-900 mb-2">{listing.title}</h4>
            )}
            {listing.address && (
              <div className="flex items-start gap-2 mb-2 text-sm text-gray-600">
                <MapPin className="h-4 w-4 mt-0.5 flex-shrink-0" />
                <span>{listing.address}</span>
              </div>
            )}
            {listing.price && (
              <div className="flex items-center gap-2 mb-2 text-sm font-semibold text-green-600">
                <DollarSign className="h-4 w-4" />
                <span>{listing.price}</span>
              </div>
            )}
            {listing.description && (
              <p className="text-sm text-gray-600 mb-2 line-clamp-2">{listing.description}</p>
            )}
            {listing.url && (
              <a
                href={listing.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-xs text-blue-600 hover:text-blue-800"
              >
                <ExternalLink className="h-3 w-3" />
                View Listing
              </a>
            )}
            {listing.date && (
              <div className="flex items-center gap-2 mt-2 text-xs text-gray-500">
                <Calendar className="h-3 w-3" />
                <span>{listing.date}</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
