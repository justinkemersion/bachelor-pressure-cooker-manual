import type { NextConfig } from "next";
import { assertValidBookInternalLinks } from "./src/lib/content";

const nextConfig: NextConfig = {
  output: "standalone",
};

export default async function createNextConfig(): Promise<NextConfig> {
  await assertValidBookInternalLinks();
  return nextConfig;
}
