# Validation Rules

This document defines validation rules that must pass before exposing or updating services.

## Global Uniqueness
- Service.name MUST be globally unique.
- Route.rule MUST be globally unique.

## Required Fields
- Service requires: name, domain, routes[>=1], health, visibility.
- Route requires: rule.
- Domain requires: name.

## Health and Visibility
- health ∈ { healthy, degraded, unavailable }
- visibility ∈ { public, restricted }
- Homepage links disabled when status != healthy.

## Certificate Policy
- Production: internal PKI or CA-signed certificates only.
- Non-production (dev/lab): self-signed allowed on isolated networks.
- Invalid/missing certificates: withhold exposure; emit AuditEvent(policy_violation).

## Access Control
- Domains may define accessGroups (RBAC/GBAC); viewers without access must not see restricted services.

## Change Safety and Rollback
- Reject changes introducing name/route conflicts.
- Maintain previous working configuration; on failure, rollback atomically.

## Auditability
- Emit AuditEvent(create|update|remove|policy_violation) with timestamp, actor, and details.
