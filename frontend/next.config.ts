import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  basePath: process.env.NEXT_PUBLIC_BASE_PATH,
  output: "export",
  images: {
    unoptimized: true,
  },
  /* config options here */
};

export default nextConfig;
