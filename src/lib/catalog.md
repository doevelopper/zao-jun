# Catalog Structure

The catalog collects domain and service metadata used to drive discovery and routing.

## Layout
- Domains: list of `Domain` objects (see src/models/domain.yaml)
- Services: list of `Service` objects (see src/models/service.yaml)

## Rules
- Each Service.domain must refer to an existing Domain.name.
- Service and Route uniqueness enforced globally.
- Metadata may include owner or other labels for governance.

## Loading
- Catalog may be loaded from YAML files (e.g., specs/.../catalog/*.yaml) for validation and testing.
- Validation must run before activation; conflicts reject the change.

## Output
- Homepage entries derived from Service and health status.
- Routing configuration derived from Service.routes.
