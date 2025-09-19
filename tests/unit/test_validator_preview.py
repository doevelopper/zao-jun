import json
from pathlib import Path

from src.cli.validate_catalog import parse_rule_to_url, build_homepage_preview


def test_parse_rule_to_url():
    # Valid rule
    rule = "Host(`home.local`) && PathPrefix(`/app`)"
    assert parse_rule_to_url(rule) == "https://home.local/app"

    # No path defaults to '/'
    rule2 = "Host(`example.org`)"
    assert parse_rule_to_url(rule2) == "https://example.org/"

    # Missing host returns None
    rule3 = "PathPrefix(`/only`)"
    assert parse_rule_to_url(rule3) is None


def test_build_homepage_preview_includes_domain_theming(tmp_path: Path):
    domains = [
        {"name": "Core", "color": "#22c55e", "icon": "🧭", "logo": None},
        {"name": "Aux"},
    ]
    services = [
        {
            "name": "Home",
            "domain": "Core",
            "health": "healthy",
            "routes": [
                {"name": "ui", "rule": "Host(`home.local`) && PathPrefix(`/`)"}
            ],
        },
        {
            "name": "Orphan",
            "domain": "Unknown",
            "health": "unavailable",
            "routes": [
                {"name": "ui", "rule": "Host(`missing.local`) && PathPrefix(`/ui`)"}
            ],
        },
    ]

    preview = build_homepage_preview(domains, services)
    # It should include the Core domain with theming
    core = next((d for d in preview if d["name"] == "Core"), None)
    assert core is not None
    assert core["color"] == "#22c55e"
    assert core["icon"] == "🧭"

    # Orphan service goes under __unknown__
    unknown = next((d for d in preview if d["name"] == "__unknown__"), None)
    assert unknown is not None
    assert any(s["name"] == "Orphan" for s in unknown["services"]) 
