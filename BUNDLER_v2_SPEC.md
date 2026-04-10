# Bundler v2 Spec – Virtual FS Sandbox + Snapshots

---

## What Is the Bundler?

The Bundler is the **SandFS layer** that wraps your real filesystem in a sandboxed virtual FS. It lets AI agents read anything freely, but enforces write-protection: agents can only write files tagged with their ID suffix.

---

## Core Concepts

### Virtual FS (SandFS)

- **Mount Point:** `src/bundler/sandfs/`
- **Read Access:** All agents, unrestricted
- **Write Access:** Only files ending in `_<AGENT_ID>.<ext>` are accepted
  - e.g. `analysis_GROK.md`, `refactor_DV.py`, `summary_GEM.txt`
- Writes without a valid ID tag are **rejected at the FS layer** (not just warned)

### ID Tags

Each agent/API integration has a registered tag:

| Agent | ID Tag |
|-------|--------|
| Grok (xAI) | `_GROK` |
| DeepSeek | `_DV` |
| Gemini | `_GEM` |
| Igor (MCP) | `_IGOR` |
| Lippy (headless) | `_LIPPY` |
| Human / manual | `_ME` |

---

## Snapshot Engine

Snapshots capture the entire SandFS state as a compressed archive.

### Storage Location

```
src/bundler/snapshots/
├── snap_20260410_120000_baseline.tar.gz
├── snap_20260410_130000_before_refactor.tar.gz
└── snap_20260410_140000_named_stable.tar.gz
```

### Snapshot Lifecycle

1. **Auto-snapshot** → triggered before every write operation
2. **Manual snapshot** → `@SNAP:label` tag in any AI command or Control Bridge call
3. **Revert** → `@REVERT:label` (or timestamp) restores the full SandFS state
4. **Prune** → old auto-snapshots pruned after N versions (configurable in `.env`)

### Configuration (`.env` / `.env.example`)

```env
SANDFS_ROOT=src/bundler/sandfs
SNAPSHOT_DIR=src/bundler/snapshots
MAX_AUTO_SNAPSHOTS=10
ALLOWED_ID_TAGS=GROK,DV,GEM,IGOR,LIPPY,ME
```

---

## Bundle Format

A "bundle" is a self-contained project package:

```
my_bundle/
├── bundle.json        ← manifest (name, version, agent-tag allowlist)
├── src/               ← read-only source files
├── workspace/         ← agent write area (ID-tagged files only)
└── snapshots/         ← bundle-local snapshots
```

### `bundle.json` schema

```json
{
  "name": "my_bundle",
  "version": "1.0.0",
  "allowedTags": ["GROK", "DV", "GEM"],
  "readRoots": ["src/"],
  "writeRoot": "workspace/",
  "snapshotDir": "snapshots/"
}
```

---

## Python API (planned – `src/bundler/sandfs.py`)

```python
from bundler.sandfs import SandFS

fs = SandFS("path/to/my_bundle")

# Read freely
content = fs.read("src/main.py")

# Write (will raise if no valid ID tag in filename)
fs.write("workspace/analysis_GROK.md", content)

# Snapshot
fs.snapshot(label="before_big_refactor")

# Revert
fs.revert(label="before_big_refactor")
```
