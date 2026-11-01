"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  ShieldAlert,
  ShieldCheck,
  GitBranch,
  GitMerge,
  BookOpen,
  Boxes,
  Sparkles,
  ArrowLeft,
  Copy,
  Check,
  Wand2,
  FileCode,
  AlertTriangle,
} from "lucide-react";

export default function RepositoryDetailPage({ params }: { params: { id: string } }) {
  const [activeTab, setActiveTab] = useState<"secrets" | "conflicts" | "deps" | "docgen" | "vibelog">("secrets");
  const [copied, setCopied] = useState(false);
  const [secretsFixed, setSecretsFixed] = useState(false);
  const [conflictResolved, setConflictResolved] = useState(false);
  const [depsPatched, setDepsPatched] = useState(false);

  const sampleReadme = `# 🚀 Vibe Coder Web App

> Built with passion, AI tools, and clean code.  
> **Type:** \`Next.js Web Application\` • **Language:** \`TypeScript / React\` • **Manager:** \`npm\`

---

## ⚡ Quickstart Guide (Run in 3 Steps)

### 1. Clone the repository
\`\`\`bash
git clone https://github.com/vibe-coder/vibe-coder-app.git
cd vibe-coder-app
\`\`\`

### 2. Install Dependencies
\`\`\`bash
npm install
\`\`\`

### 3. Launch Development Server
\`\`\`bash
npm run dev
\`\`\`

Open [http://localhost:3000](http://localhost:3000) to view your app!

---

*Generated with ❤️ by GitHub Noob Toolkit (GNT)*`;

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-cyber-muted hover:text-cyber-bright mb-2 transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" /> Back to Dashboard
          </Link>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-black text-cyber-bright font-mono">
              vibe-coder-app
            </h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-brand/10 text-brand border border-brand/30">
              main branch
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="px-3 py-1.5 rounded-lg bg-cyber-surface border border-cyber-border text-xs font-mono">
            Vibe Health: <span className="font-bold text-safe">94/100</span>
          </div>
        </div>
      </div>

      {/* Tabs Bar */}
      <div className="flex border-b border-cyber-border overflow-x-auto space-x-2">
        <button
          onClick={() => setActiveTab("secrets")}
          className={`flex items-center gap-2 px-4 py-3 text-xs sm:text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
            activeTab === "secrets"
              ? "border-brand text-brand bg-brand/5"
              : "border-transparent text-cyber-muted hover:text-cyber-bright"
          }`}
        >
          <ShieldAlert className="w-4 h-4 text-critical" />
          1. Secret Leak Shield
        </button>

        <button
          onClick={() => setActiveTab("conflicts")}
          className={`flex items-center gap-2 px-4 py-3 text-xs sm:text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
            activeTab === "conflicts"
              ? "border-brand text-brand bg-brand/5"
              : "border-transparent text-cyber-muted hover:text-cyber-bright"
          }`}
        >
          <GitMerge className="w-4 h-4 text-safe" />
          2. Conflict Solver
        </button>

        <button
          onClick={() => setActiveTab("deps")}
          className={`flex items-center gap-2 px-4 py-3 text-xs sm:text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
            activeTab === "deps"
              ? "border-brand text-brand bg-brand/5"
              : "border-transparent text-cyber-muted hover:text-cyber-bright"
          }`}
        >
          <Boxes className="w-4 h-4 text-purple-400" />
          3. DepDoctor (AST)
        </button>

        <button
          onClick={() => setActiveTab("docgen")}
          className={`flex items-center gap-2 px-4 py-3 text-xs sm:text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
            activeTab === "docgen"
              ? "border-brand text-brand bg-brand/5"
              : "border-transparent text-cyber-muted hover:text-cyber-bright"
          }`}
        >
          <BookOpen className="w-4 h-4 text-brand" />
          4. Auto-README
        </button>

        <button
          onClick={() => setActiveTab("vibelog")}
          className={`flex items-center gap-2 px-4 py-3 text-xs sm:text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
            activeTab === "vibelog"
              ? "border-brand text-brand bg-brand/5"
              : "border-transparent text-cyber-muted hover:text-cyber-bright"
          }`}
        >
          <Sparkles className="w-4 h-4 text-warning" />
          5. VibeLog (Changelog)
        </button>
      </div>

      {/* Tab 1: Secret Leak Shield */}
      {activeTab === "secrets" && (
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-cyber-surface border border-cyber-border flex items-center justify-between">
            <div>
              <h2 className="text-sm font-bold text-cyber-bright">Active Secret Interception Alerts</h2>
              <p className="text-xs text-cyber-muted mt-0.5">
                GNT monitors pull requests and prevents dangerous keys from being merged publicly.
              </p>
            </div>
            {!secretsFixed && (
              <button
                onClick={() => setSecretsFixed(true)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-safe hover:bg-emerald-600 text-white font-semibold text-xs shadow-neo-safe transition-colors"
              >
                <Wand2 className="w-3.5 h-3.5" /> 1-Click Fix All
              </button>
            )}
          </div>

          {!secretsFixed ? (
            <div className="p-5 rounded-xl bg-cyber-surface border border-critical/40 shadow-neo">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-critical text-white">
                    CRITICAL
                  </span>
                  <span className="font-bold text-sm text-cyber-bright">OpenAI Secret API Key Detected</span>
                </div>
                <span className="font-mono text-xs text-cyber-muted">server/ai_agent.py : Line 14</span>
              </div>

              <div className="p-3 rounded-lg bg-cyber-base border border-cyber-border font-mono text-xs text-cyber-bright mb-3 overflow-x-auto">
                <span className="text-cyber-muted">14 |</span> OPENAI_API_KEY = &quot;<span className="text-critical font-bold">sk-proj-999a******************9000</span>&quot;
              </div>

              <p className="text-xs text-cyber-muted leading-relaxed">
                <strong className="text-cyber-bright">Why this matters:</strong> If someone forks or clones your repo, they can spend your OpenAI credits.
              </p>

              <div className="mt-4 pt-3 border-t border-cyber-border flex items-center justify-between">
                <span className="text-xs text-cyber-muted">Recommended safe action:</span>
                <button
                  onClick={() => setSecretsFixed(true)}
                  className="px-3 py-1.5 rounded bg-brand hover:bg-brand-hover text-white text-xs font-semibold shadow-neo-brand transition-colors"
                >
                  Move to .env &amp; Add .gitignore Rule 🪄
                </button>
              </div>
            </div>
          ) : (
            <div className="p-8 rounded-xl bg-safe/10 border border-safe/30 text-center space-y-2">
              <ShieldCheck className="w-8 h-8 text-safe mx-auto" />
              <div className="font-bold text-sm text-safe">All Secrets Safely Extracted!</div>
              <p className="text-xs text-cyber-muted">
                Created `.env` entry and added `.env` to `.gitignore`. Code updated to read from `process.env`.
              </p>
            </div>
          )}
        </div>
      )}

      {/* Tab 2: Conflict Solver */}
      {activeTab === "conflicts" && (
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-cyber-surface border border-cyber-border flex items-center justify-between">
            <div>
              <h2 className="text-sm font-bold text-cyber-bright">Merge Conflict Visualizer &amp; Healer</h2>
              <p className="text-xs text-cyber-muted mt-0.5">
                No git command stress. Review conflicting branches side-by-side and merge cleanly.
              </p>
            </div>
          </div>

          {!conflictResolved ? (
            <div className="p-5 rounded-xl bg-cyber-surface border border-cyber-border shadow-neo space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-lg bg-cyber-base border border-cyber-border">
                  <div className="text-xs font-bold text-brand uppercase tracking-wider mb-2">
                    HEAD (Your Current Changes)
                  </div>
                  <pre className="text-xs font-mono text-cyber-bright bg-cyber-surface/50 p-2 rounded">
                    {`import { Button } from '@/components/ui/button';\nimport { Shield } from 'lucide-react';`}
                  </pre>
                </div>

                <div className="p-4 rounded-lg bg-cyber-base border border-cyber-border">
                  <div className="text-xs font-bold text-safe uppercase tracking-wider mb-2">
                    Incoming Branch (Collaborator / AI PR)
                  </div>
                  <pre className="text-xs font-mono text-cyber-bright bg-cyber-surface/50 p-2 rounded">
                    {`import { Tooltip } from '@/components/ui/tooltip';\nimport { Shield, Sparkles } from 'lucide-react';`}
                  </pre>
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-end gap-3 pt-2">
                <button
                  onClick={() => setConflictResolved(true)}
                  className="px-4 py-2 rounded-lg bg-brand hover:bg-brand-hover text-white text-xs font-bold shadow-neo-brand transition-all"
                >
                  Apply Smart Hybrid Merge (Deduplicated) ✨
                </button>
              </div>
            </div>
          ) : (
            <div className="p-8 rounded-xl bg-safe/10 border border-safe/30 text-center space-y-2">
              <ShieldCheck className="w-8 h-8 text-safe mx-auto" />
              <div className="font-bold text-sm text-safe">Conflict Successfully Resolved!</div>
              <p className="text-xs text-cyber-muted">
                Merged all imports into a single clean list without duplicates. No conflict markers left behind.
              </p>
            </div>
          )}
        </div>
      )}

      {/* Tab 3: DepDoctor */}
      {activeTab === "deps" && (
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-cyber-surface border border-cyber-border flex items-center justify-between">
            <div>
              <h2 className="text-sm font-bold text-cyber-bright">DepDoctor (AST Dependency Audit)</h2>
              <p className="text-xs text-cyber-muted mt-0.5">
                Catches third-party libraries used in your code that you forgot to add to `package.json`.
              </p>
            </div>
            {!depsPatched && (
              <button
                onClick={() => setDepsPatched(true)}
                className="px-3 py-1.5 rounded-lg bg-brand hover:bg-brand-hover text-white text-xs font-semibold shadow-neo-brand transition-colors"
              >
                Auto-Patch package.json 🪄
              </button>
            )}
          </div>

          {!depsPatched ? (
            <div className="p-5 rounded-xl bg-cyber-surface border border-cyber-border shadow-neo">
              <table className="w-full text-xs text-left">
                <thead>
                  <tr className="border-b border-cyber-border text-cyber-muted uppercase tracking-wider text-[10px]">
                    <th className="pb-3">Library</th>
                    <th className="pb-3">Used In File</th>
                    <th className="pb-3">Status</th>
                    <th className="pb-3 text-right">Fix Command</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-cyber-border">
                  <tr>
                    <td className="py-3 font-mono font-bold text-critical">lucide-react</td>
                    <td className="py-3 font-mono text-cyber-muted">app/dashboard/page.tsx</td>
                    <td className="py-3"><span className="px-2 py-0.5 rounded bg-critical/10 text-critical border border-critical/30 text-[10px]">Missing</span></td>
                    <td className="py-3 text-right font-mono text-brand">npm install lucide-react</td>
                  </tr>
                  <tr>
                    <td className="py-3 font-mono font-bold text-critical">clsx</td>
                    <td className="py-3 font-mono text-cyber-muted">components/Navbar.tsx</td>
                    <td className="py-3"><span className="px-2 py-0.5 rounded bg-critical/10 text-critical border border-critical/30 text-[10px]">Missing</span></td>
                    <td className="py-3 text-right font-mono text-brand">npm install clsx</td>
                  </tr>
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-8 rounded-xl bg-safe/10 border border-safe/30 text-center space-y-2">
              <ShieldCheck className="w-8 h-8 text-safe mx-auto" />
              <div className="font-bold text-sm text-safe">Dependencies Synchronized!</div>
              <p className="text-xs text-cyber-muted">
                Created PR #15 adding `lucide-react` and `clsx` to `package.json`. Deployment will now succeed!
              </p>
            </div>
          )}
        </div>
      )}

      {/* Tab 4: Auto-DocGen */}
      {activeTab === "docgen" && (
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-cyber-surface border border-cyber-border flex items-center justify-between">
            <div>
              <h2 className="text-sm font-bold text-cyber-bright">Auto-Generated README.md</h2>
              <p className="text-xs text-cyber-muted mt-0.5">
                Created automatically from your manifests and project profile. Clear &amp; jargon-free.
              </p>
            </div>
            <button
              onClick={() => copyToClipboard(sampleReadme)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-cyber-surface2 hover:bg-cyber-border text-cyber-bright text-xs font-semibold border border-cyber-border transition-colors shadow-neo-sm"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-safe" /> : <Copy className="w-3.5 h-3.5" />}
              {copied ? "Copied!" : "Copy Markdown"}
            </button>
          </div>

          <div className="p-6 rounded-xl bg-cyber-base border border-cyber-border font-mono text-xs text-cyber-bright shadow-neo whitespace-pre-wrap overflow-x-auto leading-relaxed">
            {sampleReadme}
          </div>
        </div>
      )}

      {/* Tab 5: VibeLog */}
      {activeTab === "vibelog" && (
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-cyber-surface border border-cyber-border">
            <h2 className="text-sm font-bold text-cyber-bright">Human Changelog (VibeLog)</h2>
            <p className="text-xs text-cyber-muted mt-0.5">
              Empathetic, clear breakdown of changes from the last 3 commits.
            </p>
          </div>

          <div className="p-6 rounded-xl bg-cyber-surface border border-cyber-border shadow-neo space-y-4 text-xs">
            <div className="p-4 rounded-lg bg-brand/10 border border-brand/30">
              <div className="font-bold text-sm text-cyber-bright mb-1">
                New Stripe checkout and smoother dashboard UX 🎉
              </div>
              <p className="text-cyber-muted leading-relaxed">
                You added Stripe subscription buttons and improved the visual layout of your app. No breaking changes detected!
              </p>
            </div>

            <div>
              <h3 className="font-bold text-cyber-bright mb-1.5">✨ New Features &amp; Upgrades</h3>
              <ul className="list-disc list-inside text-cyber-muted space-y-1">
                <li>Added Stripe Checkout webhook listener in `backend/routes/billing.py`</li>
                <li>Created animated VibeGauge radial meter for visual health grading</li>
              </ul>
            </div>

            <div>
              <h3 className="font-bold text-cyber-bright mb-1.5">🐛 Fixes &amp; Safety Polishing</h3>
              <ul className="list-disc list-inside text-cyber-muted space-y-1">
                <li>Wrapped environment variable access with fallback guards</li>
                <li>Added automatic `.gitignore` check for sensitive files</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
