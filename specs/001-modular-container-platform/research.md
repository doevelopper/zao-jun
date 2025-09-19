# Research Summary

This document consolidates decisions and rationale for the Modular Container Platform.

## Decisions

1. Single Secure Entry Point
- Decision: All external traffic terminates TLS at a single edge; no direct host port exposure by services.
- Rationale: Centralized policy enforcement, simplified security posture, smaller blast radius.
- Alternatives: Per-service exposure (rejected: inconsistent policy and increased attack surface).

2. Metadata-Driven Routing
- Decision: Declarative metadata defines name, domain, and route; conflicts are rejected.
- Rationale: Repeatability, auditable configuration, minimal manual ops.
- Alternatives: Manual routing edits (rejected: error-prone, slow onboarding).

3. Certificates Policy
- Decision: Prod uses organization-approved certificates; self-signed allowed only in dev/lab on isolated networks; invalid/missing certs block exposure.
- Rationale: Security and trust for production while enabling local development.
- Alternatives: Allow self-signed in prod (rejected: security risk).

4. Access Control
- Decision: Authentication via org SSO; authorization via RBAC/GBAC mapped to domains; least privilege.
- Rationale: Consistent identity and scoped access.
- Alternatives: Per-service auth models (rejected: fragmentation, higher ops load).

5. Observability
- Decision: Structured logs with ≥14-day retention (90 days recommended), metrics at ≤60s with basic dashboards.
- Rationale: Troubleshooting, capacity planning, reliability.
- Alternatives: Ad-hoc logging (rejected: low debuggability, compliance gaps).

6. Scale Targets
- Decision: Support ~100 services with <1s homepage render; paginate/group beyond.
- Rationale: Practical single-host target.
- Alternatives: Unlimited services (rejected: impractical without scaling the platform).

## Open Items
- None; all clarifications finalized in the spec and constitution.

## References
- Feature Spec: ../spec.md
- Constitution: ../../.specify/memory/constitution.md
