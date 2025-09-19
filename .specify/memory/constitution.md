# Zao-Jun Platform Constitution

## Core Principles

### I. Single Secure Entry Point (Zero-Trust Edge)
All external traffic MUST pass through a single entry point with TLS termination. No service may expose host ports directly. This ensures consistent policy enforcement, auditability, and blast-radius reduction.

### II. Metadata-Driven Service Exposure
Service discovery and routing are declarative. Services declare name, domain grouping, and route rules via metadata. Manual routing edits are prohibited; conflicts are rejected with actionable errors.

### III. 10-Minute Onboarding Standard
Onboarding a new service from template to live exposure MUST be achievable in under 10 minutes for a trained user. Templates and documentation are mandatory and kept current.

### IV. Domain-Oriented Organization
Services are organized by domain for navigation and access policies. The homepage reflects domain groupings and surfaces service health and entry links.

### V. No Direct Port Exposure
Only the platform’s edge may bind externally. Any attempt to expose container ports directly is blocked, logged as an audit event, and flagged to platform administrators.

### VI. Observability by Default
Structured logs and basic metrics are mandatory. Centralized logging retains at least 14 days (90 days recommended). Metrics are collected at ≤60s intervals with dashboards for availability, latency, error rates, and resource usage.

### VII. Safety, Validation, and Rollback
All changes are validated before activation. Conflicting or invalid definitions are rejected. Rollback MUST be available to restore prior working configurations if a change degrades availability.

### VIII. Certificates Policy
Production endpoints require organization-approved certificates (internal PKI or CA-signed). Self-signed certificates are permitted only in development and lab/staging on isolated networks. Endpoints with invalid/missing certificates are withheld from exposure and audited.

### IX. Access Control and Least Privilege
Access is governed by roles and groups mapped to domains. Platform Admins have full control; Service Owners manage services within assigned domains; Viewers have read-only access. Principle of least privilege applies to all operations.

### X. Simplicity and Scope Discipline
Prefer the simplest approach that satisfies requirements. Avoid premature optimization and unnecessary coupling. The platform’s scope is service exposure, organization, and observability readiness—not bespoke service configuration.

## Security & Performance Standards

### Security Requirements
- Zero direct port exposure from services to the host.
- Centralized TLS termination; per-service policies enforced at the edge.
- Audit events recorded for create/update/remove, policy violations, and certificate issues.
- Authentication via organization SSO; authorization via RBAC/GBAC mapped to domains.

### Certificate Handling
- Production: internal PKI or CA-signed certificates only.
- Non-production: self-signed allowed on isolated networks.
- Invalid/missing certificates: block exposure for the affected endpoint and emit audit events.

### Performance Targets
- Homepage renders in <1s with up to ~100 exposed services on a single host.
- Routing/discovery updates propagate without manual restarts.
- Onboarding time: <10 minutes from template to live exposure for a trained user.

### Reliability & Recovery
- Health checks determine service availability; unhealthy services are not advertised as available.
- Rollback available for configuration changes causing unavailability.
- Platform components restart automatically on failure to maintain availability.

## Development Workflow & Quality Gates

### Workflow
1. Specify: Feature specs state user value and constraints (no implementation details).
2. Plan: Tasks and acceptance criteria derived from the spec.
3. Implement: Changes adhere to principles and pass quality gates.

### Review Process
- Specs must include user scenarios, functional requirements, and clear boundaries.
- All routes and service names must be unique; conflicts are rejected.
- Security checks: no host port exposure; certificate policy compliance; RBAC mappings in place.
- Observability checks: structured logs and metrics enabled for new/changed services.

### Quality Gates (Non-Negotiable)
- Single entry point enforced; no direct ports.
- Metadata validation passes with no unresolved conflicts.
- Audit logging enabled for relevant actions.
- Rollback procedure documented and verifiable.
- Documentation updated: templates, onboarding guide, and homepage listing.

## Governance

- This Constitution supersedes other project practices when conflicts arise.
- Amendments require: written proposal, review approval by Platform Admins, documented migration/rollback plan, and updated version/date.
- All pull requests must certify compliance with Core Principles and Quality Gates.
- Complexity must be justified against Simplicity and Scope Discipline.
- Use this Constitution as the single source of truth for platform rules and expectations.

**Version**: 1.0.0 | **Ratified**: 2025-09-19 | **Last Amended**: 2025-09-19