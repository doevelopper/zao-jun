# Tasks – Modular Multi-Service Container Hosting Platform

Branch: `001-modular-platform-to`
Source Artifacts: spec.md, plan.md, research.md, data-model.md, contracts/openapi.yaml, quickstart.md

Legend: [P] = Can execute in parallel with other [P] tasks (different files / independent)

## Ordering Principles
1. Environment & scaffolding
2. Schema & migration definitions (models)
3. Contract test stubs (fail first)
4. Integration & scenario tests (fail)
5. Core implementation to pass contract tests
6. Supporting features (health aggregation, certificate lifecycle, throttling)
7. Dashboard & status feed
8. Observability & retention jobs
9. Polishing & documentation

## Tasks

### Setup & Tooling
T001. Initialize project source structure (`src/`, `tests/contract`, `tests/integration`, `tests/unit`, `scripts/`) – create directories and placeholder README in each.
T002. Add base configuration: `pyproject.toml` (if Python chosen) or alternative tool manifest; include dependencies: postgres driver, HTTP framework (to decide in implementation), testing libs (pytest), OpenAPI validation library. (Depends: T001)
T003. Create `.env.example` with required variables (DB_URL, CERT_DIR, LOG_LEVEL, DASH_REFRESH_INTERVAL). (Depends: T001)
T004. Implement bootstrap script `scripts/dev_up.sh` for starting compose stack (gateway, router, postgres, placeholder app container). (Depends: T001)
T005. Add lint/format config (ruff/black or shellcheck for scripts) and CI placeholder. (Depends: T002)

### Data Model & Migrations (Models before services)
T006. Define migration file `migrations/001_init.sql` creating tables: service, routing_rule, certificate, audit_event, health_snapshot, category_trend, service_state_transition. (Depends: T002)
T007. Add unique constraints & indexes (domain uniqueness, service_name uniqueness, category_trend composite). (Depends: T006)
T008. Implement model layer (ORM or query module) `src/models/service.py` basic CRUD + state transition helper. (Depends: T006)
T009. Implement model modules for routing_rule, certificate. (Depends: T006) [P]
T010. Implement model modules for audit_event, service_state_transition. (Depends: T006) [P]
T011. Implement model modules for health_snapshot, category_trend. (Depends: T006) [P]
T012. Add retention job SQL scripts (audit prune >180d, health_snapshot prune >30d). (Depends: T006)

### Contract Tests (Failing First)
T013. Add contract test `tests/contract/test_register_service.py` validating POST /services schema & required fields. (Depends: T006)
T014. Add contract test `tests/contract/test_list_services.py` (GET /services filters status/category). (Depends: T006) [P]
T015. Add contract test `tests/contract/test_get_service.py`. (Depends: T006) [P]
T016. Add contract test `tests/contract/test_update_service.py`. (Depends: T006) [P]
T017. Add contract test `tests/contract/test_decommission_service.py`. (Depends: T006) [P]
T018. Add contract test `tests/contract/test_domain_reassign.py` (POST /services/{id}/domain). (Depends: T006) [P]
T019. Add contract test `tests/contract/test_routing_preview.py`. (Depends: T006) [P]
T020. Add contract test `tests/contract/test_status_feed.py`. (Depends: T006) [P]
T021. Add contract test `tests/contract/test_audit_events.py`. (Depends: T006) [P]
T022. Add contract test `tests/contract/test_category_trends.py`. (Depends: T006) [P]
T023. Add contract test `tests/contract/test_certificate_info_future.py` (placeholder for future certificate metadata endpoint). (Depends: T006) [P]

### Integration / Scenario Tests (User Stories & Quickstart)
T024. Integration test onboarding flow: register → polling → Healthy transition (`tests/integration/test_onboarding_flow.py`). (Depends: T013)
T025. Integration test routing collision prevention with preview rejection. (Depends: T019)
T026. Integration test certificate expiry warning schedule simulation (fast-forward time). (Depends: T012)
T027. Integration test decommission path (register → decommission → no routing). (Depends: T017)
T028. Integration test dashboard JSON parity vs HTML listing (status feed vs rendered). (Depends: T020)
T029. Integration test state transitions (Healthy → Degraded → Failed → Healthy). (Depends: T011)
T030. Integration test throttling response (sustained load triggers 429). (Depends: T024)
T031. Integration test retention job pruning audit & health snapshots (time travel). (Depends: T012)

