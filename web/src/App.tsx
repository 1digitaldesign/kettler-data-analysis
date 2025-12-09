import { BarChart3, Building2, FileSearch, Globe, Home, Search } from 'lucide-react'
import { Link, Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import ACRISSearch from './components/ACRISSearch'
import AnalysisTools from './components/AnalysisTools'
import Dashboard from './components/Dashboard'
import DataVisualization from './components/DataVisualization'
import SearchInterface from './components/SearchInterface'
import WebScraping from './components/WebScraping'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <nav className="bg-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <h1 className="text-xl font-bold text-gray-900">Kettler Data Analysis</h1>
                </div>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  <Link
                    to="/"
                    className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 hover:text-gray-700"
                  >
                    <Home className="mr-2 h-4 w-4" />
                    Dashboard
                  </Link>
                  <Link
                    to="/search"
                    className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-700"
                  >
                    <Search className="mr-2 h-4 w-4" />
                    Search
                  </Link>
                  <Link
                    to="/analysis"
                    className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-700"
                  >
                    <FileSearch className="mr-2 h-4 w-4" />
                    Analysis
                  </Link>
                  <Link
                    to="/visualization"
                    className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-700"
                  >
                    <BarChart3 className="mr-2 h-4 w-4" />
                    Visualization
                  </Link>
                  <Link
                    to="/scraping"
                    className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-700"
                  >
                    <Globe className="mr-2 h-4 w-4" />
                    Scraping
                  </Link>
                  <Link
                    to="/acris"
                    className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-700"
                  >
                    <Building2 className="mr-2 h-4 w-4" />
                    ACRIS
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/search" element={<SearchInterface />} />
            <Route path="/analysis" element={<AnalysisTools />} />
            <Route path="/visualization" element={<DataVisualization />} />
            <Route path="/scraping" element={<WebScraping />} />
            <Route path="/acris" element={<ACRISSearch />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
