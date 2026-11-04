# Security Policy

## Supported Versions

| Version | Supported |
| --- | --- |
| 2.x (Current `main`) | :white_check_mark: |
| 1.x | :white_check_mark: |
| < 1.0 | :x: |

Security fixes land on `main` first and are verified against the full `pytest` security regression suite (`tests/test_secrets.py` and `tests/test_github_app.py`).

## Reporting a Vulnerability

Use **GitHub Private Vulnerability Reporting** whenever possible so the report reaches the maintainer directly:

- <https://github.com/1stANUNNAKI/GNT/security/advisories/new>

Do **not** open a public GitHub issue for security vulnerabilities.

Include:

- Affected file, module (`core/`, `backend/`, `github_app/`, `mcp_server/`, `frontend/`), version, and commit SHA
- Steps to reproduce from a clean checkout
- Expected impact and affected trust boundary (e.g., webhook signature verification, MCP tool boundary, secret scanner bypass, or JWT auth)
- Any PoC logs with real tokens, keys, local paths, and private data redacted (`[REDACTED]`)

Expected response SLA:

- **Acknowledgment:** within 48 hours
- **Initial assessment:** within 7 days
- **Critical fix or mitigation target:** within 14 days when the report affects a supported release and crosses a real trust boundary
- **Coordinated disclosure:** before public advisory publication

## Scope

This policy covers:

- The `1stANUNNAKI/GNT` repository (`GitHub Noob Toolkit`)
- The **GNT Core Engine** (`core/secrets.py`, `core/docgen.py`, `core/vibelog.py`, `core/conflicts.py`, `core/dependencies.py`, `core/health_score.py`)
- The **FastAPI Backend & Stripe Webhook Service** (`backend/`)
- The **GitHub App Webhook & Checks API Server** (`github_app/`)
- The **GNT FastMCP Server** (`mcp_server/server.py`)
- Bundled AI Agent Skills (`skills/`), Agents (`agents/`), and Slash Commands (`commands/`)

## Official Distribution Surfaces

Official GNT surfaces are:

- **GitHub Repository:** <https://github.com/1stANUNNAKI/GNT>
- **Companion Gist & Sanitizer Suite:** <https://github.com/1stANUNNAKI/GITHUB-GIST-ARCHITECT>
- **Local FastMCP Entry Point:** `python -m mcp_server.server`

Treat any third-party package or mirror not explicitly listed in this repository as unofficial until verified.

## Out of Scope

Reports are usually out of scope when they only show:

- Local command execution where the user already controls the local shell and no higher-privilege trust boundary is crossed
- Missing rate limits in local-only development mode (`uvicorn --reload`) without production reverse-proxy configuration
- Self-XSS or social engineering with no repository-controlled exploit path
- Vulnerabilities in third-party dependencies unless GNT pins or invokes them in a way that creates exploitable impact

## Supply-Chain & Webhook Security Rules

GNT treats supply-chain and webhook exposure as first-class security surfaces:

1. **HMAC-SHA256 Webhook Verification (`github_app/webhook_handler.py`):** Every incoming GitHub webhook MUST be validated using constant-time `hmac.compare_digest` against `GITHUB_WEBHOOK_SECRET` before any payload parsing occurs.
2. **Stripe Webhook Signature Verification (`backend/stripe_service.py`):** Every billing event is verified against `STRIPE_WEBHOOK_SECRET`.
3. **Zero Secret Persistence:** `core/secrets.py` masks all detected credentials via `mask_secret()` so raw secrets are never written to database tables, logs, or PR comments.
4. **Pinned GitHub Actions:** CI/CD workflows under `.github/workflows/` must never interpolate untrusted PR titles or branch names directly into `run:` shell blocks.

## Operational Guidance

### Secrets Handling

`.env.example` is a **template**. All placeholder values must be populated in a local, untracked `.env` file or injected via cloud secret managers. Never commit real credentials. If a secret is accidentally committed, rotate it immediately at the issuing provider and rewrite git history.

Quick local secret audit before pushing:

```bash
# macOS / Linux
grep -rnE '(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|sk_live_[A-Za-z0-9]{20,})' .
```

```powershell
# Windows PowerShell
Select-String -Path .\* -Include *.py,*.ts,*.tsx,*.json,*.md -Pattern '(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|sk_live_[A-Za-z0-9]{20,})'
```

### Local API & FastMCP Ports

Before starting the FastAPI backend (`:8000`) or Next.js portal (`:3000`), verify no unauthorized process is intercepting local ports:

```powershell
# Windows
netstat -ano | findstr :8000
```

```bash
# macOS / Linux
lsof -iTCP:8000 -sTCP:LISTEN
```

## Security Resources

- **Built-in Secret Scanner Test Suite:** `pytest tests/test_secrets.py -v`
- **OWASP MCP Top 10:** <https://owasp.org/www-project-mcp-top-10/>
- **OWASP Top 10 for Agentic Applications:** <https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/>
