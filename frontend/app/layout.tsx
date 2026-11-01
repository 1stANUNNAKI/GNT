import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "GitHub Noob Toolkit (GNT) · The Copilot for Vibe Coders",
  description:
    "An automated protective shield and friendly copilot for beginners who build software with AI tools. Catches secret leaks, fixes merge conflicts, and explains git diffs without jargon.",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-cyber-base text-cyber-text min-h-screen selection:bg-brand selection:text-white antialiased">
        {children}
      </body>
    </html>
  );
}
