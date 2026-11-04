---
name: secret-leak-shield
description: Dual-layer GitHub secret scanner combining deterministic regex patterns and Shannon entropy (H >= 4.0) with forbidden file (.env, id_rsa) staging guards.
origin: GNT
---

# 🛡️ Secret Leak Shield (`secret-leak-shield`)

Prevents accidental credential exposure in source files and Git diffs before commits or Pull Requests reach GitHub.

## When to Activate
- Before any `git commit` or `git push`
- When auditing code snippets, `.env` files, or Pull Request diffs for leaked API keys
- When configuring pre-receive or GitHub App Checks API security gates

## Core Capabilities (`core/secrets.py`)
1. **Deterministic Regex Matching:** Detects OpenAI (`sk-...`), Anthropic (`sk-ant-...`), Stripe Live/Test keys (`sk_live_...`), AWS Access Key IDs (`AKIA...`), GitHub PATs (`ghp_...`, `github_pat_...`), and RSA/OpenSSH private keys.
2. **Shannon Entropy Analysis ($H \ge 4.0$):** Flags high-entropy random secret assignments even when the vendor prefix is unknown.
3. **Forbidden File Guard:** Blocks `.env`, `.env.local`, `id_rsa`, and `.pem` files from being tracked in Git.

## Usage Example
```python
from core.secrets import scan_diff_for_secrets

report = scan_diff_for_secrets(diff_text, tracked_files=[".env.example", "main.py"])
if not report.passed:
    for finding in report.findings:
        print(f"[{finding.severity}] Line {finding.line_number}: {finding.rule_name} ({finding.masked_preview})")
```

## Anti-Patterns
- Never log raw matched secrets in CI output; always use `mask_secret()` so only the first 4 and last 2 characters are visible.
