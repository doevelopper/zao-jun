#!/usr/bin/env python3
import argparse
import sys
import json
import re
from pathlib import Path
import yaml
from jsonschema import validate, Draft7Validator, RefResolver

ROOT = Path(__file__).resolve().parents[2]
MODELS = ROOT / "src" / "models"

SCHEMAS = {
    "service": MODELS / "service.yaml",
    "domain": MODELS / "domain.yaml",
    "route": MODELS / "route.yaml",
}


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_schema(name: str):
    schema_path = SCHEMAS[name]
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)
    return schema


def error(msg: str):
    print(json.dumps({"ok": False, "error": msg}), file=sys.stderr)
    return 1


def ok(payload):
    print(json.dumps({"ok": True, **payload}, indent=2))
    return 0


def validate_item(item, schema, base_uri: str):
    resolver = RefResolver(base_uri=base_uri, referrer=schema)
    v = Draft7Validator(schema, resolver=resolver)
    errors = sorted(v.iter_errors(item), key=lambda e: e.path)
    return [f"{list(e.path)}: {e.message}" for e in errors]


def coerce_bool(val):
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        v = val.strip().lower()
        if v in {"true", "yes", "1"}: return True
        if v in {"false", "no", "0"}: return False
    return None


def parse_rule_to_url(rule: str) -> str | None:
    # Very lightweight parse for patterns like: Host(`home.local`) && PathPrefix(`/app`)
    try:
        host_match = re.search(r"Host\(`([^`]+)`\)", rule)
        path_match = re.search(r"PathPrefix\(`([^`]+)`\)", rule)
        host = host_match.group(1) if host_match else None
        path = path_match.group(1) if path_match else "/"
        if not host:
            return None
        if not path.startswith("/"):
            path = "/" + path
        return f"https://{host}{path}"
    except Exception:
        return None


def check_cert_policy(services: list[dict]) -> tuple[list[str], list[str]]:
    """
    Validate certificate placeholders in service.metadata per policy:
    - Production: cert_type must be org/ca, valid=true, chain_complete=true, expired=false
    - Non-prod: self-signed allowed, but still must be valid (not expired) with full chain for exposure
    Returns (errors, warnings)
    """
    errors: list[str] = []
    warnings: list[str] = []
    for i, s in enumerate(services):
        md = s.get("metadata") or {}
        env = (md.get("cert_env") or "dev").lower()
        ctype = (md.get("cert_type") or "self-signed").lower()
        valid = coerce_bool(md.get("cert_valid"))
        chain = coerce_bool(md.get("cert_chain_complete"))
        expired = coerce_bool(md.get("cert_expired"))

        missing_keys = [k for k in ("cert_env","cert_type","cert_valid","cert_chain_complete","cert_expired") if k not in md]
        if missing_keys:
            warnings.append(f"service[{i}] {s.get('name')}: missing cert metadata keys: {', '.join(missing_keys)}")
            # Continue policy evaluation only on provided values

        # Treat missing booleans as unknown (warn), but do not block unless clear violation
        if env == "production":
            if ctype not in {"org", "ca", "ca-signed", "internal-pki", "pki"}:
                errors.append(f"service[{i}] {s.get('name')}: self-signed not permitted in production")
        # In all envs, invalid/expired/chain-missing blocks exposure
        if valid is False:
            errors.append(f"service[{i}] {s.get('name')}: certificate invalid per placeholder")
        if expired is True:
            errors.append(f"service[{i}] {s.get('name')}: certificate expired per placeholder")
        if chain is False:
            errors.append(f"service[{i}] {s.get('name')}: certificate chain incomplete per placeholder")

    return errors, warnings


