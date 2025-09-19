#!/usr/bin/env python3
import argparse
import sys
import json
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
    print(json.dumps({"ok": True, **payload}))
    return 0


def validate_item(item, schema, base_uri: str):
    resolver = RefResolver(base_uri=base_uri, referrer=schema)
    v = Draft7Validator(schema, resolver=resolver)
    errors = sorted(v.iter_errors(item), key=lambda e: e.path)
    return [f"{list(e.path)}: {e.message}" for e in errors]


def main():
    parser = argparse.ArgumentParser(description="Validate catalog (domains/services)")
    parser.add_argument("catalog", type=Path, help="Path to catalog folder with domains/services YAML")
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
    if all_errors:
        print(json.dumps({"ok": False, "errors": all_errors}, indent=2))
        return 1

    return ok({
        "domains": len(domain_names),
        "services": len(service_names),
        "unique_route_rules": len(route_rules)
    })


if __name__ == "__main__":
    sys.exit(main())
