/**
 * ElectroMancer – Cloudflare Worker
 *
 * Endpoints:
 *   GET  /           → info page
 *   GET  /api/hello  → JSON greeting
 *   GET  /api/status → health check
 *   POST /api/ai     → GitHub Models API proxy (requires GITHUB_TOKEN secret)
 *
 * Local dev:
 *   cd cloudflare && wrangler dev
 *
 * Deploy:
 *   cd cloudflare && wrangler deploy
 */

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...CORS_HEADERS,
    },
  });
}

async function handleAI(request, env) {
  if (!env.GITHUB_TOKEN) {
    return jsonResponse(
      {
        error:
          "GITHUB_TOKEN secret not set. Add it with `wrangler secret put GITHUB_TOKEN` or in a .dev.vars file.",
      },
      503
    );
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return jsonResponse({ error: "Invalid JSON body" }, 400);
  }

  const prompt = body.prompt || "Say hello!";
  const model = body.model || "gpt-4o-mini";

  // GitHub Models API is OpenAI-compatible
  const aiRes = await fetch("https://models.inference.ai.azure.com/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${env.GITHUB_TOKEN}`,
    },
    body: JSON.stringify({
      model,
      messages: [
        {
          role: "system",
          content:
            "You are a helpful AI assistant for the ElectroMancer project. Be concise.",
        },
        { role: "user", content: prompt },
      ],
      max_tokens: 512,
    }),
  });

  if (!aiRes.ok) {
    const errText = await aiRes.text();
    return jsonResponse(
      { error: `GitHub Models API error ${aiRes.status}`, detail: errText },
      aiRes.status
    );
  }

  const aiData = await aiRes.json();
  const reply = aiData.choices?.[0]?.message?.content ?? "(no reply)";

  return jsonResponse({ reply, model, prompt });
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const { pathname, method } = { pathname: url.pathname, method: request.method };

    // ── CORS pre-flight ────────────────────────────────────────
    if (method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    // ── Routes ─────────────────────────────────────────────────
    if (pathname === "/" || pathname === "") {
      return new Response(
        `<h1>⚡ ElectroMancer Cloudflare Worker</h1>
         <p>Endpoints: <code>/api/hello</code> · <code>/api/status</code> · <code>POST /api/ai</code></p>`,
        { headers: { "Content-Type": "text/html", ...CORS_HEADERS } }
      );
    }

    if (pathname === "/api/hello") {
      return jsonResponse({
        message: "Hello from ElectroMancer Cloudflare Worker! ⚡☁️",
        runtime: "Cloudflare Workers",
        timestamp: new Date().toISOString(),
      });
    }

    if (pathname === "/api/status") {
      return jsonResponse({
        status: "ok",
        timestamp: new Date().toISOString(),
        region: request.cf?.colo ?? "local",
        country: request.cf?.country ?? "unknown",
      });
    }

    if (pathname === "/api/ai" && method === "POST") {
      return handleAI(request, env);
    }

    return jsonResponse({ error: "Not found", path: pathname }, 404);
  },
};
