#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from html import escape

def render_html(preview: list[dict]) -> str:
    def card(service):
        status = service.get("status", "unknown")
        link = service.get("link")
        enabled = service.get("link_enabled")
        name = escape(service.get("name", ""))
        badge_color = {
            "healthy": "#22c55e",
            "degraded": "#f59e0b",
            "unavailable": "#ef4444",
        }.get(status, "#9ca3af")
        link_html = (
            f'<a href="{escape(link)}" class="btn" style="opacity:{1.0 if enabled else 0.5}" ' \
            f'{"" if enabled else "aria-disabled=\"true\" tabindex=\"-1\""}>' \
            f"Open</a>" if link else ""
        )
        return f"""
        <div class=card>
          <div class=card-header>
            <span class=name>{name}</span>
            <span class=badge style=\"background:{badge_color}\">{status}</span>
          </div>
          <div class=card-body>
            <div class=link>{link_html}</div>
          </div>
        </div>
        """

    domains_html = []
    for d in preview:
        domain_name = escape(d.get("name", ""))
        services = d.get("services", [])
        services_html = "\n".join(card(s) for s in services)
        domains_html.append(f"""
        <section class=domain>
          <h2>{domain_name}</h2>
          <div class=grid>
            {services_html}
          </div>
        </section>
        """)

    content = "\n".join(domains_html)

    return f"""
<!doctype html>
<html lang=en>
<head>
  <meta charset=utf-8>
  <meta name=viewport content="width=device-width, initial-scale=1">
  <title>Zao-Jun Homepage</title>
  <style>
    :root {{ --bg:#0b1020; --fg:#e5e7eb; --muted:#9ca3af; --card:#111827; --grid:repeat(auto-fill,minmax(220px,1fr)); }}
    html,body {{ margin:0; padding:0; background:var(--bg); color:var(--fg); font-family:system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Arial, "Apple Color Emoji", "Segoe UI Emoji"; }}
    header {{ padding:24px 32px; border-bottom:1px solid #1f2937; position:sticky; top:0; background:rgba(11,16,32,.9); backdrop-filter: blur(6px); }}
    h1 {{ margin:0; font-size:20px; letter-spacing:.02em; }}
    main {{ padding:24px 32px; max-width:1200px; margin:0 auto; }}
    h2 {{ margin:24px 0 12px; font-size:16px; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; }}
    .grid {{ display:grid; grid-template-columns: var(--grid); gap:16px; }}
    .card {{ background:var(--card); border:1px solid #1f2937; border-radius:12px; overflow:hidden; display:flex; flex-direction:column; }}
    .card-header {{ display:flex; align-items:center; justify-content:space-between; padding:12px 14px; border-bottom:1px solid #1f2937; }}
    .name {{ font-weight:600; }}
    .badge {{ color:#0b1020; font-size:12px; padding:2px 8px; border-radius:999px; text-transform:capitalize; }}
    .card-body {{ padding:12px 14px; }}
    .btn {{ display:inline-block; background:#2563eb; color:white; text-decoration:none; padding:8px 10px; border-radius:8px; font-weight:600; }}
    footer {{ padding:24px 32px; color:var(--muted); border-top:1px solid #1f2937; margin-top:24px; }}
  </style>
</head>
<body>
  <header>
    <h1>Zao-Jun — Services</h1>
  </header>
  <main>
    {content}
  </main>
  <footer>
    Generated from homepage-preview.json
  </footer>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Generate static HTML homepage from preview JSON")
    parser.add_argument("preview", type=Path, help="Path to homepage-preview.json")
    parser.add_argument("--output", type=Path, default=Path("homepage.html"), help="Output HTML file path")
    args = parser.parse_args()

    data = json.loads(args.preview.read_text(encoding="utf-8"))
    html = render_html(data)
    args.output.write_text(html, encoding="utf-8")
    print(json.dumps({"ok": True, "output": str(args.output)}))

if __name__ == "__main__":
    main()
