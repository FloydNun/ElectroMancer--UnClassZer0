import { useState, useEffect } from "react";
import "./App.css";

const WORKER_URL = import.meta.env.VITE_WORKER_URL || "http://localhost:8787";

function StatusBadge({ label, url, port }) {
  return (
    <div className="badge">
      <span className="badge__dot" />
      <span className="badge__label">{label}</span>
      <code className="badge__port">:{port}</code>
    </div>
  );
}

function ApiDemo() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const callWorker = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${WORKER_URL}/api/hello`);
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setError(
        "Could not reach the Worker. Make sure `wrangler dev` is running (port 8787)."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card">
      <h2>☁️ Cloudflare Worker API Demo</h2>
      <p>
        Click the button to call the local Cloudflare Worker running on port{" "}
        <code>8787</code>.
      </p>
      <button className="btn" onClick={callWorker} disabled={loading}>
        {loading ? "Calling…" : "Call Worker /api/hello"}
      </button>
      {response && (
        <pre className="response">{JSON.stringify(response, null, 2)}</pre>
      )}
      {error && <p className="error">{error}</p>}
    </section>
  );
}

function GitHubAiDemo() {
  const [prompt, setPrompt] = useState("Explain React in one sentence.");
  const [reply, setReply] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const askAI = async () => {
    setLoading(true);
    setError(null);
    setReply(null);
    try {
      // Calls through the Cloudflare Worker which proxies GitHub Models API
      const res = await fetch(`${WORKER_URL}/api/ai`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      setReply(data.reply || JSON.stringify(data));
    } catch (err) {
      setError(
        "Could not reach the AI proxy Worker. Make sure `wrangler dev` is running and GITHUB_TOKEN is set."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card">
      <h2>🤖 GitHub AI (via Worker proxy)</h2>
      <p>
        Ask a question and the Cloudflare Worker will proxy it to{" "}
        <strong>GitHub Models API</strong>.
      </p>
      <textarea
        className="textarea"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        rows={3}
      />
      <button className="btn" onClick={askAI} disabled={loading || !prompt}>
        {loading ? "Thinking…" : "Ask GitHub AI ✨"}
      </button>
      {reply && <pre className="response">{reply}</pre>}
      {error && <p className="error">{error}</p>}
    </section>
  );
}

export default function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="app">
      <header className="hero">
        <h1>⚡ ElectroMancer</h1>
        <p className="tagline">React · Vite · Cloudflare Pages · GitHub AI</p>
      </header>

      <main className="container">
        <section className="card">
          <h2>🚀 Services Running</h2>
          <div className="badges">
            <StatusBadge label="Vite (React)" port="5173" />
            <StatusBadge label="Cloudflare Worker" port="8787" />
            <StatusBadge label="Live Server" port="5500" />
            <StatusBadge label="Flask (Python)" port="5000" />
            <StatusBadge label="PHP Server" port="8000" />
          </div>
        </section>

        <section className="card">
          <h2>⚛️ React Counter</h2>
          <p>Interactive demo – click to increment:</p>
          <button className="btn btn--count" onClick={() => setCount((c) => c + 1)}>
            Count: {count}
          </button>
        </section>

        <ApiDemo />
        <GitHubAiDemo />
      </main>

      <footer className="footer">
        <p>
          ElectroMancer · UnClassZer0 · AI SuperFriends Team ·{" "}
          <a
            href="https://github.com/FloydNun/ElectroMancer--UnClassZer0"
            target="_blank"
            rel="noreferrer"
          >
            GitHub
          </a>
        </p>
      </footer>
    </div>
  );
}
