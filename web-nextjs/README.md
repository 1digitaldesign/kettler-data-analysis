# Kettler Data Visualization Dashboard

A Next.js 14 application for visualizing and analyzing Kettler Management investigation data.

## Features

- **Dashboard**: Overview statistics and key metrics
- **Firms Explorer**: Browse and search all registered firms
- **Connection Analysis**: Network visualization of firm relationships
- **Research Findings**: Nexus analysis and research summaries
- **Violations**: Documented violations and evidence
- **Timeline**: Chronological view of license events

## Tech Stack

- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **Recharts** (Data visualization)
- **React Force Graph** (Network visualization)
- **Lucide React** (Icons)

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
cd web-nextjs
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

```bash
npm run build
npm start
```

## Project Structure

```
web-nextjs/
├── app/                    # Next.js App Router pages
│   ├── api/               # API routes
│   ├── firms/             # Firms explorer page
│   ├── connections/       # Connection analysis page
│   ├── research/          # Research findings page
│   ├── violations/        # Violations page
│   └── timeline/          # Timeline page
├── components/            # React components
│   ├── charts/           # Chart components
│   └── ...
├── lib/                   # Utility functions
│   └── api.ts            # Data fetching functions
└── public/                # Static assets
```

## Data Sources

The application reads data from:
- `../data/` - Source data files (firms, licenses)
- `../research/` - Research findings and analysis

## Deployment to Vercel

1. Push code to GitHub
2. Import project in Vercel
3. Configure build settings:
   - Framework: Next.js
   - Root Directory: `web-nextjs`
   - Build Command: `npm run build`
   - Output Directory: `.next`

The `vercel.json` file is already configured for optimal deployment.

## API Routes

- `GET /api/data/firms` - Get all firms
- `GET /api/data/license-gaps` - Get license gap analysis
- `GET /api/data/connections` - Get connection matrix
- `GET /api/data/timeline` - Get timeline events
- `GET /api/data/violations` - Get violations
- `GET /api/data/nexus-findings` - Get nexus findings (markdown)

## License

Private project - Kettler Data Analysis
