import Link from "next/link";
import {
  contentHref,
  groupContentByCategory,
  type ContentCategory,
  type ContentItem,
} from "@/lib/content";

const CATEGORY_ORDER: ContentCategory[] = [
  "fundamentals",
  "techniques",
  "recipes",
  "reference",
];

const CATEGORY_LABEL: Record<ContentCategory, string> = {
  fundamentals: "Fundamentals",
  techniques: "Techniques",
  recipes: "Recipes",
  reference: "Reference",
};

export function AppSidebar({ items }: { items: ContentItem[] }) {
  const grouped = groupContentByCategory(items);

  return (
    <aside className="fixed inset-y-0 left-0 z-40 hidden w-64 flex-col border-r border-slate-800 bg-slate-950 md:flex">
      <div className="border-b border-slate-800 px-4 py-5">
        <Link
          href="/"
          className="text-sm font-semibold tracking-tight text-zinc-100 transition-colors hover:text-white"
        >
          Bachelor Cookbook
        </Link>
        <p className="mt-1 text-xs text-slate-500">Docs & recipes</p>
      </div>
      <nav className="flex-1 overflow-y-auto px-3 py-4">
        {CATEGORY_ORDER.map((cat) => {
          const list = grouped[cat];
          if (list.length === 0) return null;
          return (
            <div key={cat} className="mb-6 last:mb-0">
              <h2 className="mb-2 px-1 text-xs font-medium uppercase tracking-wider text-slate-500">
                {CATEGORY_LABEL[cat]}
              </h2>
              <ul className="space-y-0.5">
                {list.map((item) => (
                  <li key={`${item.category}/${item.slug}`}>
                    <Link
                      href={contentHref(item)}
                      className="block rounded-md px-2 py-1.5 text-sm text-slate-300 transition-colors hover:bg-slate-900 hover:text-white"
                    >
                      {item.title}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
      </nav>
    </aside>
  );
}
