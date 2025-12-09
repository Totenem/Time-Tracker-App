import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",

  // Expose env vars to the client
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
};

console.log("NEXT_PUBLIC_API_URL:", process.env.NEXT_PUBLIC_API_URL);

export default nextConfig;
