/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true, // Enable App Router
  },
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000',
  },
  trailingSlash: false,
  generateBuildManifest: true,
}

module.exports = nextConfig