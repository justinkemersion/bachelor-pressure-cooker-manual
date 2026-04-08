import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { AppSidebar } from "@/components/app-sidebar";
import { MobileSidebarNav } from "@/components/mobile-sidebar";
import { getAllContent } from "@/lib/content";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Bachelor Cookbook",
  description: "Pressure-cooker docs, techniques, and recipes.",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const allContent = await getAllContent();

  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full bg-slate-950 antialiased text-zinc-100`}
    >
      <body className="min-h-full bg-slate-950 font-sans text-zinc-100">
        <div className="flex min-h-screen">
          <AppSidebar items={allContent} />
          <div className="flex min-h-screen flex-1 flex-col md:ml-64">
            <MobileSidebarNav items={allContent} />
            <div className="flex flex-1 flex-col">{children}</div>
          </div>
        </div>
      </body>
    </html>
  );
}
