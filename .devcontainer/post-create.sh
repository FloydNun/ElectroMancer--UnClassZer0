#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# post-create.sh  –  runs once after the dev container is built
# ──────────────────────────────────────────────────────────────
set -euo pipefail

echo "🔧  ElectroMancer post-create setup starting…"

# ── 1. Python dependencies ────────────────────────────────────
if [ -f "requirements.txt" ]; then
  echo "📦  Installing Python packages…"
  pip install --upgrade pip --quiet
  pip install -r requirements.txt --quiet
fi

# ── 2. React / Cloudflare app ─────────────────────────────────
if [ -f "react-cloudflare-app/package.json" ]; then
  echo "📦  Installing React-Cloudflare-App npm packages…"
  (cd react-cloudflare-app && npm install --silent)
fi

# ── 3. Cloudflare Worker ──────────────────────────────────────
if [ -f "cloudflare/package.json" ]; then
  echo "📦  Installing Cloudflare Worker npm packages…"
  (cd cloudflare && npm install --silent)
fi

# ── 4. Root-level npm packages (if any) ──────────────────────
if [ -f "package.json" ]; then
  echo "📦  Installing root npm packages…"
  npm install --silent
fi

# ── 5. Ensure Wrangler is available ──────────────────────────
if ! command -v wrangler &>/dev/null; then
  echo "⚙️  Installing Wrangler CLI globally…"
  npm install -g wrangler@latest --silent
fi

echo "✅  Post-create setup complete."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ElectroMancer – UnClassZer0 Dev Environment"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🐍  Python  → cd src && python app.py"
echo "  🐘  PHP     → cd src && php -S localhost:8000"
echo "  🌐  HTML/CSS → Open src/index.html with Live Server"
echo "  ⚛️   React   → cd react-cloudflare-app && npm run dev"
echo "  ☁️   Worker  → cd cloudflare && wrangler dev"
echo "  🤖  GitHub AI → python github-ai/github_models_demo.py"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
