/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  // Enable static file serving for data files
  async rewrites() {
    return [
      {
        source: '/api/data/:path*',
        destination: '/api/data/:path*',
      },
    ];
  },
  // Optimize images
  images: {
    domains: [],
    unoptimized: false,
  },
};

module.exports = nextConfig;
