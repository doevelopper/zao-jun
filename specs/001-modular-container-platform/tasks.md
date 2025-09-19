# Tasks: Modular Container Platform

**Input**: Design documents from `/specs/001-modular-container-platform/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
2. Load optional design documents (data-model.md, contracts/, research.md, quickstart.md)
3. Generate tasks by category (Setup, Tests, Core, Integration, Polish)
4. Apply task rules (parallel [P], tests before implementation)
5. Number tasks sequentially; include dependencies and parallel examples
6. Validate task completeness and readiness
```

## Format: `[ID] [P] Description`
- [P]: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Phase 3.1: Setup
- [x] T001 Create repo-level scaffolding to support platform docs and assets (src/, tests/, ci/). Paths at repo root.
- [x] T002 Create `/specs/001-modular-container-platform/catalog/` for service/domain metadata examples and validation samples.
- [x] T003 [P] Add repo docs index linking spec, plan, research, data-model, contracts, quickstart.

## Phase 3.2: Tests First (TDD) — MUST COMPLETE BEFORE 3.3
- [x] T004 [P] Contract test: Onboard Service — write failing test file `tests/contract/test_onboard_service.md` based on `contracts/platform-contracts.md`.
- [x] T005 [P] Contract test: Update Service Metadata — write failing test file `tests/contract/test_update_service.md`.
- [x] T006 [P] Contract test: Remove Service — write failing test file `tests/contract/test_remove_service.md`.
- [x] T007 [P] Contract test: Certificate Check — write failing test file `tests/contract/test_certificate_check.md`.
- [x] T008 [P] Integration test: Homepage listing and status — write failing test `tests/integration/test_homepage_status.md` using `quickstart.md` scenarios.

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [x] T009 [P] Define `src/models/service.yaml` schema matching `data-model.md`.
- [x] T010 [P] Define `src/models/domain.yaml` schema.
- [x] T011 [P] Define `src/models/route.yaml` schema.
- [x] T012 [P] Define `src/models/homepage_entry.yaml` schema.
- [x] T013 [P] Define `src/models/audit_event.yaml` schema.
- [x] T014 Implement `src/lib/validation.md` describing validation rules and examples (unique names/routes, cert policy, etc.).
- [x] T015 Implement `src/lib/catalog.md` describing catalog structure (domains/services) and how metadata is loaded.
- [x] T016 Implement `src/lib/audit.md` describing audit event types and when to emit them.

## Phase 3.4: Integration
- [x] T017 Define `src/lib/cert-policy.md` with production vs non-production rules and exposure behavior on invalid/missing certificates.
- [x] T018 Define `src/lib/access-control.md` for SSO+RBAC mapping to domains and least-privilege guidance.
- [x] T019 Define `src/lib/observability.md` for logs (≥14d) and metrics (≤60s) with dashboard minimums.
- [x] T020 Define `src/lib/rollback.md` for change rollback triggers and steps.

## Phase 3.5: Polish
- [x] T021 [P] Create `docs/homepage-spec.md` describing homepage grouping, status badges, and link behavior on unavailable services.
- [x] T022 [P] Create `docs/onboarding-template.md` for the 10‑minute onboarding checklist.
- [x] T023 [P] Create `docs/certificates-guidance.md` summarizing allowed certificate sources per environment.
- [x] T024 Add `README.md` updates linking all docs and quickstart.

## Dependencies
- Tests (T004–T008) must fail before Core (T009–T016) begins.
- Models (T009–T013) unblock Validation (T014), Catalog (T015), Audit (T016).
- Integration docs (T017–T020) depend on Validation (T014) decisions.
- Polish (T021–T024) depends on Core and Integration sections.

## Parallel Example
```
# Launch independent [P] tasks together (different files):
Task: "Contract test: Onboard Service — tests/contract/test_onboard_service.md"
Task: "Contract test: Update Service — tests/contract/test_update_service.md"
Task: "Contract test: Remove Service — tests/contract/test_remove_service.md"
Task: "Contract test: Certificate Check — tests/contract/test_certificate_check.md"
Task: "Integration test: Homepage listing — tests/integration/test_homepage_status.md"
```

## Validation Checklist
- [ ] All contracts have corresponding contract tests (T004–T007)
- [ ] All entities have model definitions (T009–T013)
- [ ] Tests precede implementation work
- [ ] Parallel tasks only modify distinct files
- [ ] Each task includes a concrete path
