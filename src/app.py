"""
ElectroMancer – Python Flask starter app
Run: python app.py
Visit: http://localhost:5000
"""

from flask import Flask, jsonify, render_template_string
import datetime

app = Flask(__name__)

# ── Simple HTML template (inline so the file is self-contained) ──
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>ElectroMancer – Python API</title>
  <link rel="stylesheet" href="/static/styles.css" />
</head>
<body>
  <header class="hero">
    <div class="hero__inner">
      <h1>⚡ ElectroMancer</h1>
      <p class="tagline">Python · Flask · Dev Container</p>
    </div>
  </header>
  <main class="container">
    <section class="card">
      <h2>🐍 Flask App Running</h2>
      <p>Server time: <strong>{{ server_time }}</strong></p>
      <p>Try the REST API endpoints below:</p>
      <ul>
        <li><a href="/api/hello" style="color:var(--clr-accent)">GET /api/hello</a></li>
        <li><a href="/api/status" style="color:var(--clr-accent)">GET /api/status</a></li>
      </ul>
    </section>
  </main>
</body>
</html>
"""


@app.route("/")
def index():
    server_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    return render_template_string(INDEX_HTML, server_time=server_time)


@app.route("/api/hello")
def hello():
    return jsonify(
        {
            "message": "Hello from ElectroMancer Python API! ⚡",
            "framework": "Flask",
            "python_version": "3.12+",
        }
    )


@app.route("/api/status")
def status():
    return jsonify(
        {
            "status": "ok",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "services": {
                "python_flask": "running",
                "dev_container": "active",
            },
        }
    )


if __name__ == "__main__":
    # debug=True enables hot-reload (live preview for Python changes)
    app.run(host="0.0.0.0", port=5000, debug=True)
