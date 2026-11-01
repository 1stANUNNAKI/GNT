import Link from "next/link";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { PlaygroundDemo } from "@/components/PlaygroundDemo";
import {
  ShieldAlert,
  Sparkles,
  GitMerge,
  BookOpen,
  Boxes,
  Terminal,
  ArrowRight,
  CheckCircle2,
  Lock,
  Zap,
} from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-cyber-base text-cyber-text bg-cyber-grid">
      <Navbar />

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-20 pb-28 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="text-center">
          {/* Top Pill */}
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand/10 border border-brand/40 text-brand text-xs font-semibold tracking-wide uppercase shadow-neo-brand mb-6 animate-pulse">
            <Zap className="w-3.5 h-3.5" />
            Built for Vibe Coders & Non-Traditional Developers
          </div>

          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold text-cyber-bright tracking-tight max-w-4xl mx-auto leading-tight">
            Build Fast with AI. <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand via-purple-400 to-safe">
              Never Leak a Secret.
            </span>{" "}
            Never Fear Git.
          </h1>

          <p className="mt-6 text-base sm:text-xl text-cyber-muted max-w-2xl mx-auto leading-relaxed">
            The automated protective shield and friendly copilot that intercepts leaked API keys,
            turns terrifying git diffs into human English, and dissolves merge conflicts in one click.
          </p>

          {/* Action CTAs */}
          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Link
              href="/dashboard"
              className="flex items-center gap-2 px-6 py-3.5 rounded-lg bg-brand hover:bg-brand-hover text-white text-sm sm:text-base font-bold shadow-neo-brand transition-all active:translate-x-0.5 active:translate-y-0.5"
            >
              <Sparkles className="w-5 h-5" />
              Launch Web Dashboard
              <ArrowRight className="w-4 h-4 ml-1" />
            </Link>
            <a
              href="https://github.com"
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-2 px-6 py-3.5 rounded-lg bg-cyber-surface border border-cyber-border hover:bg-cyber-surface2 text-cyber-bright text-sm sm:text-base font-semibold shadow-neo transition-all"
            >
              <Lock className="w-4 h-4 text-safe" />
              Install Free GitHub App
            </a>
          </div>

          {/* Stats Bar */}
          <div className="mt-14 pt-8 border-t border-cyber-border/70 max-w-3xl mx-auto grid grid-cols-2 sm:grid-cols-4 gap-6 text-center">
            <div>
              <div className="text-2xl font-black text-cyber-bright font-mono">10,000+</div>
              <div className="text-xs text-cyber-muted mt-0.5">Secrets Shielded</div>
            </div>
            <div>
              <div className="text-2xl font-black text-safe font-mono">0 Git Shame</div>
              <div className="text-xs text-cyber-muted mt-0.5">No-Jargon Guaranteed</div>
            </div>
            <div>
              <div className="text-2xl font-black text-brand font-mono">1-Click</div>
              <div className="text-xs text-cyber-muted mt-0.5">Conflict Healing</div>
            </div>
            <div>
              <div className="text-2xl font-black text-cyber-bright font-mono">100% Free</div>
              <div className="text-xs text-cyber-muted mt-0.5">For Open Source</div>
            </div>
          </div>
        </div>
      </section>

      {/* Interactive Live Playground */}
      <PlaygroundDemo />

      {/* 5 Core Pillars Grid */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <span className="px-3 py-1 text-xs font-semibold uppercase tracking-wider rounded-full bg-safe/10 text-safe border border-safe/30">
            Unified Safety Ecosystem
          </span>
          <h2 className="mt-4 text-3xl sm:text-4xl font-extrabold text-cyber-bright tracking-tight">
            5 Automated Superpowers
          </h2>
          <p className="mt-2 text-cyber-muted max-w-xl mx-auto text-sm sm:text-base">
            Everything you need to write software fearlessly without getting stuck in terminal git hell.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Card 1 */}
          <div className="p-6 rounded-xl bg-cyber-surface border border-cyber-border shadow-neo hover:border-brand/60 transition-all">
            <div className="w-10 h-10 rounded-lg bg-critical/10 border border-critical/30 flex items-center justify-center text-critical mb-4">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-cyber-bright">1. Secret Leak Shield</h3>
            <p className="mt-2 text-xs sm:text-sm text-cyber-muted leading-relaxed">
              Scans PRs with deterministic Regex + Shannon Entropy for OpenAI, Stripe, AWS, and SSH keys. Automatically warns if `.env` was committed.
            </p>
          </div>

          {/* Card 2 */}
          <div className="p-6 rounded-xl bg-cyber-surface border border-cyber-border shadow-neo hover:border-brand/60 transition-all">
            <div className="w-10 h-10 rounded-lg bg-brand/10 border border-brand/30 flex items-center justify-center text-brand mb-4">
              <BookOpen className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-cyber-bright">2. Auto-README & DocGen</h3>
            <p className="mt-2 text-xs sm:text-sm text-cyber-muted leading-relaxed">
              Analyzes dependencies and Dockerfiles to auto-create beautiful setup guides with 3-step copy-paste run commands.
            </p>
          </div>

          {/* Card 3 */}
          <div className="p-6 rounded-xl bg-cyber-surface border border-cyber-border shadow-neo hover:border-brand/60 transition-all">
            <div className="w-10 h-10 rounded-lg bg-warning/10 border border-warning/30 flex items-center justify-center text-warning mb-4">
              <Sparkles className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-cyber-bright">3. Human Changelog (VibeLog)</h3>
            <p className="mt-2 text-xs sm:text-sm text-cyber-muted leading-relaxed">
              Translates confusing git commit diffs into cheerful, readable bullet points: Features ✨, Fixes 🐛, and No-Jargon summaries.
            </p>
          </div>

          {/* Card 4 */}
          <div className="p-6 rounded-xl bg-cyber-surface border border-cyber-border shadow-neo hover:border-brand/60 transition-all">
            <div className="w-10 h-10 rounded-lg bg-safe/10 border border-safe/30 flex items-center justify-center text-safe mb-4">
              <GitMerge className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-cyber-bright">4. Branch Conflict Solver</h3>
            <p className="mt-2 text-xs sm:text-sm text-cyber-muted leading-relaxed">
              In-memory conflict resolver that understands what each branch did and offers one-click Smart Hybrid Merges without losing work.
            </p>
          </div>

          {/* Card 5 */}
          <div className="p-6 rounded-xl bg-cyber-surface border border-cyber-border shadow-neo hover:border-brand/60 transition-all">
            <div className="w-10 h-10 rounded-lg bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400 mb-4">
              <Boxes className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-cyber-bright">5. DepDoctor (AST Scanner)</h3>
            <p className="mt-2 text-xs sm:text-sm text-cyber-muted leading-relaxed">
              Uses Abstract Syntax Trees to catch imported packages missing from `package.json` or `requirements.txt` before deployment crashes.
            </p>
          </div>

          {/* Card 6: MCP Integration */}
          <div className="p-6 rounded-xl bg-cyber-surface border border-cyber-border shadow-neo hover:border-brand/60 transition-all">
            <div className="w-10 h-10 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 mb-4">
              <Terminal className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-cyber-bright">6. FastMCP IDE Integration</h3>
            <p className="mt-2 text-xs sm:text-sm text-cyber-muted leading-relaxed">
              Direct Model Context Protocol server for Cursor and Claude Desktop. Shield your code before it ever touches git!
            </p>
          </div>
        </div>
      </section>

      {/* Pricing Preview Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto border-t border-cyber-border">
        <div className="text-center mb-16">
          <span className="px-3 py-1 text-xs font-semibold uppercase tracking-wider rounded-full bg-brand/10 text-brand border border-brand/30">
            Simple, Transparent Pricing
          </span>
          <h2 className="mt-4 text-3xl sm:text-4xl font-extrabold text-cyber-bright tracking-tight">
            Invest in Peace of Mind
          </h2>
          <p className="mt-2 text-cyber-muted max-w-xl mx-auto text-sm sm:text-base">
            One leaked API key can cost thousands. GNT keeps your wallet safe for the price of two coffees.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {/* Free Tier */}
          <div className="p-6 rounded-xl bg-cyber-surface border border-cyber-border shadow-neo flex flex-col justify-between">
            <div>
              <div className="text-sm font-bold text-cyber-muted uppercase tracking-wider">Hobby / Starter</div>
              <div className="mt-4 text-3xl font-extrabold text-cyber-bright">$0 <span className="text-xs text-cyber-muted font-normal">/ forever</span></div>
              <p className="mt-2 text-xs text-cyber-muted">Ideal for personal hobby experiments & learning git.</p>
              <ul className="mt-6 space-y-2.5 text-xs text-cyber-bright">
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-safe" /> 3 Public Repositories</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-safe" /> Secret Leak Shield</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-safe" /> Auto-README Generator</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-safe" /> Community Discord Support</li>
              </ul>
            </div>
            <Link
              href="/dashboard"
              className="mt-8 block text-center py-2.5 px-4 rounded-lg bg-cyber-surface2 hover:bg-cyber-border text-cyber-bright text-xs font-semibold border border-cyber-border transition-colors"
            >
              Get Started Free
            </Link>
          </div>

          {/* Pro Tier (Featured) */}
          <div className="p-6 rounded-xl bg-cyber-surface border-2 border-brand shadow-neo-brand relative flex flex-col justify-between">
            <div className="absolute -top-3 right-6 px-2.5 py-0.5 rounded-full bg-brand text-white text-[10px] font-bold uppercase tracking-wider">
              Most Popular
            </div>
            <div>
              <div className="text-sm font-bold text-brand uppercase tracking-wider">Vibe Pro</div>
              <div className="mt-4 text-3xl font-extrabold text-cyber-bright">$12 <span className="text-xs text-cyber-muted font-normal">/ month</span></div>
              <p className="mt-2 text-xs text-cyber-muted">For AI vibe coders shipping apps to production.</p>
              <ul className="mt-6 space-y-2.5 text-xs text-cyber-bright">
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-brand" /> Unlimited Private & Public Repos</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-brand" /> Automated PR Check Run Blocker</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-brand" /> 1-Click Conflict Solver</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-brand" /> DepDoctor AST Auto-Patching</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-brand" /> FastMCP IDE Integration (Cursor / Claude)</li>
              </ul>
            </div>
            <Link
              href="/pricing"
              className="mt-8 block text-center py-2.5 px-4 rounded-lg bg-brand hover:bg-brand-hover text-white text-xs font-semibold shadow-neo-brand transition-colors"
            >
              Upgrade to Pro (Stripe)
            </Link>
          </div>

          {/* Team Tier */}
          <div className="p-6 rounded-xl bg-cyber-surface border border-cyber-border shadow-neo flex flex-col justify-between">
            <div>
              <div className="text-sm font-bold text-cyber-muted uppercase tracking-wider">Team / Studio</div>
              <div className="mt-4 text-3xl font-extrabold text-cyber-bright">$29 <span className="text-xs text-cyber-muted font-normal">/ month</span></div>
              <p className="mt-2 text-xs text-cyber-muted">For agencies, hackathon squads, and startup teams.</p>
              <ul className="mt-6 space-y-2.5 text-xs text-cyber-bright">
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-safe" /> Everything in Pro</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-safe" /> 10 Team Member Seats</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-safe" /> Organization-wide Secret Vault</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-safe" /> Priority Support & Webhook SLA</li>
              </ul>
            </div>
            <Link
              href="/pricing"
              className="mt-8 block text-center py-2.5 px-4 rounded-lg bg-cyber-surface2 hover:bg-cyber-border text-cyber-bright text-xs font-semibold border border-cyber-border transition-colors"
            >
              Start Team Plan
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
