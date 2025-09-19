# Zao-Jun Docs Index

Quick links to planning and design artifacts for the Modular Container Platform.

- Spec: ../specs/001-modular-container-platform/spec.md
- Plan: ../specs/001-modular-container-platform/plan.md
- Research: ../specs/001-modular-container-platform/research.md
- Data Model: ../specs/001-modular-container-platform/data-model.md
- Contracts: ../specs/001-modular-container-platform/contracts/platform-contracts.md
- Quickstart: ../specs/001-modular-container-platform/quickstart.md
- Tasks: ../specs/001-modular-container-platform/tasks.md

Constitution:
- .specify/memory/constitution.md

## Generate Homepage (Preview)
1) Create preview JSON (CI does this automatically):
	- src/cli/validate_catalog.py specs/001-modular-container-platform/catalog --homepage-preview --output specs/001-modular-container-platform/catalog/homepage-preview.json
2) Render HTML:
	- src/cli/generate_homepage.py specs/001-modular-container-platform/catalog/homepage-preview.json --output specs/001-modular-container-platform/catalog/homepage.html
