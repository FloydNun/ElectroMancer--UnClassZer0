# Control Bridge + Bundler v2.1 Spec
*(Exactly as described — the unbreakable workspace)*

---

## Core Upgrades

- **Minimal Electron base** (Monaco-first, clean navigation/terminal)
- **3 side-car tabs:** Grok API + DeepSeek API + Gemini API (CLI under the hood + optional browser view)
- **Bundles mounted as virtual FS (SandFS)** → AI reads any file, writes ONLY with `_IDTAG` suffix
- **Serve-Safe Snapshot Engine** → rapid prototype test + instant revert
- **mitmproxy layer** → Lippy/Igor orchestration in headless browsers via Grok API
- **HTTP proxy** auto-extracts code/context + injects tagged commands (`@GROK:save_as_DV` etc.)
- **Obsidian** = true integration platform + live graph (weights by usage)
- No LLM Studio, no bridge worker bloat

This is the unbreakable workspace for housing stability.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                  Electron Cockpit                       │
│  ┌──────────────┐  ┌────────┐  ┌──────────────────┐   │
│  │ Monaco Editor│  │ xterm  │  │  Cytoscape Graph  │   │
│  └──────────────┘  └────────┘  └──────────────────┘   │
│  ┌──────────┐ ┌───────────┐ ┌───────────┐             │
│  │ Grok Tab │ │DeepSeek   │ │ Gemini Tab│             │
│  └──────────┘ └───────────┘ └───────────┘             │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP / WebSocket
┌───────────────────────▼─────────────────────────────────┐
│              Control Bridge (FastAPI)                    │
│  - Route requests to Grok / DeepSeek / Gemini APIs      │
│  - Manage SandFS bundle mounts                          │
│  - Trigger snapshot engine                              │
│  - Inject @IDTAG write-protection logic                 │
└────────┬──────────────────────────┬──────────────────────┘
         │                          │
┌────────▼────────┐      ┌──────────▼──────────┐
│  Bundler/SandFS │      │  mitmproxy Layer     │
│  - Virtual FS   │      │  - Headless browsers │
│  - ID-tag writes│      │  - Lippy/Igor agents │
│  - Snapshots    │      │  - Context extraction│
└─────────────────┘      └─────────────────────┘
         │
┌────────▼────────┐
│    Obsidian     │
│  - Live sync    │
│  - Usage graph  │
│  - Note weights │
└─────────────────┘
```

---

## SandFS Write-Protection Rules

| Operation | Allowed | Notes |
|-----------|---------|-------|
| Read any file | ✅ | All agents can read freely |
| Write with `_IDTAG` suffix | ✅ | e.g. `output_GROK.py`, `result_DV.md` |
| Write without `_IDTAG` | ❌ | Blocked at the FS layer |
| Overwrite existing file | ❌ | Must snapshot first |

---

## Snapshot Engine

- **Pre-action snapshot** → taken automatically before any write
- **Named snapshots** → `@SNAP:name` tag in any AI command
- **Instant revert** → `@REVERT:name` rolls back the entire SandFS state
- Snapshots stored in `src/bundler/snapshots/` as timestamped archives

---

## API Side-Car Tab Commands

| Command Tag | Action |
|-------------|--------|
| `@GROK:save_as_DV` | Save AI output as `*_DV` tagged file |
| `@GROK:snapshot` | Force a named snapshot before writing |
| `@DS:explain` | Route to DeepSeek for explanation |
| `@GEM:review` | Route to Gemini for code review |
| `@SNAP:name` | Create named snapshot |
| `@REVERT:name` | Revert to named snapshot |
