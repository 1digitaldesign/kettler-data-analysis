# Deployment Guide for Vercel

## Prerequisites

1. GitHub repository with the code
2. Vercel account (free tier works)

## Deployment Steps

### 1. Prepare Repository

Ensure your repository structure includes:
```
kettler-data-analysis/
├── web-nextjs/          # Next.js app
├── data/                # Data files
├── research/            # Research files
└── ...
```

### 2. Deploy to Vercel

#### Option A: Via Vercel Dashboard

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `web-nextjs`
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)
   - **Install Command**: `npm install` (default)

#### Option B: Via Vercel CLI

```bash
cd web-nextjs
npm install -g vercel
vercel
```

Follow the prompts to link your project.

### 3. Environment Variables

No environment variables are required for basic functionality. The app automatically detects Vercel environment and adjusts file paths.

### 4. File Access

**Important**: Vercel's serverless functions have read-only access to files in your repository. Ensure:

- Data files are committed to the repository (or use a different storage solution)
- File paths are correctly resolved (handled in `lib/api.ts`)

### 5. Alternative: Use API Routes

For production, consider:
- Moving data to a database (PostgreSQL, MongoDB)
- Using an API service (your existing microservices)
- Storing data in cloud storage (S3, Google Cloud Storage)

## Post-Deployment

1. Check build logs for any errors
2. Test all pages:
   - `/` - Dashboard
   - `/firms` - Firms Explorer
   - `/connections` - Connection Analysis
   - `/research` - Research Findings
   - `/violations` - Violations
   - `/timeline` - Timeline

## Troubleshooting

### Build Errors

- **File not found**: Check that data files are in the repository
- **Path errors**: Verify `lib/api.ts` path resolution logic
- **TypeScript errors**: Run `npm run type-check` locally first

### Runtime Errors

- **API routes failing**: Check server logs in Vercel dashboard
- **Data not loading**: Verify file paths and permissions
- **CORS issues**: Not applicable for same-origin requests

## Performance Optimization

1. **Static Generation**: Consider using `generateStaticParams` for static pages
2. **Caching**: Add cache headers to API routes
3. **Image Optimization**: Use Next.js Image component
4. **Code Splitting**: Already handled by Next.js automatically

## Monitoring

- Use Vercel Analytics (optional)
- Monitor serverless function execution times
- Set up error tracking (Sentry, etc.)
