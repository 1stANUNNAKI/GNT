/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: "standalone",
  images: {
    domains: ["avatars.githubusercontent.com"],
  },
};

export default nextConfig;
