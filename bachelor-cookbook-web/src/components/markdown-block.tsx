import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { transformMarkdownLinks } from "@/lib/content";

const prose =
  "prose prose-invert prose-zinc prose-sm max-w-none prose-headings:scroll-mt-20 prose-p:leading-relaxed prose-li:marker:text-zinc-500 prose-a:text-sky-400 prose-a:underline-offset-2 hover:prose-a:text-sky-300";

export function MarkdownBlock({ content }: { content: string }) {
  const body = transformMarkdownLinks(content);
  return (
    <div className={prose}>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{body}</ReactMarkdown>
    </div>
  );
}
