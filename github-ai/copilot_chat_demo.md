# 🤖 GitHub Copilot & GitHub AI – Getting Started

This guide covers every GitHub AI tool available in the ElectroMancer Dev Container.

---

## 1. GitHub Copilot (IDE Autocomplete + Chat)

### Prerequisites
- A GitHub account with a Copilot subscription  
  (Free tier available for verified students & open-source maintainers)
- The **GitHub.copilot** and **GitHub.copilot-chat** extensions are pre-installed in this Dev Container

### Activation
1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Run **"GitHub Copilot: Sign In"**
3. Follow the browser OAuth flow

### Key Features in this Container

| Feature | How to use |
|---------|-----------|
| **Inline autocomplete** | Start typing code – Copilot suggests completions in grey |
| **Accept suggestion** | `Tab` |
| **Next suggestion** | `Alt+]` |
| **Open Copilot panel** | `Ctrl+Enter` |
| **Copilot Chat** | Click the chat icon in the sidebar or `Ctrl+Shift+I` |
| **Inline chat** | `Ctrl+I` on a selection |
| **Explain code** | Select code → right-click → *Copilot → Explain* |
| **Fix code** | Select code → right-click → *Copilot → Fix* |
| **Generate tests** | Select code → right-click → *Copilot → Generate Tests* |
| **Generate docs** | Select code → right-click → *Copilot → Generate Docs* |

### Copilot Chat Slash Commands

```
/explain    – explain the selected code
/fix        – suggest a fix for the selected code
/tests      – generate unit tests
/doc        – generate documentation
/new        – scaffold a new file or project
/search     – search the codebase
```

### Copilot Chat Agents (@ mentions)

```
@workspace  – ask questions about your whole repo
@vscode     – VS Code questions and commands
@terminal   – generate terminal commands
@github     – search GitHub issues, PRs, code
```

---

## 2. GitHub Models API (Free AI Models via Marketplace)

GitHub Models gives you access to top AI models for free through an OpenAI-compatible REST API.

### Available Models (April 2025)
| Model | Provider | Notes |
|-------|----------|-------|
| `gpt-4o-mini` | OpenAI | Fast, free tier |
| `gpt-4o` | OpenAI | Powerful |
| `Phi-3-small-128k-instruct` | Microsoft | Lightweight |
| `Phi-3-medium-128k-instruct` | Microsoft | |
| `Meta-Llama-3-8B-Instruct` | Meta | |
| `Meta-Llama-3-70B-Instruct` | Meta | Very capable |
| `Mistral-small` | Mistral AI | |
| `Mistral-large` | Mistral AI | Very capable |
| `cohere-command-r` | Cohere | |

### Quick Start

```bash
# 1. Get a GitHub PAT at https://github.com/settings/tokens
#    (no special scopes needed)
export GITHUB_TOKEN=ghp_your_token_here

# 2. Run the interactive demo
python github-ai/github_models_demo.py

# 3. Or use the API directly with curl
curl -s https://models.inference.ai.azure.com/chat/completions \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Hello from ElectroMancer!"}],
    "max_tokens": 100
  }' | jq .
```

### Python Usage (openai SDK)

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"],
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

### JavaScript/Node Usage

```js
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://models.inference.ai.azure.com",
  apiKey: process.env.GITHUB_TOKEN,
});

const response = await client.chat.completions.create({
  model: "gpt-4o-mini",
  messages: [{ role: "user", content: "Hello!" }],
});
console.log(response.choices[0].message.content);
```

### Via Cloudflare Worker Proxy (this scaffold)

The Worker in `cloudflare/worker.js` proxies GitHub Models so your React app can call it:

```bash
# Set secret for local dev
echo "GITHUB_TOKEN=ghp_..." > cloudflare/.dev.vars

# Start the Worker
cd cloudflare && wrangler dev

# Call from React or curl
curl -X POST http://localhost:8787/api/ai \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is Cloudflare Workers?", "model": "gpt-4o-mini"}'
```

---

## 3. GitHub Marketplace Extensions

These extensions are pre-installed in the Dev Container:

| Extension | Purpose |
|-----------|---------|
| **GitHub.copilot** | AI autocomplete |
| **GitHub.copilot-chat** | AI chat assistant |
| **GitHub.vscode-pull-request-github** | Review PRs in VS Code |
| **eamodio.gitlens** | Git history & blame |

### Installing Additional Marketplace Extensions
1. Open VS Code Extensions panel (`Ctrl+Shift+X`)
2. Search for any extension
3. Click **Install** – extensions persist in the container via `devcontainer.json`

---

## 4. Useful Links

- [GitHub Models documentation](https://docs.github.com/en/github-models)
- [GitHub Models marketplace](https://github.com/marketplace/models)
- [GitHub Copilot documentation](https://docs.github.com/en/copilot)
- [GitHub Copilot in VS Code](https://code.visualstudio.com/docs/copilot/overview)
- [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/)
- [Wrangler CLI docs](https://developers.cloudflare.com/workers/wrangler/)
