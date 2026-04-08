import Link from "next/link";
import {
  contentHref,
  getFundamentals,
  getLatestRecipes,
} from "@/lib/content";

function DashboardCard({
  title,
  subtitle,
  href,
}: {
  title: string;
  subtitle?: string;
  href: string;
}) {
  return (
    <Link
      href={href}
      className="group block rounded-lg border border-zinc-800 bg-slate-950/90 p-4 shadow-sm ring-1 ring-zinc-800/60 transition-colors hover:border-slate-500 hover:ring-slate-600/50"
    >
      <h3 className="font-semibold tracking-tight text-zinc-50 group-hover:text-white">
        {title}
      </h3>
      {subtitle ? (
        <p className="mt-1 line-clamp-2 text-sm text-slate-500">{subtitle}</p>
      ) : null}
    </Link>
  );
}

export default async function Home() {
  const [fundamentals, latestRecipes] = await Promise.all([
    getFundamentals(),
    getLatestRecipes(8),
  ]);

  return (
    <div className="min-h-full flex-1 bg-slate-950">
      <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6">
        <header className="mb-10 border-b border-zinc-800 pb-8">
          <h1 className="text-3xl font-semibold tracking-tight text-zinc-50">
            Bachelor Cookbook
          </h1>
          <p className="mt-2 max-w-2xl text-slate-400">
            Fundamentals, techniques, recipes, and reference — one place.
          </p>
        </header>

        <section className="mb-12">
          <h2 className="mb-4 text-xs font-semibold uppercase tracking-wider text-slate-500">
            Fundamentals
          </h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {fundamentals.map((item) => (
              <DashboardCard
                key={`${item.category}/${item.slug}`}
                title={item.title}
                href={contentHref(item)}
              />
            ))}
          </div>
        </section>

        <section>
          <h2 className="mb-4 text-xs font-semibold uppercase tracking-wider text-slate-500">
            Latest recipes
          </h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {latestRecipes.map((item) => (
              <DashboardCard
                key={`${item.category}/${item.slug}`}
                title={item.title}
                subtitle={
                  [item.metadata.timeBucket, item.metadata.effort]
                    .filter(Boolean)
                    .join(" · ") || undefined
                }
                href={contentHref(item)}
              />
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
