import { readdir, readFile, stat } from "fs/promises";
import path from "path";

/**
 * Loads markdown from ../bachelor-cookbook-book/{01_fundamentals,...} (relative to this package).
 * Local MVP only: that path is outside the deploy bundle on typical hosts.
 */
const BOOK_ROOT = path.join(
  process.cwd(),
  "..",
  "bachelor-cookbook-book",
);

const SECTION_DIRS = [
  { folder: "01_fundamentals", category: "fundamentals" },
  { folder: "02_techniques", category: "techniques" },
  { folder: "03_recipes", category: "recipes" },
  { folder: "04_reference", category: "reference" },
] as const;

export type ContentCategory = (typeof SECTION_DIRS)[number]["category"];

export function isContentCategory(s: string): s is ContentCategory {
  return (
    s === "fundamentals" ||
    s === "techniques" ||
    s === "recipes" ||
    s === "reference"
  );
}

export type RecipeMetadata = {
  mission?: string;
  timeBucket?: string;
  effort?: string;
  heat?: string;
  protein?: string;
};

export type ContentItem = {
  category: ContentCategory;
  /** Path under the category folder, no .md, e.g. `condiments/maverick_red_v2` */
  slug: string;
  title: string;
  metadata: RecipeMetadata;
  ingredients: string | null;
  instructions: string | null;
  /** Markdown with internal book links rewritten for the web app */
  raw: string;
  /** Last modified time (ms) for sorting */
  updatedAt: number;
};

const TITLE_RE = /^#\s+(.+?)\s*$/;
const INGREDIENTS_HEADING = /^##\s+ingredients\s*$/i;
const INSTRUCTIONS_HEADING = /^##\s+instructions\s*$/i;

const BOOK_PREFIX_RE =
  /^(01_fundamentals|02_techniques|03_recipes|04_reference)\/(.*)$/i;

const PREFIX_TO_CATEGORY: Record<string, ContentCategory> = {
  "01_fundamentals": "fundamentals",
  "02_techniques": "techniques",
  "03_recipes": "recipes",
  "04_reference": "reference",
};

/**
 * Turns book-relative targets like `../01_fundamentals/liquid_ratios.md#x` into
 * `/fundamentals/liquid_ratios#x` (no .md). Idempotent on already-web paths.
 */
export function transformBookHrefToWeb(href: string): string | null {
  let h = href.trim();
  if (h.startsWith("<") && h.endsWith(">")) {
    h = h.slice(1, -1).trim();
  }
  if (/^(https?:|mailto:|tel:|\/\/)/i.test(h)) return null;
  if (h.startsWith("#") && !h.slice(1).includes("/")) return null;

  h = h.replace(/\\/g, "/");

  let hash = "";
  const hashIdx = h.indexOf("#");
  if (hashIdx >= 0) {
    hash = h.slice(hashIdx);
    h = h.slice(0, hashIdx);
  }
  const qIdx = h.indexOf("?");
  if (qIdx >= 0) h = h.slice(0, qIdx);

  h = h.trim().replace(/^\.\/+/, "");
  while (h.startsWith("../")) {
    h = h.slice(3);
  }
  h = h.replace(/^\/+/, "");

  const m = h.match(BOOK_PREFIX_RE);
  if (!m) return null;

  const bookPrefix = m[1].toLowerCase();
  const category = PREFIX_TO_CATEGORY[bookPrefix];
  if (!category) return null;

  const rest = m[2].replace(/\.md$/i, "").replace(/\/+$/, "");

  const encoded = rest
    .split("/")
    .filter(Boolean)
    .map((seg) => encodeURIComponent(seg))
    .join("/");
  return `/${category}/${encoded}${hash}`;
}

/** Resolve a book or app path to `category/slugPath` for validation, or null if not internal. */
export function resolveBookLinkToCanonicalKey(href: string): string | null {
  const fromBook = transformBookHrefToWeb(href);
  if (fromBook) {
    return webPathToCanonicalKey(fromBook);
  }
  return resolveAppPathToCanonicalKey(href);
}

function webPathToCanonicalKey(webPath: string): string | null {
  const [pathPart, ...hashParts] = webPath.split("#");
  void hashParts;
  const trimmed = pathPart.replace(/^\/+/, "");
  const segments = trimmed.split("/").filter(Boolean);
  if (segments.length < 2) return null;
  const category = decodeURIComponent(segments[0]);
  if (!isContentCategory(category)) return null;
  const slug = segments
    .slice(1)
    .map((s) => decodeURIComponent(s))
    .join("/");
  return `${category}/${slug}`;
}

function resolveAppPathToCanonicalKey(href: string): string | null {
  let h = href.trim();
  if (h.startsWith("<") && h.endsWith(">")) {
    h = h.slice(1, -1).trim();
  }
  if (!h.startsWith("/") || h.startsWith("//")) return null;
  return webPathToCanonicalKey(h);
}

