#!/usr/bin/env python3
"""
ElectroMancer – GitHub Models API Demo
=======================================
GitHub Models (from the GitHub Marketplace) gives you free access to
top AI models (GPT-4o, Llama, Phi, Mistral, Cohere …) through an
OpenAI-compatible API.

Setup:
  1. Create a GitHub Personal Access Token (PAT) at
     https://github.com/settings/tokens
     (No special scopes needed for Models API)
  2. Export it:
       export GITHUB_TOKEN=ghp_your_token_here
  3. Run:
       python github-ai/github_models_demo.py

Docs: https://docs.github.com/en/github-models
"""

import os
import sys
import json

# ── Check for dependency ──────────────────────────────────────
try:
    from openai import OpenAI
except ImportError:
    print("❌  'openai' package not found. Install it with:")
    print("     pip install openai")
    sys.exit(1)

# ── Configuration ─────────────────────────────────────────────
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_MODELS_ENDPOINT = "https://models.inference.ai.azure.com"

# Available free models on GitHub Models (April 2025 catalogue)
AVAILABLE_MODELS = {
    "1": ("gpt-4o-mini", "GPT-4o Mini (OpenAI) – fast, cheap"),
    "2": ("gpt-4o", "GPT-4o (OpenAI) – powerful"),
    "3": ("Phi-3-small-128k-instruct", "Phi-3 Small (Microsoft) – lightweight"),
    "4": ("Phi-3-medium-128k-instruct", "Phi-3 Medium (Microsoft)"),
    "5": ("Meta-Llama-3-8B-Instruct", "Llama 3 8B (Meta)"),
    "6": ("Meta-Llama-3-70B-Instruct", "Llama 3 70B (Meta) – very capable"),
    "7": ("Mistral-small", "Mistral Small"),
    "8": ("Mistral-large", "Mistral Large – very capable"),
    "9": ("cohere-command-r", "Cohere Command R"),
}


def list_models(client):
    """List models available through GitHub Models."""
    print("\n📋  Fetching available models from GitHub Models API…")
    try:
        models = client.models.list()
        print(f"    Found {len(list(models))} models.\n")
    except Exception as exc:
        print(f"    ⚠️  Could not list models dynamically: {exc}")
        print("    Using hard-coded catalogue instead.\n")

    print("  # │ Model ID                        │ Description")
    print("  ──┼─────────────────────────────────┼────────────────────────────────")
    for key, (model_id, desc) in AVAILABLE_MODELS.items():
        print(f"  {key} │ {model_id:<31} │ {desc}")
    print()


def chat(client, model: str, messages: list, max_tokens: int = 1024) -> str:
    """Send a chat completion request to GitHub Models."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content


def interactive_chat(client, model: str):
    """Simple REPL chat loop."""
    print(f"\n🤖  Chatting with {model}")
    print("    Type 'exit' or 'quit' to stop. Type 'clear' to reset history.\n")

    history = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant integrated into the ElectroMancer "
                "development environment. Be concise and friendly."
            ),
        }
    ]

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋  Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("👋  Goodbye!")
            break

        if user_input.lower() == "clear":
            history = [history[0]]  # keep system message
            print("🗑️   History cleared.\n")
            continue

        history.append({"role": "user", "content": user_input})

        try:
            reply = chat(client, model, history)
            print(f"\nAI : {reply}\n")
            history.append({"role": "assistant", "content": reply})
        except Exception as exc:
            print(f"❌  Error: {exc}\n")


def single_demo(client, model: str):
    """Run a pre-set demo prompt."""
    prompts = [
        "What is Cloudflare Workers and how does it differ from traditional servers?",
        "Give me a one-paragraph overview of React and Vite.",
        "What can I build with GitHub Models API?",
    ]
    print(f"\n🤖  Running demo prompts with {model}…\n")
    for prompt in prompts:
        print(f"❓  {prompt}")
        try:
            reply = chat(
                client,
                model,
                [
                    {"role": "system", "content": "Be concise."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=256,
            )
            print(f"✅  {reply}\n")
        except Exception as exc:
            print(f"❌  Error: {exc}\n")


# ── Main ──────────────────────────────────────────────────────
def main():
    if not GITHUB_TOKEN:
        print("❌  GITHUB_TOKEN environment variable is not set.")
        print("    Export your GitHub PAT:")
        print("      export GITHUB_TOKEN=ghp_your_token_here")
        print("    Docs: https://docs.github.com/en/github-models")
        sys.exit(1)

    client = OpenAI(
        base_url=GITHUB_MODELS_ENDPOINT,
        api_key=GITHUB_TOKEN,
    )

    print("━" * 60)
    print("  ⚡ ElectroMancer – GitHub Models API Demo")
    print("━" * 60)

    list_models(client)

    print("Choose a model (enter number) or press Enter for default [1]:")
    choice = input("  > ").strip() or "1"
    model_id, model_desc = AVAILABLE_MODELS.get(choice, AVAILABLE_MODELS["1"])
    print(f"\n  Selected: {model_desc}  ({model_id})")

    print("\nMode:")
    print("  1 – Demo (3 pre-set questions, non-interactive)")
    print("  2 – Interactive chat")
    mode = input("  > ").strip() or "1"

    if mode == "2":
        interactive_chat(client, model_id)
    else:
        single_demo(client, model_id)


if __name__ == "__main__":
    main()
