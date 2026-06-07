/** @type {import('next').NextConfig} */
const nextConfig = {
  // Produces a minimal self-contained server bundle (.next/standalone)
  // so the Docker image stays small. Required by the Dockerfile.
  output: "standalone",
};

export default nextConfig;
