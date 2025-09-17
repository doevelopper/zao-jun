
# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, or `QWEN.md` for Qwen Code).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Primary objective: Provide a secure, modular, single-host (or small-cluster) multi-service container platform with unified TLS edge, dynamic domain-based routing, standardized onboarding (<10 min SLA), observability, auditability, and a status/dashboard surface. Technical approach (initial, subject to research validation): Leverage a single reverse-proxy/gateway layer terminating TLS, internal dynamic router reading service metadata (labels/manifests), metadata-driven registration workflow producing routing + certificate configuration, centralized health aggregation refreshed ≤60s, and read-only dashboard plus JSON status feed.

## Technical Context
**Language/Version**: Likely Docker Compose orchestrated services + supplemental scripting (Bash + optional Python 3.11 for tooling) (Finalize in Phase 0).  
**Primary Dependencies**: Reverse proxy & dynamic router (gateway + internal label-based router); certificate tooling (self-signed gen + import path); health check & metrics aggregator component; static dashboard (vanilla HTML/CSS/JS).  
**Storage**: PostgreSQL for persistent metadata (services, routing rules, audit events, certificates metadata, category trends); flat files for certificates; optional object storage for archives.  
**Testing**: Container-level integration (pytest or shell-based harness), contract tests (OpenAPI schema validation), dashboard smoke tests (Playwright or lightweight curl/HTML assertions).  
**Target Platform**: Linux host (single) or minimal cluster (≤3 nodes) with Docker runtime.  
**Project Type**: single (Option 1) – monorepo with service definitions and supporting scripts.  
**Performance Goals**: Routing latency p95 ≤250ms under baseline load; onboarding 95% ≤10 min (median ≤5); dashboard refresh interval ≤60s; health aggregation CPU overhead <5%.  
**Constraints**: No direct container host port exposure; fair-share throttle when CPU >80% sustained 5 min; certificate warnings at 30/7/1/<1d; domain propagation ≤5 min typical (≤10 min cap).  
**Scale/Scope**: Target dozens (≤100) heterogeneous services; service categories ~7 functional groups; audit retention 180 days hot.

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Constitution is placeholder (principle slots not yet instantiated). Interim interpretation:
1. Principle 1 (Library-First placeholder): Provide modular separation where feasible (metadata library, health aggregation library) but avoid premature fragmentation on initial delivery → PASS (no violation; single structure kept).
2. Principle 2 (CLI Interface placeholder): All automation (onboarding, status export, certificate rotation) will expose CLI entry points (stdout JSON support) → PASS.
3. Principle 3 (Test-First placeholder): Commit to TDD for contract tests & onboarding validation scripts; tasks will reflect pre-implementation failing tests → PASS contingent on Phase 2 tasks. 
4. Principle 4 (Integration Testing placeholder): Routing & certificate renewal flows earmarked for integration test suite → PASS.
5. Principle 5 (Observability/Simplicity placeholder): Minimal initial components; avoid multi-proxy layering; structured log output (JSON lines) for audit & events → PASS.

No complexity deviations yet (single project structure retained). Re-evaluate post Phase 1 design when contracts enumerated.

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure]
```

**Structure Decision**: Option 1 (Single project). Rationale: Primarily infrastructure + metadata + dashboard; splitting into backend/frontend repos or directories unnecessary until complexity increases (threshold: >1 dedicated API service or JS framework adoption).

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved (expected none outstanding—focus on selecting concrete tooling: language for orchestration scripts, test harness frameworks, audit storage schema, certificate generation approach, health aggregation mechanism).

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/bash/update-agent-context.sh copilot` for your AI assistant
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

Preliminary Contract Candidates (from FRs & Scenarios) – to refine in Phase 1:
- Register Service (POST /services)
- Update Service Metadata (PATCH /services/{id})
- Decommission Service (POST /services/{id}/decommission)
- List Services (GET /services?status=&category=)
- Get Service (GET /services/{id})
- Health Status Feed (GET /status/services.json)
- Domain Reassignment (POST /services/{id}/domain)
- Certificate Info (GET /services/{id}/certificate)
- Preview Routing (POST /routing/preview)
- Audit Events (GET /audit?service_id=)
- Category Trends (GET /analytics/categories/daily)

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each contract → contract test task [P]
- Each entity → model creation task [P] 
- Each user story → integration test task
- Implementation tasks to make tests pass

**Ordering Strategy**:
- TDD order: Tests before implementation 
- Dependency order: Models before services before UI
- Mark [P] for parallel execution (independent files)

**Estimated Output**: 35-40 numbered, ordered tasks (increase due to added dashboard, trends analytics, certificate lifecycle automation, throttle policy tests).

**Additional Phase 2 Notes (Descriptive Only)**:
- Parallelizable groups [P]: Contract test scaffolds, entity migration DDL files, dashboard static asset skeleton, health aggregation polling script baseline.
- Sequential dependencies: Data migrations before contract tests referencing schema; certificate lifecycle script before expiry warning tests; throttling policy config before load-simulation tests.
- Risk items flagged for early inclusion: domain collision preview logic & certificate overlap rotation (reduce late integration surprises).

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
No active violations; table unused.


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [ ] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS (no new deviations introduced by contracts/data model)
- [x] All NEEDS CLARIFICATION resolved
- [ ] Complexity deviations documented (none yet)

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*
