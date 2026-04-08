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

/** Collapsible nav for small screens when the fixed sidebar is hidden */
export function MobileSidebarNav({ items }: { items: ContentItem[] }) {
  const grouped = groupContentByCategory(items);

  return (
    <details className="relative z-50 border-b border-slate-800 bg-slate-950 md:hidden">
      <summary className="cursor-pointer list-none px-4 py-3 text-sm font-medium text-zinc-200 [&::-webkit-details-marker]:hidden">
        <span className="select-none">Browse</span>
      </summary>
      <div className="max-h-[min(70vh,28rem)] overflow-y-auto border-t border-slate-800 px-3 py-3">
        {CATEGORY_ORDER.map((cat) => {
          const list = grouped[cat];
          if (list.length === 0) return null;
          return (
            <div key={cat} className="mb-4 last:mb-0">
              <h2 className="mb-1.5 px-1 text-xs font-medium uppercase tracking-wider text-slate-500">
                {CATEGORY_LABEL[cat]}
              </h2>
              <ul className="space-y-0.5">
                {list.map((item) => (
                  <li key={`${item.category}/${item.slug}`}>
                    <Link
                      href={contentHref(item)}
                      className="block rounded-md px-2 py-1.5 text-sm text-slate-300 hover:bg-slate-900 hover:text-white"
                    >
                      {item.title}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
      </div>
    </details>
  );
}