/**
 * Rewrite inline markdown links `[text](path/to/file.md)` that point at numbered
 * book folders to the web app URL shape. Safe to run more than once.
 */
export function transformMarkdownLinks(content: string): string {
  return content.replace(/\]\(\s*([^)]+)\s*\)/g, (full, rawHref: string) => {
    const web = transformBookHrefToWeb(rawHref);
    if (web === null) return full;
    return `](${web})`;
  });
}

/** @deprecated Use transformMarkdownLinks */
export const rewriteInternalLinks = transformMarkdownLinks;

function rawTitleFromContent(raw: string): string {
  for (const line of raw.split(/\r?\n/)) {
    const m = line.match(TITLE_RE);
    if (m?.[1]) return m[1].trim();
  }
  return "";
}

export function cleanTitle(rawHeading: string, relPath: string): string {
  let t = rawHeading.trim();
  t = t.replace(/\.md$/i, "");
  t = t.replace(/^\d{2}_[a-z_]+\s*:\s*/i, "");
  t = t.replace(/^03_Recipes\s*:\s*/i, "");
  t = t.replace(/^03_recipes\s*:\s*/i, "");
  t = t.replace(/^03_Recipes\s*\/\s*/i, "");
  t = t.replace(/^03_recipes\s*\/\s*/i, "");
  t = t.replace(/^03_recipes\s+/i, "");
  t = t.replace(/\s+/g, " ").trim();

  if (!t) {
    t = humanizeFilenameStem(relPath);
  }
  return t;
}

function humanizeFilenameStem(relPath: string): string {
  const stem = relPath.replace(/\.md$/i, "").split(/[/\\]/).pop() ?? relPath;
  return stem
    .replace(/_/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

export function filePathToSlug(relPath: string): string {
  return relPath.replace(/\.md$/i, "").replace(/\\/g, "/");
}

function extractPreamble(raw: string): string {
  const lines = raw.split(/\r?\n/);
  const out: string[] = [];
  for (const line of lines) {
    if (/^##\s+/.test(line.trim())) break;
    out.push(line);
  }
  return out.join("\n");
}

function captureMetaLine(preamble: string, label: string): string | undefined {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const re = new RegExp(
    `^\\s*\\*\\*${escaped}:\\*\\*\\s*(.+?)\\s*$`,
    "im",
  );
  const m = preamble.match(re);
  return m?.[1]?.trim() || undefined;
}

export function parseRecipeMetadata(raw: string): RecipeMetadata {
  const preamble = extractPreamble(raw);
  const mission = captureMetaLine(preamble, "Mission");
  const timeBucket = captureMetaLine(preamble, "Time Bucket");
  const effort = captureMetaLine(preamble, "Effort");
  const heat = captureMetaLine(preamble, "Heat");
  const protein = captureMetaLine(preamble, "Protein");
  const meta: RecipeMetadata = {};
  if (mission) meta.mission = mission;
  if (timeBucket) meta.timeBucket = timeBucket;
  if (effort) meta.effort = effort;
  if (heat) meta.heat = heat;
  if (protein) meta.protein = protein;
  return meta;
}

function splitSections(content: string): {
  ingredients: string | null;
  instructions: string | null;
} {
  const lines = content.split(/\r?\n/);
  let ingStart = -1;
  let insStart = -1;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (INGREDIENTS_HEADING.test(line)) ingStart = i;
    else if (INSTRUCTIONS_HEADING.test(line)) insStart = i;
  }

  let ingredients: string | null = null;
  let instructions: string | null = null;

  if (ingStart >= 0) {
    const ingEnd = insStart >= 0 ? insStart : lines.length;
    ingredients = lines
      .slice(ingStart + 1, ingEnd)
      .join("\n")
      .trim();
    if (ingredients.length === 0) ingredients = null;
  }

  if (insStart >= 0) {
    instructions = lines.slice(insStart + 1).join("\n").trim();
    if (instructions.length === 0) instructions = null;
  }

  return { ingredients, instructions };
}

async function collectMarkdownFiles(
  dir: string,
  base: string,
): Promise<string[]> {
  const entries = await readdir(dir, { withFileTypes: true });
  const out: string[] = [];

  for (const ent of entries) {
    const rel = path.join(base, ent.name);
    const full = path.join(dir, ent.name);
    if (ent.isDirectory()) {
      out.push(...(await collectMarkdownFiles(full, rel)));
    } else if (ent.isFile() && ent.name.endsWith(".md")) {
      out.push(rel);
    }
  }

  return out;
}

function buildItem(
  category: ContentCategory,
  relWithinSection: string,
  rawSource: string,
  updatedAt: number,
): ContentItem {
  const raw = transformMarkdownLinks(rawSource);
  const rawHeading = rawTitleFromContent(raw);
  const title = cleanTitle(rawHeading || humanizeFilenameStem(relWithinSection), relWithinSection);
  const slug = filePathToSlug(relWithinSection);
  const metadata = parseRecipeMetadata(raw);
  const { ingredients, instructions } = splitSections(raw);

  return {
    category,
    slug,
    title,
    metadata,
    ingredients,
    instructions,
    raw,
    updatedAt,
  };
}

export async function getAllContent(): Promise<ContentItem[]> {
  const items: ContentItem[] = [];

  for (const { folder, category } of SECTION_DIRS) {
    const sectionDir = path.join(BOOK_ROOT, folder);
    const relPaths = await collectMarkdownFiles(sectionDir, "");

    for (const rel of relPaths) {
      const fullPath = path.join(sectionDir, rel);
      const [rawSource, st] = await Promise.all([
        readFile(fullPath, "utf8"),
        stat(fullPath),
      ]);
      items.push(
        buildItem(category, rel, rawSource, st.mtimeMs),
      );
    }
  }

  items.sort((a, b) => {
    const cat = a.category.localeCompare(b.category);
    if (cat !== 0) return cat;
    return a.title.localeCompare(b.title, "en");
  });

  return items;
}

export function groupContentByCategory(
  items: ContentItem[],
): Record<ContentCategory, ContentItem[]> {
  const empty: Record<ContentCategory, ContentItem[]> = {
    fundamentals: [],
    techniques: [],
    recipes: [],
    reference: [],
  };
  for (const item of items) {
    empty[item.category].push(item);
  }
  for (const k of Object.keys(empty) as ContentCategory[]) {
    empty[k].sort((a, b) => a.title.localeCompare(b.title, "en"));
  }
  return empty;
}

export async function getRecipes(): Promise<ContentItem[]> {
  const all = await getAllContent();
  return all.filter((i) => i.category === "recipes");
}

export function contentHref(item: Pick<ContentItem, "category" | "slug">): string {
  return `/${item.category}/${item.slug.split("/").map(encodeURIComponent).join("/")}`;
}

export async function getContentBySlug(
  category: string,
  slugPath: string,
): Promise<ContentItem | null> {
  if (!isContentCategory(category)) return null;
  const normalized = slugPath.replace(/\\/g, "/").replace(/^\/+|\/+$/g, "");
  const all = await getAllContent();
  return (
    all.find(
      (i) => i.category === category && i.slug === normalized,
    ) ?? null
  );
}

export async function getFundamentals(): Promise<ContentItem[]> {
  const all = await getAllContent();
  return all
    .filter((i) => i.category === "fundamentals")
    .sort((a, b) => a.title.localeCompare(b.title, "en"));
}

export async function getLatestRecipes(limit: number): Promise<ContentItem[]> {
  const all = await getAllContent();
  return all
    .filter((i) => i.category === "recipes")
    .sort((a, b) => b.updatedAt - a.updatedAt)
    .slice(0, limit);
}

export type BrokenInternalLink = {
  sourceKey: string;
  href: string;
  resolvedKey: string;
};

function collectInlineMarkdownTargets(markdown: string): string[] {
  const re = /\]\(\s*([^)]+)\s*\)/g;
  const out: string[] = [];
  let m: RegExpExecArray | null;
  while ((m = re.exec(markdown)) !== null) {
    out.push(m[1].trim());
  }
  return out;
}

