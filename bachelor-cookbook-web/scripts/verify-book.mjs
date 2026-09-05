#!/usr/bin/env node
/**
 * Asserts the markdown book is visible from this package.
 * Used by `npm test` and as a Docker-build sanity check.
 */
import { readdir, stat } from "node:fs/promises";
import path from "node:path";

function resolveBookRoot() {
  const fromEnv = process.env.BOOK_ROOT?.trim();
  if (fromEnv) return path.resolve(fromEnv);
  return path.join(process.cwd(), "..", "bachelor-cookbook-book");
}

const SECTION_DIRS = [
  "01_fundamentals",
  "02_techniques",
  "03_recipes",
  "04_reference",
];

async function collectMarkdown(dir) {
  const entries = await readdir(dir, { withFileTypes: true });
  let count = 0;
  for (const ent of entries) {
    const full = path.join(dir, ent.name);
    if (ent.isDirectory()) {
      count += await collectMarkdown(full);
    } else if (ent.isFile() && ent.name.endsWith(".md")) {
      count += 1;
    }
  }
  return count;
}

const bookRoot = resolveBookRoot();
const rootStat = await stat(bookRoot).catch(() => null);
if (!rootStat?.isDirectory()) {
  console.error(`verify-book: BOOK_ROOT is not a directory: ${bookRoot}`);
  process.exit(1);
}

let total = 0;
for (const folder of SECTION_DIRS) {
  const sectionDir = path.join(bookRoot, folder);
  const st = await stat(sectionDir).catch(() => null);
  if (!st?.isDirectory()) {
    console.error(`verify-book: missing section ${folder} under ${bookRoot}`);
    process.exit(1);
  }
  const n = await collectMarkdown(sectionDir);
  if (n === 0) {
    console.error(`verify-book: no markdown in ${folder}`);
    process.exit(1);
  }
  console.log(`verify-book: ${folder} → ${n} markdown files`);
  total += n;
}

console.log(`verify-book: OK (${total} files) at ${bookRoot}`);
