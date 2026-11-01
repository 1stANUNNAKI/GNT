"use client";

import React, { useState } from "react";
import Link from "next/link";
import { VibeGauge } from "@/components/VibeGauge";
import {
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  GitBranch,
  BookOpen,
  Boxes,
  ArrowRight,
  ExternalLink,
  Plus,
  RefreshCw,
  AlertTriangle,
} from "lucide-react";

export default function DashboardOverviewPage() {
  const [healthScore, setHealthScore] = useState(94);
  const [isScanning, setIsScanning] = useState(false);

  const repos = [
    {
      id: "repo-1",
      name: "vibe-coder-app",
      branch: "main",
      score: 94,
      status: "Safe",
      badgeClass: "bg-safe/10 text-safe border-safe/30",
      icon: ShieldCheck,
      lastAudit: "Just now",
      summary: "Clean! No secret leaks or merge conflicts.",
    },
    {
      id: "repo-2",
      name: "ai-agent-service",
      branch: "feature/openai-v2",
      score: 45,
      status: "Critical Leak",
      badgeClass: "bg-critical/10 text-critical border-critical/30",
      icon: ShieldAlert,
      lastAudit: "12 mins ago",
      summary: "OpenAI secret key committed in `agent.py` line 14.",
    },
    {
      id: "repo-3",
      name: "nextjs-portfolio",
      branch: "main",
      score: 80,
      status: "Missing README",
      badgeClass: "bg-warning/10 text-warning border-warning/30",
      icon: AlertTriangle,
      lastAudit: "1 hour ago",
      summary: "No setup instructions found. Auto-generate with 1-click.",
    },
  ];

  const handleQuickScan = () => {
    setIsScanning(true);
    setTimeout(() => {
      setIsScanning(false);
      setHealthScore(98);
    }, 800);
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Top Banner: Vibe Health Score & Welcome */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Status & Quick Actions */}
        <div className="lg:col-span-2 p-6 sm:p-8 rounded-2xl bg-cyber-surface border border-cyber-border shadow-neo flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="px-3 py-1 rounded-full bg-brand/10 border border-brand/30 text-brand text-xs font-semibold uppercase tracking-wider flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5" />
                Repository Shield Status
              </span>
              <button
                onClick={handleQuickScan}
                disabled={isScanning}
                className="flex items-center gap-1.5 text-xs text-cyber-muted hover:text-cyber-bright transition-colors"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${isScanning ? "animate-spin text-brand" : ""}`} />
                {isScanning ? "Scanning..." : "Re-scan all"}
              </button>
            </div>

            <h1 className="text-2xl sm:text-3xl font-extrabold text-cyber-bright tracking-tight">
              Looking sharp! Your projects are protected.
            </h1>
            <p className="mt-2 text-xs sm:text-sm text-cyber-muted leading-relaxed max-w-xl">
              GitHub Noob Toolkit is continuously monitoring your Git commits and Pull Requests.
              No exposed credentials detected on your primary branch.
            </p>
          </div>

          {/* Quick Action Buttons */}
          <div className="mt-8 pt-6 border-t border-cyber-border grid grid-cols-2 sm:grid-cols-3 gap-3">
            <Link
              href="/dashboard/repos/default?tab=secrets"
              className="p-3 rounded-xl bg-cyber-base border border-cyber-border hover:border-brand/40 text-left transition-all hover:bg-cyber-surface2 shadow-neo-sm"
            >
              <ShieldAlert className="w-4 h-4 text-critical mb-1.5" />
              <div className="text-xs font-bold text-cyber-bright">Scan for Leaks</div>
              <div className="text-[11px] text-cyber-muted">Inspect files & diffs</div>
            </Link>

            <Link
              href="/dashboard/repos/default?tab=conflicts"
              className="p-3 rounded-xl bg-cyber-base border border-cyber-border hover:border-brand/40 text-left transition-all hover:bg-cyber-surface2 shadow-neo-sm"
            >
              <GitBranch className="w-4 h-4 text-safe mb-1.5" />
              <div className="text-xs font-bold text-cyber-bright">Solve Conflicts</div>
              <div className="text-[11px] text-cyber-muted">1-Click hybrid merge</div>
            </Link>

            <Link
              href="/dashboard/repos/default?tab=docgen"
              className="p-3 rounded-xl bg-cyber-base border border-cyber-border hover:border-brand/40 text-left transition-all hover:bg-cyber-surface2 shadow-neo-sm col-span-2 sm:col-span-1"
            >
              <BookOpen className="w-4 h-4 text-brand mb-1.5" />
              <div className="text-xs font-bold text-cyber-bright">Generate README</div>
              <div className="text-[11px] text-cyber-muted">3-step setup guide</div>
            </Link>
          </div>
        </div>

        {/* Right Col: Animated Vibe Gauge */}
        <div className="p-6 rounded-2xl bg-cyber-surface border border-cyber-border shadow-neo flex flex-col items-center justify-center text-center">
          <div className="text-xs font-bold uppercase tracking-wider text-cyber-muted mb-2">
            Overall Vibe Health
          </div>
          <VibeGauge score={healthScore} size={170} strokeWidth={14} />
          <p className="mt-2 text-xs text-cyber-muted max-w-[200px]">
            Based on active secret scans, .gitignore enforcement, and PR checks.
          </p>
        </div>
      </div>

      {/* Connected Repositories Section */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-cyber-bright tracking-tight">Connected Repositories</h2>
          <a
            href="https://github.com"
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-brand text-white hover:bg-brand-hover transition-colors shadow-neo-brand"
          >
            <Plus className="w-3.5 h-3.5" /> Connect Repo
          </a>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {repos.map((repo) => {
            const Icon = repo.icon;
            return (
              <div
                key={repo.id}
                className="p-5 rounded-xl bg-cyber-surface border border-cyber-border shadow-neo hover:border-brand/40 transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-mono text-xs font-bold text-cyber-bright flex items-center gap-1.5">
                      <GitBranch className="w-3.5 h-3.5 text-brand" /> {repo.name}
                    </span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${repo.badgeClass}`}>
                      {repo.status}
                    </span>
                  </div>

                  <div className="text-xs text-cyber-muted font-mono mb-2">
                    branch: <span className="text-cyber-bright">{repo.branch}</span> • {repo.lastAudit}
                  </div>

                  <p className="text-xs text-cyber-muted leading-relaxed">
                    {repo.summary}
                  </p>
                </div>

                <div className="mt-6 pt-4 border-t border-cyber-border flex items-center justify-between">
                  <div className="flex items-center gap-1.5">
                    <span className="text-xs font-bold font-mono text-cyber-bright">
                      {repo.score}/100
                    </span>
                  </div>
                  <Link
                    href={`/dashboard/repos/${repo.id}`}
                    className="flex items-center gap-1 text-xs font-semibold text-brand hover:underline"
                  >
                    View Shield Details <ArrowRight className="w-3 h-3" />
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Recent Bot Checks Activity */}
      <div className="p-6 rounded-2xl bg-cyber-surface border border-cyber-border shadow-neo">
        <h2 className="text-lg font-bold text-cyber-bright tracking-tight mb-4">
          Recent GitHub App Activity & Pull Request Reviews
        </h2>

        <div className="divide-y divide-cyber-border text-xs">
          <div className="py-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-safe/10 text-safe border border-safe/30">
                <ShieldCheck className="w-4 h-4" />
              </div>
              <div>
                <div className="font-bold text-cyber-bright">
                  PR #14: Add Stripe checkout webhooks • <span className="text-safe">Passed (Checks API)</span>
                </div>
                <div className="text-cyber-muted font-mono text-[11px]">
                  vibe-coder-app • SHA: `98bf01a` • VibeLog changelog posted
                </div>
              </div>
            </div>
            <span className="text-cyber-muted text-[11px] self-end sm:self-center">15m ago</span>
          </div>

          <div className="py-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-critical/10 text-critical border border-critical/30">
                <ShieldAlert className="w-4 h-4" />
              </div>
              <div>
                <div className="font-bold text-cyber-bright">
                  PR #3: Integrate Claude API model • <span className="text-critical">Blocked (Secret Intercepted)</span>
                </div>
                <div className="text-cyber-muted font-mono text-[11px]">
                  ai-agent-service • Leaked `sk-ant-***` prevented from merge
                </div>
              </div>
            </div>
            <span className="text-cyber-muted text-[11px] self-end sm:self-center">2h ago</span>
          </div>
        </div>
      </div>
    </div>
  );
}
