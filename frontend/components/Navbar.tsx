"use client";

import Link from "next/link";
import { ShieldCheck, Sparkles, Terminal, Github } from "lucide-react";

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-cyber-border bg-cyber-base/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link href="/" className="flex items-center gap-2 group">
          <div className="p-2 rounded-lg bg-brand/10 border border-brand/40 text-brand group-hover:scale-105 transition-transform shadow-neo-brand">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <span className="font-bold text-lg text-cyber-bright tracking-tight">
            GitHub <span className="text-brand">Noob Toolkit</span>
          </span>
          <span className="text-xs px-2 py-0.5 rounded-full bg-cyber-surface2 border border-cyber-border text-cyber-muted font-mono">
            v1.0
          </span>
        </Link>

        <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-cyber-muted">
          <a href="#features" className="hover:text-cyber-bright transition-colors">Features</a>
          <a href="#playground" className="hover:text-cyber-bright transition-colors">Live Playground</a>
          <Link href="/pricing" className="hover:text-cyber-bright transition-colors">Pricing</Link>
          <a href="#mcp" className="hover:text-cyber-bright transition-colors flex items-center gap-1">
            <Terminal className="w-3.5 h-3.5 text-brand" /> MCP Tools
          </a>
        </nav>

        <div className="flex items-center gap-3">
          <a
            href="https://github.com"
            target="_blank"
            rel="noreferrer"
            className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-medium border border-cyber-border bg-cyber-surface hover:bg-cyber-surface2 text-cyber-bright transition-colors"
          >
            <Github className="w-4 h-4" />
            GitHub App
          </a>
          <Link
            href="/dashboard"
            className="flex items-center gap-1.5 px-4 py-2 rounded-md text-xs font-semibold bg-brand text-white hover:bg-brand-hover shadow-neo-brand transition-all active:translate-x-0.5 active:translate-y-0.5"
          >
            <Sparkles className="w-3.5 h-3.5" />
            Launch Dashboard
          </Link>
        </div>
      </div>
    </header>
  );
}
