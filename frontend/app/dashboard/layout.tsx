"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  ShieldCheck,
  LayoutDashboard,
  GitBranch,
  ShieldAlert,
  Boxes,
  Terminal,
  Settings,
  Sparkles,
  ToggleLeft,
  ToggleRight,
  ExternalLink,
  Github,
  Zap,
} from "lucide-react";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [noJargonMode, setNoJargonMode] = useState(true);

  const navItems = [
    { label: "Overview", href: "/dashboard", icon: LayoutDashboard },
    { label: "Repositories", href: "/dashboard/repos", icon: GitBranch },
    { label: "Secret Shield", href: "/dashboard/repos/default?tab=secrets", icon: ShieldAlert },
    { label: "Conflict Solver", href: "/dashboard/repos/default?tab=conflicts", icon: Sparkles },
    { label: "DepDoctor", href: "/dashboard/repos/default?tab=deps", icon: Boxes },
    { label: "MCP & Settings", href: "/dashboard/settings", icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-cyber-base flex flex-col md:flex-row text-cyber-text">
      {/* Sidebar */}
      <aside className="w-full md:w-64 border-r border-cyber-border bg-cyber-surface/60 p-4 flex flex-col justify-between shrink-0">
        <div>
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 mb-8 px-2">
            <div className="p-2 rounded-lg bg-brand/10 border border-brand/40 text-brand shadow-neo-brand">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <div className="font-extrabold text-sm text-cyber-bright tracking-tight">GNT Dashboard</div>
              <div className="text-[10px] text-cyber-muted font-mono">Shielding Vibe Coders</div>
            </div>
          </Link>

          {/* Navigation Links */}
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.label}
                  href={item.href}
                  className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-semibold transition-all ${
                    isActive
                      ? "bg-brand text-white shadow-neo-brand"
                      : "text-cyber-muted hover:text-cyber-bright hover:bg-cyber-surface2"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Sidebar Footer: Plan Badge & GitHub App Link */}
        <div className="pt-4 border-t border-cyber-border space-y-3">
          <div className="p-3 rounded-lg bg-cyber-base border border-cyber-border flex items-center justify-between">
            <div>
              <div className="text-[10px] uppercase font-bold text-cyber-muted tracking-wider">Active Plan</div>
              <div className="text-xs font-bold text-brand flex items-center gap-1">
                <Zap className="w-3 h-3" /> Vibe Pro Plan
              </div>
            </div>
            <Link
              href="/pricing"
              className="text-[10px] text-cyber-muted hover:text-cyber-bright underline"
            >
              Manage
            </Link>
          </div>

          <a
            href="https://github.com"
            target="_blank"
            rel="noreferrer"
            className="flex items-center justify-center gap-1.5 w-full py-2 px-3 rounded-lg text-xs font-medium bg-cyber-surface2 hover:bg-cyber-border text-cyber-bright border border-cyber-border transition-colors"
          >
            <Github className="w-3.5 h-3.5" />
            Install GitHub Bot
            <ExternalLink className="w-3 h-3 ml-0.5" />
          </a>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header Bar with No-Jargon Toggle */}
        <header className="h-16 border-b border-cyber-border bg-cyber-surface/40 px-6 flex items-center justify-between backdrop-blur-sm">
          <div className="flex items-center gap-3">
            <span className="text-xs text-cyber-muted hidden sm:inline">Workspace:</span>
            <span className="text-xs font-mono font-bold text-cyber-bright px-2.5 py-1 rounded bg-cyber-base border border-cyber-border">
              vibe-coder-app / main
            </span>
          </div>

          <div className="flex items-center gap-4">
            {/* No-Jargon Mode Toggle */}
            <button
              onClick={() => setNoJargonMode(!noJargonMode)}
              className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-brand/40 bg-brand/10 hover:bg-brand/20 text-xs font-semibold text-brand transition-colors shadow-neo-brand"
            >
              {noJargonMode ? (
                <ToggleRight className="w-4 h-4 text-brand" />
              ) : (
                <ToggleLeft className="w-4 h-4 text-cyber-muted" />
              )}
              <span>No-Jargon Mode: {noJargonMode ? "ON" : "OFF"}</span>
            </button>

            {/* User Avatar */}
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-cyber-surface2 border border-cyber-border flex items-center justify-center font-bold text-xs text-brand font-mono">
                VC
              </div>
            </div>
          </div>
        </header>

        {/* Child Pages */}
        <main className="flex-1 p-6 lg:p-8 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
