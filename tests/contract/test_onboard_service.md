# Contract Test: Onboard Service (Failing Spec)

Ref: specs/001-modular-container-platform/contracts/platform-contracts.md (Onboard Service)

## Preconditions
- Unique service name and routes
- Certificate policy satisfied for target environment

## Expected Behavior
- On submit: validate metadata, reject conflicts/invalid
- On success: routing active via single entry point; audit event recorded
- Homepage shows service with status once healthy

## Negative Cases
- Duplicate name or route: onboarding rejected with actionable error
- Invalid/missing cert for env: exposure withheld; audit event emitted

## Assertions (to be automated)
- returns: { success: false, error: "duplicate-name" } when name conflicts
- returns: { success: false, error: "route-conflict" } when route conflicts
- returns: { success: false, error: "certificate-invalid" } when cert invalid
- returns: { success: true } and emits AuditEvent(create) on success
- homepage entry disabled until health=healthy

Status: FAILING (no implementation yet)
