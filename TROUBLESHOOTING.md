# Troubleshooting Guide

Common issues, diagnostics, and copy-pasteable solutions for **GitHub Noob Toolkit (GNT)**.

## Table of Contents

- [FastMCP Server & IDE Connection Issues](#fastmcp-server--ide-connection-issues)
- [Backend API & Database Issues](#backend-api--database-issues)
- [GitHub App Webhook & Checks API Errors](#github-app-webhook--checks-api-errors)
- [Frontend Next.js Build Issues](#frontend-nextjs-build-issues)
- [Running the Verification Test Suite](#running-the-verification-test-suite)

---

## FastMCP Server & IDE Connection Issues

### Symptom: `ModuleNotFoundError: No module named 'mcp_server'` or `'core'` in Cursor / Claude Desktop

**Causes:**
- `PYTHONPATH` is not set to the root of the `GNT` repository in your MCP configuration.
- Python virtual environment is not selected in the MCP `command` field.

**Solutions:**
```json
{
  "mcpServers": {
    "gnt": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/GNT"
      }
    }
  }
}
```

Test the MCP server directly from your terminal:
```bash
python -c "import mcp_server.server; print('FastMCP server loaded successfully!')"
```

---

## Backend API & Database Issues

### Symptom: `ConnectionRefusedError` on port `5432` when starting FastAPI

**Causes:**
- PostgreSQL container is not running, or `DATABASE_URL` points to an unreachable host.

**Solutions:**
```bash
# Option 1: Start PostgreSQL and Redis via Docker Compose
docker compose up -d gnt_postgres gnt_redis

# Option 2: Use SQLite async fallback for local zero-Docker testing
export DATABASE_URL="sqlite+aiosqlite:///./gnt_local.db"
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## GitHub App Webhook & Checks API Errors

### Symptom: `401 Unauthorized` or `Invalid webhook signature` on `/api/github/webhook`

**Causes:**
- `GITHUB_WEBHOOK_SECRET` in `.env` does not match the secret configured in your GitHub App settings.

**Solutions:**
```bash
# Verify your .env secret matches GitHub App settings and contains no trailing spaces
grep GITHUB_WEBHOOK_SECRET .env
```

---

## Frontend Next.js Build Issues

### Symptom: Next.js portal fails to reach backend API (`CORS` or `ECONNREFUSED`)

**Solutions:**
```bash
cd frontend
export NEXT_PUBLIC_API_URL="http://localhost:8000"
npm install
npm run dev
```

---

## Running the Verification Test Suite

To verify that all 6 core modules, webhook signature validators, and Stripe billing mocks are working properly:

```bash
pytest -v
```
Expected result: `25 passed`.
