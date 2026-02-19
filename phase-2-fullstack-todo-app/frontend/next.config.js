/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://fazalahmed-full-stack-todo-app.hf.space',
  },
  trailingSlash: false,
}

module.exports = nextConfig