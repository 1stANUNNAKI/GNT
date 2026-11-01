"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { Check, HelpCircle, Sparkles, ShieldCheck, Zap, ArrowRight, Loader2 } from "lucide-react";

export default function PricingPage() {
  const [loadingPlan, setLoadingPlan] = useState<string | null>(null);

  const handleCheckout = async (plan: string) => {
    setLoadingPlan(plan);
    try {
      const resp = await fetch("http://localhost:8000/api/billing/create-checkout-session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          plan,
          success_url: `${window.location.origin}/dashboard?billing=success`,
          cancel_url: `${window.location.origin}/pricing?billing=canceled`,
        }),
      });

      if (resp.ok) {
        const data = await resp.json();
        if (data.checkout_url) {
          window.location.href = data.checkout_url;
          return;
        }
      }
      // Fallback to direct dashboard with simulated pro
      window.location.href = `/dashboard?billing=simulated&plan=${plan}`;
    } catch {
      window.location.href = `/dashboard?billing=simulated&plan=${plan}`;
    } finally {
      setLoadingPlan(null);
    }
  };

  return (
    <div className="min-h-screen bg-cyber-base text-cyber-text bg-cyber-grid">
      <Navbar />

      <main className="max-w-7xl mx-auto py-16 px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto">
          <span className="px-3 py-1 text-xs font-semibold uppercase tracking-wider rounded-full bg-brand/10 text-brand border border-brand/30">
            Transparent Pricing
          </span>
          <h1 className="mt-4 text-4xl sm:text-5xl font-black text-cyber-bright tracking-tight">
            Stop Leaks Before They Cost You $10,000
          </h1>
          <p className="mt-4 text-sm sm:text-base text-cyber-muted">
            Simple plans for individual vibe coders and growing developer teams. Cancel or switch plans anytime.
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="mt-14 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {/* Free Tier */}
          <div className="p-8 rounded-2xl bg-cyber-surface border border-cyber-border shadow-neo flex flex-col justify-between">
            <div>
              <h3 className="text-lg font-bold text-cyber-bright">Free Starter</h3>
              <p className="mt-1 text-xs text-cyber-muted">For hobbyists and students learning GitHub.</p>
              <div className="mt-6 flex items-baseline gap-1">
                <span className="text-4xl font-black text-cyber-bright font-mono">$0</span>
                <span className="text-xs text-cyber-muted">/ month</span>
              </div>
              <ul className="mt-8 space-y-3 text-xs text-cyber-text">
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-safe" /> 3 Public Repositories</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-safe" /> Secret Leak Shield (Regex)</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-safe" /> Auto-README Generator</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-safe" /> Basic VibeLog Changelog</li>
              </ul>
            </div>
            <Link
              href="/dashboard"
              className="mt-8 block text-center py-2.5 px-4 rounded-lg bg-cyber-surface2 hover:bg-cyber-border text-cyber-bright text-xs font-semibold border border-cyber-border transition-colors shadow-neo-sm"
            >
              Start Free
            </Link>
          </div>

          {/* Pro Tier (Featured) */}
          <div className="p-8 rounded-2xl bg-cyber-surface border-2 border-brand shadow-neo-brand relative flex flex-col justify-between">
            <div className="absolute -top-3.5 right-6 px-3 py-1 rounded-full bg-brand text-white text-[11px] font-bold uppercase tracking-wider shadow-neo-brand">
              Most Popular
            </div>
            <div>
              <h3 className="text-lg font-bold text-brand flex items-center gap-1.5">
                <Zap className="w-4 h-4" /> Vibe Pro
              </h3>
              <p className="mt-1 text-xs text-cyber-muted">For serious vibe coders shipping production software.</p>
              <div className="mt-6 flex items-baseline gap-1">
                <span className="text-4xl font-black text-cyber-bright font-mono">$12</span>
                <span className="text-xs text-cyber-muted">/ month</span>
              </div>
              <ul className="mt-8 space-y-3 text-xs text-cyber-bright">
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-brand" /> Unlimited Private & Public Repos</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-brand" /> Shannon Entropy Secret Shield</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-brand" /> Checks API PR Blocker with Annotations</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-brand" /> 1-Click Merge Conflict Solver</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-brand" /> DepDoctor AST Missing Library Fixer</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-brand" /> FastMCP IDE Server (Cursor / Claude Desktop)</li>
              </ul>
            </div>
            <button
              onClick={() => handleCheckout("pro")}
              disabled={loadingPlan === "pro"}
              className="mt-8 w-full py-3 px-4 rounded-lg bg-brand hover:bg-brand-hover text-white text-xs font-bold shadow-neo-brand transition-all flex items-center justify-center gap-2"
            >
              {loadingPlan === "pro" ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
              Upgrade with Stripe
            </button>
          </div>

          {/* Team Tier */}
          <div className="p-8 rounded-2xl bg-cyber-surface border border-cyber-border shadow-neo flex flex-col justify-between">
            <div>
              <h3 className="text-lg font-bold text-cyber-bright">Team / Agency</h3>
              <p className="mt-1 text-xs text-cyber-muted">For dev agencies, startups & hackathon squads.</p>
              <div className="mt-6 flex items-baseline gap-1">
                <span className="text-4xl font-black text-cyber-bright font-mono">$29</span>
                <span className="text-xs text-cyber-muted">/ month</span>
              </div>
              <ul className="mt-8 space-y-3 text-xs text-cyber-text">
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-safe" /> Everything in Pro</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-safe" /> 10 Team Member Accounts</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-safe" /> Organization Secret Scan Audit Log</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-safe" /> Priority Webhook Processing SLA</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-safe" /> Dedicated Support via Discord/Slack</li>
              </ul>
            </div>
            <button
              onClick={() => handleCheckout("team")}
              disabled={loadingPlan === "team"}
              className="mt-8 w-full py-2.5 px-4 rounded-lg bg-cyber-surface2 hover:bg-cyber-border text-cyber-bright text-xs font-semibold border border-cyber-border transition-colors shadow-neo-sm flex items-center justify-center gap-2"
            >
              {loadingPlan === "team" ? <Loader2 className="w-4 h-4 animate-spin" /> : "Subscribe Team"}
            </button>
          </div>
        </div>

        {/* FAQs */}
        <div className="mt-24 max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold text-cyber-bright text-center mb-8">
            Frequently Asked Questions
          </h2>
          <div className="space-y-4">
            <div className="p-5 rounded-xl bg-cyber-surface border border-cyber-border">
              <h3 className="font-semibold text-cyber-bright text-sm flex items-center gap-2">
                <HelpCircle className="w-4 h-4 text-brand" />
                What if I already pushed a secret key to GitHub?
              </h3>
              <p className="mt-2 text-xs text-cyber-muted leading-relaxed">
                Don&apos;t panic! GNT&apos;s bot will immediately post a non-shaming alert on your PR with exact instructions on how to revoke the key on your provider (OpenAI, Stripe, etc.) and remove it from git history using `git rm --cached`.
              </p>
            </div>

            <div className="p-5 rounded-xl bg-cyber-surface border border-cyber-border">
              <h3 className="font-semibold text-cyber-bright text-sm flex items-center gap-2">
                <HelpCircle className="w-4 h-4 text-brand" />
                Does GNT store my source code?
              </h3>
              <p className="mt-2 text-xs text-cyber-muted leading-relaxed">
                Never. GNT processes git diffs in-memory inside ephemeral server instances. Only health scores and masked metadata (e.g. `sk-proj-ab***`) are saved in your dashboard for audit history.
              </p>
            </div>

            <div className="p-5 rounded-xl bg-cyber-surface border border-cyber-border">
              <h3 className="font-semibold text-cyber-bright text-sm flex items-center gap-2">
                <HelpCircle className="w-4 h-4 text-brand" />
                How do I connect GNT to Cursor or Claude Desktop?
              </h3>
              <p className="mt-2 text-xs text-cyber-muted leading-relaxed">
                GNT includes an official FastMCP server. Simply copy the JSON configuration snippet in your Dashboard Settings into your `claude_desktop_config.json` or `.cursor/mcp.json`.
              </p>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
