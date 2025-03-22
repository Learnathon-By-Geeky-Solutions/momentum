import type { NextConfig } from "next"

const nextConfig: NextConfig = {
  basePath: "/momentum",
  output: "export",
  images: {
    unoptimized: true,
  },
  /* config options here */
}

export default nextConfig
