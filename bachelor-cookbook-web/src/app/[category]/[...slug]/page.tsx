import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { MarkdownBlock } from "@/components/markdown-block";
import {
  getAllContent,
  getContentBySlug,
  isContentCategory,
  type ContentItem,
} from "@/lib/content";

type Props = {
  params: Promise<{ category: string; slug: string[] }>;
};

function slugPathFromParams(slugParts: string[]): string {
  return slugParts.map((s) => decodeURIComponent(s)).join("/");
}

function stripLeadingH1(md: string): string {
  return md.replace(/^#\s+[^\n]+\n+/, "");
}

function MetaBadges({ item }: { item: ContentItem }) {
  const { metadata } = item;
  const items: { label: string; value: string }[] = [];
  if (metadata.mission) items.push({ label: "Mission", value: metadata.mission });
  if (metadata.protein) items.push({ label: "Protein", value: metadata.protein });
  if (metadata.timeBucket) items.push({ label: "Time", value: metadata.timeBucket });
  if (metadata.effort) items.push({ label: "Effort", value: metadata.effort });
  if (metadata.heat) items.push({ label: "Heat", value: metadata.heat });

  if (items.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-2 border-b border-zinc-800 pb-6">
      {items.map((entry) => (
        <span
          key={entry.label}
          className="rounded-full bg-slate-800 px-2 py-1 text-xs text-slate-300"
        >
          {entry.label}: {entry.value}
        </span>
      ))}
    </div>
  );
}

export async function generateStaticParams(): Promise<
  { category: string; slug: string[] }[]
> {
  const all = await getAllContent();
  return all.map((item) => ({
    category: item.category,
    slug: item.slug.split("/").filter(Boolean),
  }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { category, slug } = await params;
  if (!isContentCategory(category)) return { title: "Cookbook" };
  const path = slugPathFromParams(slug);
  const item = await getContentBySlug(category, path);
  if (!item) return { title: "Not found" };
  return {
    title: `${item.title} · Bachelor Cookbook`,
    description: item.metadata.mission ?? item.title,
  };
}

export default async function DocPage({ params }: Props) {
  const { category, slug } = await params;
  if (!isContentCategory(category)) notFound();

  const path = slugPathFromParams(slug);
  const item = await getContentBySlug(category, path);

  if (!item) notFound();

  const isRecipe = item.category === "recipes";
  const hasSections = item.ingredients ?? item.instructions;
  const twoCol =
    isRecipe &&
    Boolean(item.ingredients) &&
    Boolean(item.instructions);

  const bodyForGeneric = stripLeadingH1(item.raw);

  return (
    <div className="min-h-full flex-1 bg-slate-950">
      <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 md:py-10">
        <Link
          href="/"
          className="mb-6 inline-block text-sm text-zinc-500 transition-colors hover:text-zinc-300"
        >
          ← Home
        </Link>
        <header className="mb-8 space-y-4">
          <h1 className="text-3xl font-semibold tracking-tight text-zinc-50 sm:text-4xl">
            {item.title}
          </h1>
          <MetaBadges item={item} />
        </header>

        {isRecipe && hasSections ? (
          <div
            className={
              twoCol
                ? "grid gap-10 lg:grid-cols-2 lg:gap-12 lg:items-start"
                : "max-w-3xl space-y-10"
            }
          >
            {item.ingredients ? (
              <section className="space-y-3">
                <h2 className="text-xs font-semibold uppercase tracking-wider text-zinc-500">
                  Ingredients
                </h2>
                <MarkdownBlock content={item.ingredients} />
              </section>
            ) : null}
            {item.instructions ? (
              <section className="space-y-3">
                <h2 className="text-xs font-semibold uppercase tracking-wider text-zinc-500">
                  Instructions
                </h2>
                <MarkdownBlock content={item.instructions} />
              </section>
            ) : null}
          </div>
        ) : null}

        {isRecipe && !hasSections ? (
          <section className="space-y-3">
            <MarkdownBlock content={bodyForGeneric} />
          </section>
        ) : null}

        {!isRecipe ? (
          <div className="prose-headings:scroll-mt-20">
            <MarkdownBlock content={bodyForGeneric} />
          </div>
        ) : null}
      </div>
    </div>
  );
}
