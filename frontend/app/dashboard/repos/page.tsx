"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  GitBranch,
  ShieldCheck,
  ShieldAlert,
  AlertTriangle,
  Plus,
  Search,
  ArrowRight,
  Filter,
  ExternalLink,
} from "lucide-react";

export default function RepositoriesListPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [filterStatus, setFilterStatus] = useState<string>("all");

  const repos = [
    {
      id: "default",
      name: "vibe-coder-app",
      owner: "vibe-coder",
      branch: "main",
      score: 94,
      status: "Safe",
      badgeClass: "bg-safe/10 text-safe border-safe/30",
      icon: ShieldCheck,
      issuesCount: 0,
      lastAudit: "Just now",
      description: "Next.js 14 AI app with Stripe subscriptions and Tailwind CSS.",
    },
    {
      id: "agent-service",
      name: "ai-agent-service",
      owner: "vibe-coder",
      branch: "feature/openai-v2",
      score: 45,
      status: "Critical Leak",
      badgeClass: "bg-critical/10 text-critical border-critical/30",
      icon: ShieldAlert,
      issuesCount: 1,
      lastAudit: "12 mins ago",
      description: "Python FastAPI autonomous agent backend with OpenAI integration.",
    },
    {
      id: "portfolio",
      name: "nextjs-portfolio",
      owner: "vibe-coder",
      branch: "main",
      score: 80,
      status: "Missing README",
      badgeClass: "bg-warning/10 text-warning border-warning/30",
      icon: AlertTriangle,
      issuesCount: 1,
      lastAudit: "1 hour ago",
      description: "Personal developer portfolio and creative showcase.",
    },
  ];

  const filteredRepos = repos.filter((r) => {
    const matchesSearch = r.name.toLowerCase().includes(searchTerm.toLowerCase());
    if (filterStatus === "safe") return matchesSearch && r.status === "Safe";
    if (filterStatus === "issues") return matchesSearch && r.status !== "Safe";
    return matchesSearch;
  });

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-cyber-bright tracking-tight">Connected Repositories</h1>
          <p className="text-xs sm:text-sm text-cyber-muted mt-0.5">
            Manage repositories shielded by GitHub Noob Toolkit (GNT).
          </p>
        </div>

        <a
          href="https://github.com"
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-brand hover:bg-brand-hover text-white text-xs font-bold shadow-neo-brand transition-all self-start sm:self-auto"
        >
          <Plus className="w-3.5 h-3.5" />
          Connect New Repo
        </a>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row items-center gap-3 bg-cyber-surface p-3 rounded-xl border border-cyber-border shadow-neo-sm">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-cyber-muted absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search repositories by name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-cyber-base border border-cyber-border rounded-lg pl-9 pr-3 py-1.5 text-xs text-cyber-bright placeholder-cyber-muted focus:outline-none focus:border-brand"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <button
            onClick={() => setFilterStatus("all")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
              filterStatus === "all"
                ? "bg-brand/10 border-brand text-brand"
                : "bg-cyber-base border-cyber-border text-cyber-muted hover:text-cyber-bright"
            }`}
          >
            All (3)
          </button>
          <button
            onClick={() => setFilterStatus("safe")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
              filterStatus === "safe"
                ? "bg-safe/10 border-safe text-safe"
                : "bg-cyber-base border-cyber-border text-cyber-muted hover:text-cyber-bright"
            }`}
          >
            Safe (1)
          </button>
          <button
            onClick={() => setFilterStatus("issues")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
              filterStatus === "issues"
                ? "bg-critical/10 border-critical text-critical"
                : "bg-cyber-base border-cyber-border text-cyber-muted hover:text-cyber-bright"
            }`}
          >
            Alerts (2)
          </button>
        </div>
      </div>

      {/* Repositories Cards List */}
      <div className="space-y-4">
        {filteredRepos.map((repo) => {
          const Icon = repo.icon;
          return (
            <div
              key={repo.id}
              className="p-5 rounded-xl bg-cyber-surface border border-cyber-border shadow-neo hover:border-brand/40 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4"
            >
              <div className="space-y-1.5">
                <div className="flex items-center gap-2.5">
                  <span className="font-mono text-sm font-bold text-cyber-bright flex items-center gap-1.5">
                    <GitBranch className="w-4 h-4 text-brand" />
                    {repo.owner}/{repo.name}
                  </span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${repo.badgeClass}`}>
                    {repo.status}
                  </span>
                </div>
                <p className="text-xs text-cyber-muted">{repo.description}</p>
                <div className="flex items-center gap-3 text-[11px] font-mono text-cyber-muted pt-1">
                  <span>branch: <strong className="text-cyber-bright">{repo.branch}</strong></span>
                  <span>•</span>
                  <span>last audited: {repo.lastAudit}</span>
                </div>
              </div>

              <div className="flex items-center gap-4 self-end sm:self-center shrink-0">
                <div className="text-right">
                  <div className="text-xs text-cyber-muted">Vibe Health</div>
                  <div className="text-base font-black font-mono text-cyber-bright">{repo.score}/100</div>
                </div>

                <Link
                  href={`/dashboard/repos/${repo.id}`}
                  className="flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-cyber-surface2 hover:bg-brand hover:text-white border border-cyber-border text-cyber-bright text-xs font-semibold transition-all shadow-neo-sm"
                >
                  View Shield Details
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
