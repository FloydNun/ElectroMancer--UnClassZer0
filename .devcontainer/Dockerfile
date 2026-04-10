# ──────────────────────────────────────────────────────────────
# ElectroMancer Dev Container
# Base: Microsoft's universal devcontainer image
# Supports: Windows (Docker Desktop) & Linux Docker hosts
# ──────────────────────────────────────────────────────────────
FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# Avoid interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# ── System packages ────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    git \
    gnupg \
    lsb-release \
    ca-certificates \
    build-essential \
    unzip \
    jq \
    # PHP deps (feature installs PHP itself, but we want extra extensions)
    libpng-dev \
    libjpeg-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

# ── Cloudflare Wrangler CLI (global) ──────────────────────────
# Installed here so it's available immediately; the Node feature
# is applied by devcontainer.json on top of this layer.
# Wrangler is also installed in post-create.sh as a fallback.
RUN npm install -g wrangler@latest 2>/dev/null || true

# ── Set a sensible working directory ──────────────────────────
WORKDIR /workspace
