import json
from pathlib import Path

from src.cli.generate_homepage import render_html


def test_render_html_contains_domain_and_service():
    preview = [
        {
            "name": "Core",
            "color": "#22c55e",
            "icon": "🧭",
            "services": [
                {
                    "name": "Home",
                    "status": "healthy",
                    "visibility": "public",
                    "link": "https://home.local/",
                    "link_enabled": True,
                }
            ],
        }
    ]

    html = render_html(preview)
    # contains domain header and service name
    assert "Core" in html
    assert "Home" in html
    # contains Open button link
    assert "https://home.local/" in html
    # contains accent color variable usage
    assert "--accent:#22c55e" in html or "#22c55e" in html
