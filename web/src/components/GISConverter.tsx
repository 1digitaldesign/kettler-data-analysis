import axios from 'axios'
import { AlertCircle, CheckCircle, Download, FileText, Loader, Map, Upload } from 'lucide-react'
import { useState } from 'react'

interface GISConversionJob {
  id: string
  inputFile: string
  outputFormat: string
  status: 'pending' | 'running' | 'completed' | 'error'
  result?: any
  error?: string
  startedAt?: Date
  completedAt?: Date
}

export default function GISConverter() {
  const [inputFile, setInputFile] = useState<File | null>(null)
  const [outputFormat, setOutputFormat] = useState('geojson')
  const [targetSRS, setTargetSRS] = useState('')
  const [jobs, setJobs] = useState<GISConversionJob[]>([])
  const [loading, setLoading] = useState(false)

  const formats = [
    { value: 'geojson', label: 'GeoJSON', description: 'JSON format for geographic data' },
    { value: 'shp', label: 'Shapefile', description: 'ESRI Shapefile format' },
    { value: 'kml', label: 'KML', description: 'Keyhole Markup Language' },
    { value: 'kmz', label: 'KMZ', description: 'Compressed KML' },
    { value: 'gpkg', label: 'GPKG', description: 'GeoPackage format' },
    { value: 'gml', label: 'GML', description: 'Geography Markup Language' },
  ]

  const commonSRS = [
    { value: 'EPSG:4326', label: 'WGS84 (EPSG:4326)' },
    { value: 'EPSG:3857', label: 'Web Mercator (EPSG:3857)' },
    { value: 'EPSG:2263', label: 'NAD83 / New York Long Island (EPSG:2263)' },
    { value: 'EPSG:32118', label: 'NAD83 / New York Long Island East (EPSG:32118)' },
  ]

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setInputFile(file)
    }
  }

  const handleConvert = async () => {
    if (!inputFile) {
      alert('Please select a file to convert')
      return
    }

    setLoading(true)
    const jobId = `gis_${Date.now()}`

    const newJob: GISConversionJob = {
      id: jobId,
      inputFile: inputFile.name,
      outputFormat,
      status: 'running',
      startedAt: new Date(),
    }
    setJobs(prev => [newJob, ...prev])

    try {
      // Upload file first (in real implementation, use proper file upload endpoint)
      const formData = new FormData()
      formData.append('file', inputFile)

      // For now, we'll use the convert endpoint with file path
      // In production, implement proper file upload handling
      const response = await axios.post('/api/gis/convert', {
        input_file: inputFile.name, // This would be the uploaded file path
        output_format: outputFormat,
        target_srs: targetSRS || undefined,
      })

      setJobs(prev => prev.map(job =>
        job.id === jobId
          ? {
              ...job,
              status: 'completed',
              result: response.data.data,
              completedAt: new Date(),
            }
          : job
      ))
    } catch (error: any) {
      setJobs(prev => prev.map(job =>
        job.id === jobId
          ? {
              ...job,
              status: 'error',
              error: error.response?.data?.detail || error.message || 'Conversion failed',
              completedAt: new Date(),
            }
          : job
      ))
    } finally {
      setLoading(false)
    }
  }

  const downloadResult = (job: GISConversionJob) => {
    if (!job.result) return

    const dataStr = JSON.stringify(job.result, null, 2)
    const blob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `conversion_result_${job.id}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <Map className="h-8 w-8 text-green-500" />
          <h1 className="text-3xl font-bold text-gray-900">GIS File Converter</h1>
        </div>
        <p className="text-sm text-gray-600">
          Convert GIS files between formats (Shapefile, GeoJSON, KML, etc.) using GDAL
        </p>
      </div>

      {/* Conversion Form */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">File Conversion</h2>

        {/* File Upload */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Input File
          </label>
          <div className="flex items-center gap-4">
            <label className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700 cursor-pointer">
              <Upload className="h-5 w-5" />
              Choose File
              <input
                type="file"
                onChange={handleFileSelect}
                accept=".shp,.geojson,.kml,.kmz,.gpkg,.gml,.tif,.tiff"
                className="hidden"
              />
            </label>
            {inputFile && (
              <span className="text-sm text-gray-700">{inputFile.name}</span>
            )}
          </div>
          <p className="mt-2 text-xs text-gray-500">
            Supported formats: Shapefile, GeoJSON, KML, KMZ, GPKG, GML, GeoTIFF
          </p>
        </div>

        {/* Output Format */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Output Format
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {formats.map((format) => (
              <button
                key={format.value}
                onClick={() => setOutputFormat(format.value)}
                className={`p-4 border-2 rounded-lg text-left transition-all ${
                  outputFormat === format.value
                    ? 'border-green-500 bg-green-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="font-semibold text-gray-900">{format.label}</div>
                <div className="text-xs text-gray-600 mt-1">{format.description}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Target SRS (Optional) */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Target Spatial Reference System (Optional)
          </label>
          <select
            value={targetSRS}
            onChange={(e) => setTargetSRS(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg"
          >
            <option value="">Keep original SRS</option>
            {commonSRS.map(srs => (
              <option key={srs.value} value={srs.value}>{srs.label}</option>
            ))}
          </select>
          <input
            type="text"
            value={targetSRS}
            onChange={(e) => setTargetSRS(e.target.value)}
            placeholder="Or enter custom EPSG code (e.g., EPSG:4326)"
            className="mt-2 w-full px-4 py-2 border border-gray-300 rounded-lg"
          />
        </div>

        {/* Convert Button */}
        <button
          onClick={handleConvert}
          disabled={loading || !inputFile}
          className="w-full bg-green-500 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
        >
          {loading ? (
            <>
              <Loader className="animate-spin mr-2 h-5 w-5" />
              Converting...
            </>
          ) : (
            <>
              <FileText className="mr-2 h-5 w-5" />
              Convert File
            </>
          )}
        </button>
      </div>

      {/* Results */}
      {jobs.length > 0 && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">
              Conversion Jobs ({jobs.length})
            </h2>
          </div>
          <div className="divide-y divide-gray-200">
            {jobs.map((job) => (
              <div key={job.id} className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-xs font-medium text-green-600 bg-green-100 px-2 py-1 rounded">
                        {job.outputFormat.toUpperCase()}
                      </span>
                      {job.status === 'running' && (
                        <Loader className="animate-spin h-4 w-4 text-blue-500" />
                      )}
                      {job.status === 'completed' && (
                        <CheckCircle className="h-4 w-4 text-green-500" />
                      )}
                      {job.status === 'error' && (
                        <AlertCircle className="h-4 w-4 text-red-500" />
                      )}
                      <span className={`text-sm font-medium ${
                        job.status === 'completed' ? 'text-green-700' :
                        job.status === 'error' ? 'text-red-700' :
                        job.status === 'running' ? 'text-blue-700' :
                        'text-gray-700'
                      }`}>
                        {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
                      </span>
                    </div>
                    <div className="text-sm text-gray-600 space-y-1">
                      <div><strong>Input:</strong> {job.inputFile}</div>
                      <div><strong>Output Format:</strong> {job.outputFormat}</div>
                    </div>
                    {job.startedAt && (
                      <p className="text-xs text-gray-500 mt-2">
                        Started: {job.startedAt.toLocaleString()}
                        {job.completedAt && ` • Completed: ${job.completedAt.toLocaleString()}`}
                      </p>
                    )}
                  </div>
                  {job.status === 'completed' && job.result && (
                    <button
                      onClick={() => downloadResult(job)}
                      className="flex items-center gap-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-700 transition-colors"
                    >
                      <Download className="h-4 w-4" />
                      Download
                    </button>
                  )}
                </div>

                {/* Results Display */}
                {job.status === 'completed' && job.result && (
                  <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                    <h3 className="text-sm font-semibold text-gray-900 mb-2">Conversion Result</h3>
                    <div className="text-sm text-gray-700 space-y-1">
                      <div><strong>Output File:</strong> {job.result.output_file}</div>
                      <div><strong>Feature Count:</strong> {job.result.feature_count}</div>
                      <div><strong>Input Format:</strong> {job.result.input_format}</div>
                      <div><strong>Output Format:</strong> {job.result.output_format}</div>
                    </div>
                  </div>
                )}

                {/* Error Display */}
                {job.status === 'error' && job.error && (
                  <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <p className="text-sm text-red-700">
                      <strong>Error:</strong> {job.error}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
