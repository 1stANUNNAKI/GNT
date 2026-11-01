"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Terminal, Copy, Check, Zap, CreditCard, Shield, ExternalLink } from "lucide-react";

export default function SettingsPage() {
  const [copiedMcp, setCopiedMcp] = useState(false);

  const mcpConfigJson = `{
  "mcpServers": {
    "gnt": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "env": {
        "GNT_API_KEY": "gnt_live_token_sample_12345"
      }
    }
  }
}`;

  const copyMcpConfig = () => {
    navigator.clipboard.writeText(mcpConfigJson);
    setCopiedMcp(true);
    setTimeout(() => setCopiedMcp(false), 1500);
  };

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-black text-cyber-bright tracking-tight">Settings &amp; Integrations</h1>
        <p className="text-xs sm:text-sm text-cyber-muted mt-1">
          Configure Model Context Protocol (MCP) tools for Cursor, manage Stripe billing, and set webhook secrets.
        </p>
      </div>

      {/* Section 1: FastMCP IDE Integration */}
      <div className="p-6 rounded-2xl bg-cyber-surface border border-cyber-border shadow-neo space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-lg bg-brand/10 border border-brand/30 text-brand">
              <Terminal className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-cyber-bright">Model Context Protocol (FastMCP)</h2>
              <p className="text-xs text-cyber-muted">Direct integration into Cursor, Claude Desktop &amp; Windsurf</p>
            </div>
          </div>
          <button
            onClick={copyMcpConfig}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-cyber-surface2 hover:bg-cyber-border text-cyber-bright text-xs font-semibold border border-cyber-border transition-colors shadow-neo-sm"
          >
            {copiedMcp ? <Check className="w-3.5 h-3.5 text-safe" /> : <Copy className="w-3.5 h-3.5" />}
            {copiedMcp ? "Copied JSON!" : "Copy Config"}
          </button>
        </div>

        <p className="text-xs text-cyber-muted leading-relaxed">
          Paste this snippet into your <code className="text-brand">claude_desktop_config.json</code> or <code className="text-brand">.cursor/mcp.json</code>. Your AI agent will automatically gain the ability to scan for secrets, explain git diffs, and heal conflicts before you push.
        </p>

        <pre className="p-4 rounded-xl bg-cyber-base border border-cyber-border font-mono text-xs text-cyber-bright overflow-x-auto whitespace-pre-wrap">
          {mcpConfigJson}
        </pre>
      </div>

      {/* Section 2: Stripe Billing */}
      <div className="p-6 rounded-2xl bg-cyber-surface border border-cyber-border shadow-neo space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-lg bg-safe/10 border border-safe/30 text-safe">
              <CreditCard className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-cyber-bright">Subscription &amp; Monetization</h2>
              <p className="text-xs text-cyber-muted">Manage payments, invoices, and active plan</p>
            </div>
          </div>
          <Link
            href="/pricing"
            className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-brand hover:bg-brand-hover text-white text-xs font-semibold shadow-neo-brand transition-colors"
          >
            <Zap className="w-3.5 h-3.5" /> Change Plan
          </Link>
        </div>

        <div className="p-4 rounded-xl bg-cyber-base border border-cyber-border flex items-center justify-between">
          <div>
            <div className="text-xs font-bold text-cyber-bright">Active Plan: <span className="text-brand">Vibe Pro ($12/month)</span></div>
            <div className="text-[11px] text-cyber-muted mt-0.5">Renews automatically via Stripe. Cancel anytime.</div>
          </div>
          <a
            href="http://localhost:8000/api/billing/portal"
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-1 text-xs font-medium text-cyber-muted hover:text-cyber-bright underline"
          >
            Stripe Customer Portal <ExternalLink className="w-3 h-3" />
          </a>
        </div>
      </div>
    </div>
  );
}