def build_homepage_preview(domains: list[dict], services: list[dict]):
    domain_index = {d.get("name"): {"name": d.get("name"), "services": []} for d in domains}
    for s in services:
        dom = s.get("domain")
        item = {
            "name": s.get("name"),
            "status": s.get("health"),
            "visibility": s.get("visibility", "public"),
            "link": None,
            "link_enabled": False,
        }
        # Try first route to construct a URL
        routes = s.get("routes", [])
        if routes:
            url = parse_rule_to_url(routes[0].get("rule", ""))
            item["link"] = url
        item["link_enabled"] = (s.get("health") == "healthy") and bool(item["link"])

        # Place under known domain, else collect under a special bucket
        bucket = domain_index.get(dom)
        if not bucket:
            bucket = domain_index.setdefault("__unknown__", {"name": "__unknown__", "services": []})
        bucket["services"].append(item)

    # Return list preserving domain names
    return list(domain_index.values())


def main():
    parser = argparse.ArgumentParser(description="Validate catalog (domains/services)")
    parser.add_argument("catalog", type=Path, help="Path to catalog folder with domains/services YAML")
    parser.add_argument("--check-certs", action="store_true", help="Validate certificate policy placeholders from service.metadata")
    parser.add_argument("--homepage-preview", action="store_true", help="Generate homepage preview JSON from catalog")
    parser.add_argument("--output", type=Path, help="Optional path to write homepage preview JSON")
    args = parser.parse_args()

    catalog_dir = args.catalog
    if not catalog_dir.exists() or not catalog_dir.is_dir():
        return error(f"Catalog dir not found: {catalog_dir}")

    # Load schemas
    service_schema = load_schema("service")
    domain_schema = load_schema("domain")

    # Load catalog files
    domains_path = catalog_dir / "domains.example.yaml"
    services_path = catalog_dir / "services.example.yaml"

    if not domains_path.exists() or not services_path.exists():
        return error("Expected domains.example.yaml and services.example.yaml in catalog directory")

    domains = load_yaml(domains_path)
    services = load_yaml(services_path)

    # Normalize to lists if single objects provided
    if isinstance(domains, dict):
        domains = [domains]
    if isinstance(services, dict):
        services = [services]

    # Validate domains
    domain_names = set()
    domain_errors = []
    for i, d in enumerate(domains):
        errs = validate_item(d, domain_schema, base_uri=f"file://{MODELS}/")
        if errs:
            domain_errors.extend([f"domain[{i}] {e}" for e in errs])
        name = d.get("name")
        if name in domain_names:
            domain_errors.append(f"domain[{i}] duplicate name: {name}")
        else:
            domain_names.add(name)

    # Validate services
    service_names = set()
    route_rules = set()
    service_errors = []
    for i, s in enumerate(services):
        errs = validate_item(s, service_schema, base_uri=f"file://{MODELS}/")
        if errs:
            service_errors.extend([f"service[{i}] {e}" for e in errs])
        name = s.get("name")
        if name in service_names:
            service_errors.append(f"service[{i}] duplicate name: {name}")
        else:
            service_names.add(name)
        # domain existence
        dom = s.get("domain")
        if dom not in domain_names:
            service_errors.append(f"service[{i}] unknown domain: {dom}")
        # route uniqueness
        for r in s.get("routes", []) :
            rule = r.get("rule")
            if rule in route_rules:
                service_errors.append(f"service[{i}] duplicate route rule: {rule}")
            else:
                route_rules.add(rule)

    all_errors = domain_errors + service_errors

    cert_warnings: list[str] = []
    if args.check_certs:
        cert_errors, cert_warnings = check_cert_policy(services)
        all_errors.extend(cert_errors)

    if all_errors:
        print(json.dumps({"ok": False, "errors": all_errors, "warnings": cert_warnings}, indent=2))
        return 1

    payload = {
        "domains": len(domain_names),
        "services": len(service_names),
        "unique_route_rules": len(route_rules),
        "warnings": cert_warnings,
    }
    if args.homepage_preview:
        preview = build_homepage_preview(domains, services)
        payload["homepage_preview"] = preview
        if args.output:
            try:
                args.output.write_text(json.dumps(preview, indent=2))
            except Exception as e:
                return error(f"Failed writing preview to {args.output}: {e}")

    return ok(payload)


if __name__ == "__main__":
    sys.exit(main())
