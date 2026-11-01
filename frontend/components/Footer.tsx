import Link from "next/link";
import { ShieldCheck, Heart } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-cyber-border bg-cyber-surface/50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6 text-sm text-cyber-muted">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-brand" />
          <span className="font-semibold text-cyber-bright">GitHub Noob Toolkit</span>
          <span>— Zero Shame. Zero Leaks. Pure Vibe.</span>
        </div>

        <div className="flex items-center gap-6">
          <Link href="/pricing" className="hover:text-cyber-bright transition-colors">Pricing</Link>
          <Link href="/dashboard" className="hover:text-cyber-bright transition-colors">Dashboard</Link>
          <a href="https://github.com" target="_blank" rel="noreferrer" className="hover:text-cyber-bright transition-colors">GitHub Marketplace</a>
        </div>

        <div className="flex items-center gap-1.5 text-xs">
          Built with <Heart className="w-3.5 h-3.5 text-critical fill-critical" /> for non-traditional developers & AI coders.
        </div>
      </div>
    </footer>
  );
}
