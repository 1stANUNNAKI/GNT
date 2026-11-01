"use client";

import React, { useState } from "react";
import { ShieldAlert, Sparkles, GitMerge, FileCode, Check, Copy, ArrowRight, AlertTriangle, ShieldCheck } from "lucide-react";

export function PlaygroundDemo() {
  const [activeTab, setActiveTab] = useState<"secrets" | "vibelog" | "conflicts">("secrets");

  // --- Secret Shield State ---
  const [secretInput, setSecretInput] = useState(
    `# App configuration\nimport os\n\nOPENAI_API_KEY = "sk-proj-999aaabbbccc111222333444555666777888999000"\nDATABASE_URL = "postgres://admin:superSecretPass123@aws.db.internal:5432/production"\n\nprint("Server booting...")`
  );
  const [scannedSecrets, setScannedSecrets] = useState<{ detected: boolean; findings: any[] } | null>(null);

  // --- VibeLog State ---
  const [diffInput, setDiffInput] = useState(
    `diff --git a/routes/payment.py b/routes/payment.py
new file mode 100644
--- /dev/null
+++ b/routes/payment.py
@@ -0,0 +1,5 @@
+from fastapi import APIRouter
+router = APIRouter()
+async def create_stripe_checkout():
+    return {"status": "paid"}
diff --git a/auth/login.py b/auth/login.py
--- a/auth/login.py
+++ b/auth/login.py
@@ -10,2 +10,4 @@
-    pass
+    try:
+        validate_jwt_token(token)
+    except Exception:
+        return False`
  );
  const [vibeLogResult, setVibeLogResult] = useState<any | null>(null);

  // --- Conflict State ---
  const [conflictInput, setConflictInput] = useState(
    `import React from 'react';
<<<<<<< HEAD (Your changes)
import { Button } from '@/components/ui/button';
import { Shield } from 'lucide-react';
=======
import { Tooltip } from '@/components/ui/tooltip';
import { Shield, Sparkles } from 'lucide-react';
>>>>>>> incoming-feature
export default function Header() { ... }`
  );
  const [conflictResolved, setConflictResolved] = useState<string | null>(null);

  // Actions
  const runSecretScan = () => {
    const findings = [];
    if (secretInput.includes("sk-") || secretInput.includes("sk-proj-")) {
      findings.push({
        rule: "OpenAI Secret API Key",
        severity: "CRITICAL",
        masked: "sk-proj-999a******************9000",
        advice: "Move this key to .env. Don't worry, everyone commits their API key once!",
      });
    }
    if (secretInput.includes("postgres://") && secretInput.includes("@")) {
      findings.push({
        rule: "Database Password Leak",
        severity: "HIGH",
        masked: "postgres://admin:********@aws.db.internal...",
        advice: "Store your database URI inside DATABASE_URL environment variable.",
      });
    }
    setScannedSecrets({ detected: findings.length > 0, findings });
  };

  const runVibeLog = () => {
    setVibeLogResult({
      headline: "New payment functionality and safer login! 🎉",
      noJargon: "You added a brand new Stripe payment endpoint and added a safety catch to stop the login screen from crashing on bad tokens.",
      features: ["Created new payment checkout endpoint in `payment.py`"],
      fixes: ["Added safety shield to catch invalid login tokens gracefully"],
    });
  };

  const runConflictMerge = (strategy: "hybrid" | "ours" | "theirs") => {
    if (strategy === "hybrid") {
      setConflictResolved(
        `import React from 'react';\nimport { Button } from '@/components/ui/button';\nimport { Tooltip } from '@/components/ui/tooltip';\nimport { Shield, Sparkles } from 'lucide-react';\n\nexport default function Header() { ... }`
      );
    } else if (strategy === "ours") {
      setConflictResolved(
        `import React from 'react';\nimport { Button } from '@/components/ui/button';\nimport { Shield } from 'lucide-react';\n\nexport default function Header() { ... }`
      );
    } else {
      setConflictResolved(
        `import React from 'react';\nimport { Tooltip } from '@/components/ui/tooltip';\nimport { Shield, Sparkles } from 'lucide-react';\n\nexport default function Header() { ... }`
      );
    }
  };

  return (
    <section id="playground" className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="text-center mb-12">
        <span className="px-3 py-1 text-xs font-semibold uppercase tracking-wider rounded-full bg-brand/10 text-brand border border-brand/30">
          Interactive Live Playground
        </span>
        <h2 className="mt-4 text-3xl sm:text-4xl font-extrabold text-cyber-bright tracking-tight">
          Try the GNT Shield in 30 Seconds
        </h2>
        <p className="mt-2 text-cyber-muted max-w-2xl mx-auto text-sm sm:text-base">
          No sign up required. See how GNT protects vibe coders from leaked keys, explains git diffs, and dissolves merge conflicts.
        </p>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap items-center justify-center gap-2 mb-6">
        <button
          onClick={() => setActiveTab("secrets")}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-xs sm:text-sm font-semibold border transition-all ${
            activeTab === "secrets"
              ? "bg-brand text-white border-brand shadow-neo-brand"
              : "bg-cyber-surface border-cyber-border text-cyber-muted hover:text-cyber-bright hover:bg-cyber-surface2"
          }`}
        >
          <ShieldAlert className="w-4 h-4 text-critical" />
          1. Secret Leak Shield
        </button>
        <button
          onClick={() => setActiveTab("vibelog")}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-xs sm:text-sm font-semibold border transition-all ${
            activeTab === "vibelog"
              ? "bg-brand text-white border-brand shadow-neo-brand"
              : "bg-cyber-surface border-cyber-border text-cyber-muted hover:text-cyber-bright hover:bg-cyber-surface2"
          }`}
        >
          <Sparkles className="w-4 h-4 text-warning" />
          2. Human Changelog (VibeLog)
        </button>
        <button
          onClick={() => setActiveTab("conflicts")}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-xs sm:text-sm font-semibold border transition-all ${
            activeTab === "conflicts"
              ? "bg-brand text-white border-brand shadow-neo-brand"
              : "bg-cyber-surface border-cyber-border text-cyber-muted hover:text-cyber-bright hover:bg-cyber-surface2"
          }`}
        >
          <GitMerge className="w-4 h-4 text-safe" />
          3. Conflict Solver
        </button>
      </div>

      {/* Main Interactive Box */}
      <div className="bg-cyber-surface border border-cyber-border rounded-xl p-6 shadow-neo">
        {/* Tab 1: Secret Shield */}
        {activeTab === "secrets" && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono text-cyber-muted flex items-center gap-1.5">
                  <FileCode className="w-3.5 h-3.5 text-brand" /> Paste Code or Git Diff
                </span>
                <span className="text-xs text-cyber-muted">Includes leaked OpenAI key & DB pass</span>
              </div>
              <textarea
                value={secretInput}
                onChange={(e) => setSecretInput(e.target.value)}
                rows={9}
                className="w-full bg-cyber-base border border-cyber-border rounded-lg p-3 text-xs sm:text-sm font-mono text-cyber-bright focus:outline-none focus:border-brand transition-colors"
              />
              <button
                onClick={runSecretScan}
                className="mt-3 w-full py-2.5 px-4 rounded-lg bg-critical hover:bg-red-600 text-white font-semibold text-xs sm:text-sm shadow-neo-crit flex items-center justify-center gap-2 transition-all active:translate-x-0.5 active:translate-y-0.5"
              >
                <ShieldAlert className="w-4 h-4" />
                Scan for Leaks
              </button>
            </div>

            <div className="bg-cyber-base border border-cyber-border rounded-lg p-4 flex flex-col justify-between">
              <div>
                <div className="text-xs font-semibold text-cyber-muted uppercase tracking-wider mb-3">
                  Shield Inspection Results
                </div>
                {!scannedSecrets ? (
                  <div className="text-center py-12 text-cyber-muted text-xs">
                    Click &quot;Scan for Leaks&quot; to test GNT&apos;s automated secret interception.
                  </div>
                ) : scannedSecrets.findings.length > 0 ? (
                  <div className="space-y-3">
                    {scannedSecrets.findings.map((f, i) => (
                      <div key={i} className="p-3 rounded-lg border border-critical/40 bg-critical/10 text-xs">
                        <div className="flex items-center justify-between font-bold text-critical">
                          <span>{f.rule}</span>
                          <span className="px-1.5 py-0.5 rounded bg-critical text-white text-[10px]">
                            {f.severity}
                          </span>
                        </div>
                        <div className="mt-1 font-mono text-cyber-bright bg-cyber-surface/80 p-1.5 rounded border border-cyber-border">
                          {f.masked}
                        </div>
                        <p className="mt-2 text-cyber-muted">{f.advice}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="flex items-center gap-2 p-4 rounded-lg bg-safe/10 border border-safe/30 text-safe text-xs">
                    <ShieldCheck className="w-5 h-5" />
                    All clear! No exposed keys detected. Safe to push!
                  </div>
                )}
              </div>

              {scannedSecrets && scannedSecrets.findings.length > 0 && (
                <div className="mt-4 pt-3 border-t border-cyber-border flex items-center justify-between">
                  <span className="text-xs text-cyber-muted">One-click safe fix available:</span>
                  <button
                    onClick={() => {
                      setSecretInput(`import os\n\nOPENAI_API_KEY = os.getenv("OPENAI_API_KEY")\nDATABASE_URL = os.getenv("DATABASE_URL")\n\nprint("Server booting safely...")`);
                      setScannedSecrets({ detected: false, findings: [] });
                    }}
                    className="px-3 py-1.5 rounded text-xs font-semibold bg-safe text-white hover:bg-emerald-600 transition-colors shadow-neo-safe"
                  >
                    1-Click Move to .env 🪄
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Tab 2: VibeLog */}
        {activeTab === "vibelog" && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono text-cyber-muted flex items-center gap-1.5">
                  <FileCode className="w-3.5 h-3.5 text-warning" /> Git Diff
                </span>
                <span className="text-xs text-cyber-muted">Intimidating technical diff</span>
              </div>
              <textarea
                value={diffInput}
                onChange={(e) => setDiffInput(e.target.value)}
                rows={9}
                className="w-full bg-cyber-base border border-cyber-border rounded-lg p-3 text-xs sm:text-sm font-mono text-cyber-bright focus:outline-none focus:border-brand transition-colors"
              />
              <button
                onClick={runVibeLog}
                className="mt-3 w-full py-2.5 px-4 rounded-lg bg-brand hover:bg-brand-hover text-white font-semibold text-xs sm:text-sm shadow-neo-brand flex items-center justify-center gap-2 transition-all active:translate-x-0.5 active:translate-y-0.5"
              >
                <Sparkles className="w-4 h-4" />
                Explain Like I&apos;m Human (No-Jargon)
              </button>
            </div>

            <div className="bg-cyber-base border border-cyber-border rounded-lg p-4">
              <div className="text-xs font-semibold text-cyber-muted uppercase tracking-wider mb-3">
                Human-Readable Changelog (VibeLog)
              </div>
              {!vibeLogResult ? (
                <div className="text-center py-12 text-cyber-muted text-xs">
                  Click &quot;Explain Like I&apos;m Human&quot; to translate git hashes into friendly English.
                </div>
              ) : (
                <div className="space-y-3 text-xs">
                  <div className="p-3 rounded-lg bg-cyber-surface border border-brand/30">
                    <div className="font-bold text-sm text-cyber-bright mb-1">{vibeLogResult.headline}</div>
                    <p className="text-cyber-muted">{vibeLogResult.noJargon}</p>
                  </div>

                  <div>
                    <div className="font-semibold text-cyber-bright mb-1">✨ New Features & Upgrades</div>
                    <ul className="list-disc list-inside text-cyber-muted space-y-1">
                      {vibeLogResult.features.map((f: string, i: number) => (
                        <li key={i}>{f}</li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <div className="font-semibold text-cyber-bright mb-1">🐛 Fixes & Polishing</div>
                    <ul className="list-disc list-inside text-cyber-muted space-y-1">
                      {vibeLogResult.fixes.map((fx: string, i: number) => (
                        <li key={i}>{fx}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Tab 3: Conflicts */}
        {activeTab === "conflicts" && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono text-cyber-muted flex items-center gap-1.5">
                  <FileCode className="w-3.5 h-3.5 text-safe" /> Conflict Markers
                </span>
                <span className="text-xs text-cyber-muted">&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</span>
              </div>
              <textarea
                value={conflictInput}
                onChange={(e) => setConflictInput(e.target.value)}
                rows={9}
                className="w-full bg-cyber-base border border-cyber-border rounded-lg p-3 text-xs sm:text-sm font-mono text-cyber-bright focus:outline-none focus:border-brand transition-colors"
              />
              <div className="mt-3 flex items-center gap-2">
                <button
                  onClick={() => runConflictMerge("hybrid")}
                  className="flex-1 py-2 px-3 rounded-lg bg-brand hover:bg-brand-hover text-white font-semibold text-xs shadow-neo-brand transition-all active:translate-x-0.5 active:translate-y-0.5"
                >
                  Smart Hybrid Merge ✨
                </button>
                <button
                  onClick={() => runConflictMerge("ours")}
                  className="py-2 px-3 rounded-lg bg-cyber-surface2 hover:bg-cyber-border text-cyber-bright font-semibold text-xs border border-cyber-border"
                >
                  Accept Ours
                </button>
                <button
                  onClick={() => runConflictMerge("theirs")}
                  className="py-2 px-3 rounded-lg bg-cyber-surface2 hover:bg-cyber-border text-cyber-bright font-semibold text-xs border border-cyber-border"
                >
                  Accept Theirs
                </button>
              </div>
            </div>

            <div className="bg-cyber-base border border-cyber-border rounded-lg p-4">
              <div className="text-xs font-semibold text-cyber-muted uppercase tracking-wider mb-3">
                Resolved Conflict Patch (No Marker Git Bloat)
              </div>
              {!conflictResolved ? (
                <div className="text-center py-12 text-cyber-muted text-xs">
                  Choose a merge button to safely produce conflict-free code without git accidents.
                </div>
              ) : (
                <div className="space-y-3">
                  <pre className="p-3 bg-cyber-surface border border-safe/40 rounded-lg text-xs font-mono text-safe overflow-x-auto whitespace-pre-wrap">
                    {conflictResolved}
                  </pre>
                  <div className="p-3 rounded-lg bg-safe/10 border border-safe/30 text-safe text-xs flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 flex-shrink-0" />
                    Conflict resolved smoothly! Combined both import lists with zero duplicates.
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
