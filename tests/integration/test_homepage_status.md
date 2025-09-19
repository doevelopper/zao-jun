# Integration Test: Homepage Listing & Status (Failing Spec)

Ref: specs/001-modular-container-platform/quickstart.md

## Scenario
- Given a newly onboarded service with valid metadata and healthy status
- When the homepage is viewed through the single TLS entry point
- Then the service appears under its domain with a status badge and working link

## Negative Scenario
- Given a service with unhealthy status
- When the homepage is viewed
- Then the entry is present but link is disabled and status shows "Unavailable" with reason/tooltip

## Assertions (to be automated)
- lists service under correct domain
- shows status badge: healthy/degraded/unavailable
- disables link when status != healthy

Status: FAILING (no implementation yet)
