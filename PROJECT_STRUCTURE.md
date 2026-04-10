# Project Structure v2.1 – Stable Workspace

- **docs/** → All literature, AI-CHATS gems, screenshots, salvage notes
- **src/control_bridge/** → FastAPI orchestrator + mitmproxy + API clients
- **src/bundler/** → SandFS virtual FS, ID-tag sandbox, snapshot engine
- **src/agents/** → Igor's MCP Empire (modular, headless-browser ready)
- **electron_cockpit/** → Minimal Electron + Monaco editor (recommended base: https://github.com/leonkoech/electron-code-editor)
  - Monaco primary editor
  - xterm terminal
  - 3 side-car tabs (Grok/DeepSeek/Gemini API + optional webview)
  - Cytoscape graph panel (contextual tags + usage weights)
  - Obsidian live sync

Main branch = clean, production-ready code only.
Salvage branches = CounterBalance + any other old repos (refactor as you go).

---

## Full Folder Map

```
ElectroMancer--UnClassZer0/
├── README.md                          ← Main literature + vision
├── PROJECT_STRUCTURE.md               ← This file: full folder map + explanations
├── CONTROL_BRIDGE_v2.1_SPEC.md        ← Control Bridge + Bundler vision (full spec)
├── BUNDLER_v2_SPEC.md                 ← Virtual FS sandbox + snapshots spec
├── QUICK_START_v2.md                  ← One-click setup for new collaborators
├── .gitignore
├── .env.example                       ← Template for all environment variables
│
├── docs/
│   ├── AI-CHATS/                      ← Copy your best AI dialog gems here
│   ├── SCREENSHOTS/                   ← UI screenshots, architecture diagrams
│   └── SALVAGE_NOTES.md               ← Notes from salvaged repos / old branches
│
├── src/
│   ├── control_bridge/                ← control_bridge.py (FastAPI orchestrator)
│   ├── bundler/                       ← SandFS virtual FS + snapshot engine
│   ├── agents/                        ← Igor's MCP Empire modules
│   ├── electron_cockpit/              ← Electron + Monaco source (inner src/)
│   ├── index.html                     ← HTML starter (Live Server → :5500)
│   ├── styles.css                     ← Shared dark-theme stylesheet
│   ├── app.py                         ← Flask app → :5000
│   └── index.php                      ← PHP page → :8000
│
├── electron_cockpit/                  ← Top-level Electron app root
│   └── (populated from leonkoech template or custom build)
│
├── react-cloudflare-app/              ← Vite + React → :5173
├── cloudflare/                        ← Cloudflare Worker
├── github-ai/                         ← GitHub Models demo
└── requirements.txt
```
