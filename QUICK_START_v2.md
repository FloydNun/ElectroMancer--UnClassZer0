# Quick Start v2 – ElectroMancer AISFT

Get up and running in one shot.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows) or Docker Engine (Linux)
- [VS Code](https://code.visualstudio.com/) + [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Git

---

## Step 1 – Clone & Open in Dev Container

```bash
git clone https://github.com/FloydNun/ElectroMancer--UnClassZer0.git
cd ElectroMancer--UnClassZer0
code .
```

Press `F1` → **Dev Containers: Reopen in Container**  
Wait ~2 min for the first build. All tools and extensions auto-install.

---

## Step 2 – Copy Environment Variables

```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

Required keys for full functionality:

| Variable | Where to get it |
|----------|----------------|
| `GITHUB_TOKEN` | https://github.com/settings/tokens |
| `GROK_API_KEY` | https://console.x.ai |
| `DEEPSEEK_API_KEY` | https://platform.deepseek.com |
| `GEMINI_API_KEY` | https://aistudio.google.com/apikey |

---

## Step 3 – Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4 – Start Services

All ports are auto-forwarded by the Dev Container.

| Service | Command | Port |
|---------|---------|------|
| **Flask / Control Bridge** | `cd src && python app.py` | 5000 |
| **React (Vite)** | `cd react-cloudflare-app && npm run dev` | 5173 |
| **Cloudflare Worker** | `cd cloudflare && wrangler dev` | 8787 |
| **HTML Live Preview** | Open `src/index.html` → right-click → *Open with Live Server* | 5500 |
| **PHP** | `cd src && php -S localhost:8000` | 8000 |

---

## Step 5 – Electron Cockpit (optional, when ready)

```bash
cd electron_cockpit
npm install
npm start
```

Recommended base template: https://github.com/leonkoech/electron-code-editor

---

## Salvage Branches

Old repos (Counter Balance, etc.) live in dedicated branches — never on main.

```bash
# View salvage branches
git branch -r | grep salvage

# Check out a salvage branch
git checkout salvage/counter-balance
```

---

## Key Docs

| File | Purpose |
|------|---------|
| [README.md](README.md) | Vision + full project overview |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Folder map + explanations |
| [CONTROL_BRIDGE_v2.1_SPEC.md](CONTROL_BRIDGE_v2.1_SPEC.md) | Control Bridge + Bundler architecture |
| [BUNDLER_v2_SPEC.md](BUNDLER_v2_SPEC.md) | SandFS virtual FS + snapshot spec |
| [docs/SALVAGE_NOTES.md](docs/SALVAGE_NOTES.md) | Notes from old/salvaged repos |
