# Data Model – Modular Multi-Service Platform

## Overview
Relational schema centered on Service registration, routing, certificates, health status, and auditability. Designed for PostgreSQL.

## Entities
### service
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Internal identifier |
| service_name | text | unique, not null | Display & lookup name |
| owner_contact | text | not null | Team or person reference |
| primary_domain | text | unique, not null | External domain / FQDN |
| category | text | not null | Functional group (enum candidate) |
| container_image_ref | text | not null | Immutable image reference |
| business_purpose | text | not null | Business justification |
| support_channel | text | not null | Escalation path |
| compliance_tier | text | not null | Policy classification |
| requested_cert_type | text | not null | self-signed | external |
| health_check_path | text | not null | Relative path |
| state | text | index | Onboarding/Healthy/Degraded/Failed/OnboardingFailed/Retired |
| created_at | timestamptz | default now() | Creation time |
| updated_at | timestamptz | default now() | Mutation time |

### routing_rule
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | |
| service_id | UUID | FK→service(id) | Cascade delete on service removal (retired keeps snapshot separately) |
| domain | text | not null | Domain or subdomain |
| path_pattern | text | not null | Path glob or prefix |
| priority | int | not null | Lower → higher precedence |
| active | bool | not null | Enabled flag |
| created_at | timestamptz | | |

### certificate
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | |
| service_id | UUID | FK→service(id) | Nullable if shared cert later |
| cert_type | text | not null | self-signed | external |
| valid_from | timestamptz | not null | |
| valid_to | timestamptz | not null | |
| days_to_expiry_cache | int | | Precomputed for dashboard |
| pem_path | text | not null | Secure filesystem path |
| bundle_version | int | | Rotation overlap tracking |
| created_at | timestamptz | | |

### audit_event
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | |
| event_type | text | index | register/update/decommission/domain_change/cert_rotate/onboarding_timeout/health_state_change |
| service_id | UUID | FK→service(id) | Nullable for global events |
| actor | text | | User/automation origin |
| summary | text | | Human-readable summary |
| data | jsonb | | Structured payload |
| created_at | timestamptz | default now() | |

### health_snapshot
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | bigserial | PK | |
| service_id | UUID | FK→service(id) | |
| status | text | | Healthy/Degraded/Failed |
| latency_ms_p95 | int | | Aggregated value |
| error_rate | numeric(5,2) | | % errors in window |
| timestamp | timestamptz | index | Snapshot time |

### category_trend
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | bigserial | PK | |
| category | text | not null | |
| date | date | unique(category,date) | Daily snapshot date |
| service_count | int | | Active (non-Retired) services |
| healthy_count | int | | Healthy subset |
| degraded_count | int | | Degraded subset |
| failed_count | int | | Failed subset |

### service_state_transition
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | bigserial | PK | |
| service_id | UUID | FK→service(id) | |
| from_state | text | | Previous state |
| to_state | text | | New state |
| reason | text | | Optional context |
| created_at | timestamptz | default now() | |

## Relationships & Invariants
- service 1..* routing_rule (enforced via FK; active uniqueness ensures no conflicting domain+path for active rules).
- service 1..* certificate (allow multiple for rotation; at most one active overlapping bundle version).
- service 1..* health_snapshot (time-series).
- service 1..* audit_event.
- service 1..* service_state_transition.
- category_trend derived daily from service states.

## State Transition Rules
Onboarding → Healthy (first successful all checks)
Onboarding → OnboardingFailed (timeout or health failure after retry)
Healthy → Degraded (latency p95 > threshold or error_rate > threshold sustained window)
Degraded → Failed (continued degradation threshold breach)
Failed → Healthy (recovery window stable)
Any Active → Retired (decommission)

## Validation Constraints
- primary_domain unique; conflict detection pre-insert preview.
- category must be in maintained category set (Automation, Database, Dashboard, AI, SDLC, QLM, Dev).
- health_check_path must start with '/'.
- requested_cert_type in {self-signed, external}.
- service_name normalized (lowercase + hyphen) uniqueness.

## Retention Policies
- audit_event prune >180d (archive first).
- health_snapshot prune >30d (aggregate older to daily p95 & error summary optional future enhancement).

## Open Questions (Deferred)
- Multi-tenant namespace isolation (future scaling).
- Shared certificate objects for wildcard domains.

**Status**: Draft – produced Phase 1.