/** Scan book markdown for `[text](...)` links that resolve to a missing page. */
export async function findBrokenInternalMarkdownLinks(): Promise<
  BrokenInternalLink[]
> {
  const files: { sourceKey: string; raw: string }[] = [];

  for (const { folder, category } of SECTION_DIRS) {
    const sectionDir = path.join(BOOK_ROOT, folder);
    const relPaths = await collectMarkdownFiles(sectionDir, "");
    for (const rel of relPaths) {
      const fullPath = path.join(sectionDir, rel);
      const raw = await readFile(fullPath, "utf8");
      files.push({
        sourceKey: `${category}/${filePathToSlug(rel)}`,
        raw,
      });
    }
  }

  const valid = new Set(files.map((f) => f.sourceKey));
  const broken: BrokenInternalLink[] = [];

  for (const { sourceKey, raw } of files) {
    for (const href of collectInlineMarkdownTargets(raw)) {
      const key = resolveBookLinkToCanonicalKey(href);
      if (key === null) continue;
      if (!valid.has(key)) {
        broken.push({ sourceKey, href, resolvedKey: key });
      }
    }
  }

  return broken;
}

/** Call from `next.config` during build; throws with a full report if any link is dead. */
export async function assertValidBookInternalLinks(): Promise<void> {
  if (process.env.SKIP_BOOK_LINK_CHECK === "1") return;

  const broken = await findBrokenInternalMarkdownLinks();
  if (broken.length === 0) return;

  const lines = broken.map(
    (b) =>
      `  • ${b.sourceKey}: "${b.href}" → ${b.resolvedKey} (missing)`,
  );
  throw new Error(
    `Broken internal markdown links (${broken.length}):\n${lines.join("\n")}`,
  );
}
