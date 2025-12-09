# Web Scraping Feature

## Overview

Added comprehensive web scraping functionality to the web application, allowing users to scrape data from various platforms directly from the browser interface.

## Features

### 1. Multi-Platform Support
- **Airbnb** - Scrape Airbnb listings by address
- **VRBO** - Scrape VRBO listings by address
- **Front Websites** - Scrape company websites by URL
- **Multi-Platform** - Scrape across multiple platforms simultaneously

### 2. User Interface Components

#### WebScraping Component (`web/src/components/WebScraping.tsx`)
- Platform selection with visual cards
- Multi-line target input (addresses or URLs)
- Real-time job status tracking
- Results display with preview
- Export functionality (JSON download)
- Error handling and display

#### ScrapingResults Component (`web/src/components/ScrapingResults.tsx`)
- Grid layout for listing cards
- Key information display (title, address, price)
- External link support
- Responsive design

### 3. Backend API Endpoints

#### POST `/api/scraping/scrape`
Scrapes data from specified platform.

**Request:**
```json
{
  "platform": "airbnb",
  "targets": ["800 John Carlyle Street, Alexandria, VA"]
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "platform": "airbnb",
    "listings": [...]
  }
}
```

#### GET `/api/scraping/platforms`
Returns available scraping platforms.

**Response:**
```json
{
  "platforms": [
    {"id": "airbnb", "name": "Airbnb", "description": "..."},
    ...
  ]
}
```

### 4. Integration

- Integrated with `UnifiedScraper` Python module
- Uses existing scraping infrastructure
- Saves results to standard data directories
- Compatible with vector embedding system

## Usage

### From Web Interface

1. Navigate to **Scraping** page
2. Select platform (Airbnb, VRBO, Front Websites, or Multi-Platform)
3. Enter targets (one per line):
   - For Airbnb/VRBO: addresses
   - For Front Websites: URLs
4. Click **Start Scraping**
5. View results in real-time
6. Export results as JSON

### Example Targets

**Airbnb/VRBO:**
```
800 John Carlyle Street, Alexandria, VA
123 Main Street, Washington, DC
```

**Front Websites:**
```
https://www.example-property.com
https://www.company-website.com
```

## Technical Details

### Frontend
- React component with state management
- Axios for API calls
- Real-time status updates
- Job queue display
- Error handling

### Backend
- FastAPI endpoint integration
- Calls `UnifiedScraper` methods:
  - `scrape_airbnb()`
  - `scrape_vrbo()`
  - `scrape_front_websites()`
  - `scrape_multi_platform()`
- Error handling and validation

### Data Flow

1. User enters targets and selects platform
2. Frontend sends POST request to `/api/scraping/scrape`
3. Backend calls appropriate `UnifiedScraper` method
4. Results returned to frontend
5. Displayed in UI with export option
6. Results also saved to `data/scraped/` directory

## Benefits

1. **User-Friendly** - No command-line needed
2. **Visual Feedback** - Real-time status updates
3. **Batch Processing** - Multiple targets at once
4. **Export Capability** - Download results as JSON
5. **Error Handling** - Clear error messages
6. **Integration** - Works with existing Python modules

## Future Enhancements

1. Scheduled scraping
2. Scraping history
3. Advanced filtering
4. Comparison views
5. Email notifications
6. Scraping templates
7. Rate limiting display
8. Progress bars for large batches

## Files Created/Modified

### Created
- `web/src/components/WebScraping.tsx` - Main scraping interface
- `web/src/components/ScrapingResults.tsx` - Results display component
- `WEB_SCRAPING_FEATURE.md` - This documentation

### Modified
- `web/src/App.tsx` - Added scraping route
- `api/server.py` - Added scraping endpoints
- `web/src/utils/api.ts` - Added scraping API functions

## Testing

To test the scraping feature:

1. Start the API server:
   ```bash
   python api/server.py
   ```

2. Start the web app:
   ```bash
   cd web
   npm run dev
   ```

3. Navigate to http://localhost:3000/scraping

4. Enter a test address and click "Start Scraping"

5. Verify results appear in the UI

6. Test export functionality

## Notes

- Scraping may take time depending on targets
- Some platforms may have rate limits
- Results are cached in browser session
- Export downloads JSON file with all results
