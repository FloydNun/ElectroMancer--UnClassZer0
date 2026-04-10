# ⚡ ElectroMancer – UnClassZer0

**UnClassZer0 Edition · AI SuperFriends Team · Human-AI Symbiosis Framework**  
`#ORIGIN` `#AISFT` `#BUILD-from-inside`

A fully-configured development scaffold featuring a **Dev Container** (Windows & Linux), live-preview for **Python · PHP · HTML/CSS**, a **React + Vite** app deployed to **Cloudflare Pages**, a **Cloudflare Worker**, and a **GitHub AI (GitHub Models)** integration.

---

## 🚀 Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows) or Docker Engine (Linux)
- [VS Code](https://code.visualstudio.com/) + [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Open in Dev Container
1. Clone this repo and open it in VS Code
2. Press `F1` → **Dev Containers: Reopen in Container**
3. Wait for the container to build and `post-create.sh` to finish (~2 min first time)
4. All tools, extensions, and ports are ready automatically!

---

## 📁 Repository Structure

```
.
├── .devcontainer/
│   ├── devcontainer.json   # Dev Container config (extensions, ports, features)
│   ├── Dockerfile          # Base image (Ubuntu 22.04 + Wrangler)
│   └── post-create.sh      # Auto-runs after container build
│
├── src/                    # HTML / CSS / Python / PHP starters
│   ├── index.html          # HTML starter page (open with Live Server → :5500)
│   ├── styles.css          # Shared dark-theme stylesheet
│   ├── app.py              # Flask app with hot-reload  → :5000
│   └── index.php           # PHP page  → :8000
│
├── react-cloudflare-app/   # Vite + React scaffold → :5173
│   ├── src/
│   │   ├── App.jsx         # Main React component (Worker API + GitHub AI demo)
│   │   ├── main.jsx
│   │   └── *.css
│   ├── vite.config.js
│   └── package.json
│
├── cloudflare/             # Cloudflare Worker
│   ├── worker.js           # Worker with /api/hello, /api/status, /api/ai
│   ├── wrangler.toml       # Wrangler config
│   └── package.json
│
├── github-ai/              # GitHub AI / Copilot guides
│   ├── github_models_demo.py   # Interactive CLI demo (Python)
│   └── copilot_chat_demo.md    # Full guide: Copilot + GitHub Models API
│
├── requirements.txt        # Python: flask, openai, requests
└── .gitignore
```

---

## 🛠️ Running the Services

All ports are auto-forwarded by the Dev Container.

| Service | Command | Port |
|---------|---------|------|
| **HTML/CSS Live Preview** | Open `src/index.html` → right-click → *Open with Live Server* | 5500 |
| **Python / Flask** | `cd src && python app.py` | 5000 |
| **PHP** | `cd src && php -S localhost:8000` | 8000 |
| **React (Vite)** | `cd react-cloudflare-app && npm run dev` | 5173 |
| **Cloudflare Worker** | `cd cloudflare && wrangler dev` | 8787 |

---

## 🤖 GitHub AI – GitHub Models (Marketplace)

Get free access to GPT-4o, Llama 3, Phi-3, Mistral, and more.

```bash
# 1. Create a GitHub PAT at https://github.com/settings/tokens
export GITHUB_TOKEN=ghp_your_token_here

# 2. Run the interactive demo
python github-ai/github_models_demo.py
```

See [`github-ai/copilot_chat_demo.md`](github-ai/copilot_chat_demo.md) for the full guide including Copilot Chat commands, slash commands, and `@agents`.

---

## ☁️ Cloudflare Integration

### Local Worker dev
```bash
# Set GITHUB_TOKEN for the AI proxy endpoint
echo "GITHUB_TOKEN=ghp_..." > cloudflare/.dev.vars

cd cloudflare && wrangler dev      # → http://localhost:8787
```

### Deploy React app to Cloudflare Pages
```bash
cd react-cloudflare-app
npm run build
wrangler pages deploy dist --project-name electromancer
```

### Deploy Worker
```bash
cd cloudflare
wrangler secret put GITHUB_TOKEN   # paste your token
wrangler deploy
```

---

## 🐍 Python API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | HTML landing page |
| `GET /api/hello` | JSON greeting |
| `GET /api/status` | Health check with timestamp |

---

## 🔑 Environment Variables

| Variable | Where | Purpose |
|----------|-------|---------|
| `GITHUB_TOKEN` | Shell export / `cloudflare/.dev.vars` | GitHub Models API + Copilot |
| `VITE_WORKER_URL` | `react-cloudflare-app/.env.local` | Override Worker URL in React |

> ⚠️ **Never commit secrets.** `.env`, `.dev.vars` are in `.gitignore`.

---

## 📦 Dev Container Features

| Tool | Version |
|------|---------|
| Python | 3.12 |
| PHP | 8.3 + Composer |
| Node.js | LTS |
| Wrangler (Cloudflare CLI) | latest |
| GitHub CLI (`gh`) | latest |

Pre-installed VS Code extensions: **GitHub Copilot**, **Copilot Chat**, **Live Server**, **Python**, **PHP Intelephense**, **ESLint**, **Prettier**, **Cloudflare Workers**, **GitLens**, and more.

---

*Built with ❤️ by the AI SuperFriends Team*
