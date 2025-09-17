# Phase 0 Research – Modular Multi-Service Platform

## Scope
Resolve remaining technology selection & operational unknowns to enable Phase 1 design (data model & contracts) without ambiguity.

## Decision Log
### 1. Runtime & Orchestration
Decision: Docker Compose (single host / small cluster) baseline.
Rationale: Minimal overhead, matches stated scope; fast iteration.
Alternatives: K8s (overkill), Nomad (adds ops complexity), Podman (similar value, less pervasive docs).

### 2. Metadata Persistence
Decision: PostgreSQL (single instance) for service metadata, audit, routing rules, category trends.
Rationale: Relational integrity (unique constraints for domain collisions), time-series capable via simple partitioning or daily snapshots.
Alternatives: SQLite (concurrency risk), Redis (persistence semantics), Document store (complex unique constraints).

### 3. Audit & Logging Strategy
Decision: Structured JSON lines persisted to Postgres (audit_events table) plus optional file-based rolling logs for tail/debug.
Rationale: Queryability + compliance retention rules; no external ELK dependency at MVP.
Alternatives: ELK/Opensearch (resource heavy), Loki (would add extra stack complexity).

### 4. Certificate Lifecycle
Decision: Self-signed root + per-domain cert generation via scripted OpenSSL; external cert import path accepted (stored encrypted at rest).
Rationale: Control + simplicity; matches requirement for self-signed support.
Alternatives: ACME integration (deferred), HashiCorp Vault PKI (operational overhead).

### 5. Health Aggregation Interval
Decision: 60s scheduled poll with on-demand manual refresh trigger.
Rationale: Balances freshness vs resource consumption; meets ≤60s requirement.
Alternatives: Event streaming (adds complexity), shorter interval (<30s) increases overhead.

### 6. Dashboard Delivery
Decision: Static assets (HTML/CSS/vanilla JS) served by gateway; JSON endpoint consumed for dynamic updates.
Rationale: No framework build pipeline; low latency and simple deploy.
Alternatives: SPA framework (React/Vue) not justified for small surface.

### 7. Throttling Policy Implementation
Decision: Implement at gateway layer using request counters + sliding window; degrade to 429 after policy threshold.
Rationale: Central vantage; uniform enforcement.
Alternatives: Per-service sidecar (duplicated logic), host firewall (coarse-grained).

### 8. Domain Collision & Wildcard Precedence
Decision: DB constraint + deterministic comparator (specificity > feature number order). Preview endpoint simulates before commit.
Alternatives: First-come-first-serve only (harder to reason about), manual review (slower onboarding).

### 9. Service State Machine
Decision: Enumerated states: Onboarding, Healthy, Degraded, Failed, OnboardingFailed, Retired. Transitions validated centrally.
Alternatives: Free-form status string (error-prone), implicit states (hidden logic).

### 10. Metrics Set (Minimum Viable)
Decision: request_count, error_rate, latency_p50/p95/p99, cert_days_to_expiry, health_pass_rate, onboarding_duration, routing_change_events.
Rationale: Directly map to FR observability and dashboard needs.
Alternatives: Add CPU/memory per service later (requires deeper host integration).

### 11. Data Retention Enforcement
Decision: Scheduled daily retention job: prune >180d audit hot entries (archive export), rotate log archives, maintain category trend snapshots.
Alternatives: On-write triggers (complex), external archival system (deferred).

### 12. Contract Style
Decision: REST JSON endpoints; OpenAPI 3.1 spec in `contracts/openapi.yaml` + per-endpoint example stubs.
Rationale: Simplicity; wide tool support; low barrier for contract tests.
Alternatives: GraphQL (overhead), gRPC (binary complexity).

## Outstanding (Deferred) – Not Blocking Phase 1
- ACME certificate automation integration.
- Multi-node coordination (consensus) for state updates.
- Advanced performance tuning (latency instrumentation beyond aggregation baseline).
- Rich analytics (beyond category trends).

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Single Postgres instance failure | Platform metadata loss | Daily backups + export script |
| Certificate renewal script failure | Service TLS warnings | Multi-step warnings & critical alert + manual regenerate CLI |
| Throttling false positives under burst | User-facing 429 | Adaptive window tuning + log sampling |
| Health check flapping | Status instability | Two consecutive failures threshold before state change |
| Domain propagation delay >10m | SLA breach | Alert + manual verification procedure |

## Research Closure
All previously flagged unknowns now have concrete decisions; proceed to Phase 1 design.

**Status**: COMPLETE
