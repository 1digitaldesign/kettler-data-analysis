# Quick Start Guide

## Local Development

1. **Install Dependencies**
   ```bash
   cd web-nextjs
   npm install
   ```

2. **Run Development Server**
   ```bash
   npm run dev
   ```

3. **Open Browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Available Pages

- **Dashboard** (`/`) - Overview with statistics and charts
- **Firms Explorer** (`/firms`) - Browse and search all firms
- **Connections** (`/connections`) - Network visualization
- **Research** (`/research`) - Nexus findings and analysis
- **Violations** (`/violations`) - Documented violations
- **Timeline** (`/timeline`) - Chronological events

## Data Requirements

The app expects data files in:
- `../data/` - Source data (firms, licenses)
- `../research/` - Research findings and analysis

Ensure these directories exist relative to `web-nextjs/`.

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### Type Errors
```bash
npm run type-check
```

### Build Errors
```bash
npm run build
```

## Next Steps

1. Test all pages locally
2. Verify data loads correctly
3. Deploy to Vercel (see DEPLOYMENT.md)