### Core Service Implementation
T032. Implement DB connection & migration runner utility (`src/lib/db.py`). (Depends: T006)
T033. Implement service registration endpoint logic (validations, storage, initial audit). (Depends: T013,T008)
T034. Implement list services endpoint with filtering & pagination. (Depends: T014,T008)
T035. Implement get service endpoint. (Depends: T015,T008)
T036. Implement update service metadata endpoint (validate allowed fields). (Depends: T016,T008)
T037. Implement decommission endpoint (state transition + routing cleanup + audit). (Depends: T017,T008,T010)
T038. Implement domain reassign endpoint (collision check + audit). (Depends: T018,T008,T009)
T039. Implement routing preview endpoint (simulate conflict, priority resolution). (Depends: T019,T009)
T040. Implement status feed endpoint (aggregate latest health + certificate expiry days). (Depends: T020,T011,T009,T008)
T041. Implement audit events listing endpoint with filtering. (Depends: T021,T010)
T042. Implement category trends endpoint (daily snapshot read). (Depends: T022,T011)
T043. Implement certificate info endpoint (metadata) initial version. (Depends: T023,T009)

### Supporting Features
T044. Implement health aggregation scheduler (60s poll, store health_snapshot). (Depends: T011,T032)
T045. Implement state transition evaluator (Degraded/Failed thresholds). (Depends: T029,T044)
T046. Implement certificate lifecycle manager (renewal attempts, warnings). (Depends: T026,T009)
T047. Implement throttling middleware (sliding window). (Depends: T030)
T048. Implement retention job scheduler (audit prune, health prune, trend snapshot). (Depends: T031,T012)
T049. Implement domain propagation/monitor script (alert if >10m). (Depends: T038)

### Dashboard & Frontend Assets
T050. Create static HTML skeleton with service table & placeholders (`src/dashboard/index.html`). (Depends: T020)
T051. Add dashboard JS fetcher updating every 60s (configurable) (`src/dashboard/app.js`). (Depends: T050,T040)
T052. Add visual indicators for cert expiry <30d and status coloring (CSS) (`src/dashboard/styles.css`). (Depends: T050)
T053. Add category/status filters (client-side). (Depends: T051)

### Observability & Logging
T054. Implement structured JSON logger utility. (Depends: T032)
T055. Integrate logging in endpoints & lifecycle managers. (Depends: T054,T033-T043)
T056. Emit audit events for state transitions & certificate renewals. (Depends: T045,T046,T010)

### Testing & Quality
T057. Add unit tests for validation logic (domains, required fields). (Depends: T033)
T058. Add unit tests for state transition evaluator thresholds. (Depends: T045)
T059. Add unit tests for throttling window calculations. (Depends: T047)
T060. Add unit tests for certificate renewal decision logic. (Depends: T046)

### Documentation & Polishing
T061. Update quickstart with certificate info endpoint usage. (Depends: T043)
T062. Add architecture overview diagram (`specs/001-modular-platform-to/architecture.md`). (Depends: T040,T044)
T063. Add README section summarizing feature and how to run local stack. (Depends: T004,T032)
T064. Add CHANGELOG entries for major milestones. (Depends: T043)
T065. Review retention & pruning scripts for idempotency; document in `docs/operations.md`. (Depends: T048)

### Finalization
T066. Run full test suite & ensure all contract/integration tests pass; update plan Gate: Post-Design ✓. (Depends: T032-T065)
T067. Performance smoke test: measure routing latency & adjust thresholds if needed. (Depends: T066)
T068. Security review checklist: no direct port exposure, certificate storage permissions. (Depends: T066)
T069. Prepare release notes & tag pre-release version v0.1.0. (Depends: T066,T068)

## Parallel Execution Guidance
- Models (T009,T010,T011) can proceed in parallel after migrations (T006).
- Contract tests (T014–T023) parallel after base schema (T006).
- Early integration tests (T024–T026) wait for respective contract tests.
- Core endpoints must follow order due to shared service logic; avoid parallelizing T033–T043.
- Dashboard tasks (T050–T053) partially parallel once status feed endpoint (T040) exists.

## Agent Command Examples (Conceptual)
```
/run T013  # implement failing contract test
/run T033  # implement registration endpoint (after test exists)
```

## Totals
- Total Tasks: 69
- Parallelizable [P] tasks: 17

**Status**: READY FOR EXECUTION
